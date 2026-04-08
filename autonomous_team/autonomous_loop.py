#!/usr/bin/env python3
"""
三虾自主协作系统 - 主循环
自动领取任务、执行、提交审核、同步知识
"""

import os
import sys
import json
import subprocess
import logging
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    GIT_REPO, GIT_BRANCH, LOCAL_REPO_PATH,
    LOG_DIR, LOG_FILE, SHRIMP_ID, SHRIMP_NAME, SHRIMP_ROLE,
    TASKS_DIR, KNOWLEDGE_DIR
)
from task_pool import (
    ensure_dirs, claim_tasks_if_available, 
    get_my_tasks, complete_task, approve_task, reject_task,
    get_pending_tasks, create_task
)
from knowledge_sync import save_learning, get_recent_knowledge

# ============ 日志配置 ============
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def log(msg):
    """打印带虾米标识的日志"""
    prefix = f"[{SHRIMP_NAME}]"
    logger.info(f"{prefix} {msg}")

def run_cmd(cmd, cwd=None, capture=True):
    """运行命令"""
    try:
        if capture:
            result = subprocess.run(
                cmd, shell=True, cwd=cwd,
                capture_output=True, text=True, timeout=120
            )
            return result.returncode, result.stdout, result.stderr
        else:
            result = subprocess.run(cmd, shell=True, cwd=cwd)
            return result.returncode, "", ""
    except subprocess.TimeoutExpired:
        return -1, "", "Command timeout"
    except Exception as e:
        return -1, "", str(e)

def git_pull():
    """拉取最新代码"""
    log("📥 拉取最新代码...")
    repo_path = LOCAL_REPO_PATH or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    code, out, err = run_cmd(f"git pull origin {GIT_BRANCH} --rebase", cwd=repo_path)
    if code == 0:
        log("✅ 拉取成功")
    else:
        log(f"⚠️ 拉取失败: {err[:200]}")
    return code == 0

def git_push():
    """推送代码"""
    log("📤 推送代码...")
    repo_path = LOCAL_REPO_PATH or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    commit_msg = f'[{SHRIMP_ID}] 自动轮回: {timestamp}'
    cmd = f'git add {TASKS_DIR} {KNOWLEDGE_DIR} && git commit -m "{commit_msg}" && git push origin {GIT_BRANCH}'
    code, out, err = run_cmd(cmd, cwd=repo_path)
    if code == 0:
        log("✅ 推送成功")
    else:
        log(f"⚠️ 推送失败: {err[:200]}")
    return code == 0

def execute_task(task):
    """执行任务
    
    这是一个模板方法，实际任务会根据task的内容执行不同操作。
    返回执行结果和学习内容。
    """
    log(f"🔧 执行任务: {task['title']}")
    
    task_id = task['id']
    description = task.get('description', '')
    
    # ========== 这里是任务执行的核心逻辑 ==========
    # 根据不同任务类型实现具体执行
    # 例如：
    # - 代码开发任务：写代码、测试
    # - 调研任务：搜索、整理资料
    # - 学习任务：阅读、总结
    # ==========================================
    
    # 示例：如果是测试任务
    result = {
        'task_id': task_id,
        'executed_by': SHRIMP_ID,
        'executed_at': datetime.now().isoformat() + 'Z',
        'status': 'completed',
        'summary': f"任务 '{task['title']}' 已完成",
        'details': description
    }
    
    # 学习成果
    learnings = [
        f"完成了任务: {task['title']}",
        f"任务优先级: {task.get('priority', 'normal')}",
        f"执行虾米: {SHRIMP_NAME} ({SHRIMP_ID})"
    ]
    
    return result, learnings

def review_done_tasks():
    """审核已完成的任务（仅总经理执行）"""
    if SHRIMP_ID != "shrimp_3":  # 只有新加坡虾米是总经理
        return
    
    my_tasks = get_my_tasks()
    done_tasks = my_tasks.get('done', [])
    
    if not done_tasks:
        log("📋 没有待审核的任务")
        return
    
    for task in done_tasks:
        # 简单策略：检查result是否存在且有效
        if task.get('result'):
            log(f"✅ 审核通过任务: {task['title']}")
            approve_task(task)
            
            # 同步知识
            if task.get('learnings'):
                save_learning(
                    title=f"任务完成: {task['title']}",
                    content=json.dumps({
                        'task': task['title'],
                        'result': task['result'],
                        'learnings': task['learnings']
                    }, ensure_ascii=False, indent=2),
                    tags=['task', 'completed', task.get('priority', 'normal')]
                )
        else:
            log(f"⚠️ 任务结果为空，打回: {task['title']}")
            reject_task(task, "任务结果为空，请补充完整")

def sync_knowledge_from_team():
    """同步团队其他虾米的知识"""
    log("📚 同步团队知识库...")
    recent = get_recent_knowledge(limit=5)
    for item in recent:
        log(f"  发现知识: {item['name']}")
    return len(recent)

def main():
    """主循环"""
    log("=" * 50)
    log(f"🦐 {SHRIMP_NAME} ({SHRIMP_ROLE}) 自主轮回开始")
    log(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("=" * 50)
    
    # 1. 确保目录存在
    ensure_dirs()
    
    # 2. 拉取最新代码
    git_pull()
    
    # 3. 检查我的进行中任务，继续执行
    my_tasks = get_my_tasks()
    
    # 3.1 继续执行 doing 任务
    if my_tasks.get('doing'):
        log(f"📋 发现 {len(my_tasks['doing'])} 个进行中的任务，继续执行...")
        for task in my_tasks['doing']:
            try:
                result, learnings = execute_task(task)
                complete_task(task, result, learnings)
                log(f"✅ 完成任务并提交审核: {task['title']}")
                
                # 保存学习成果
                if learnings:
                    save_learning(
                        title=f"任务完成: {task['title']}",
                        content=json.dumps(result, ensure_ascii=False, indent=2),
                        tags=['task', 'completed', SHRIMP_ID]
                    )
            except Exception as e:
                log(f"❌ 任务执行失败: {e}")
    
    # 3.2 总经理审核 done 任务
    if SHRIMP_ID == "shrimp_3":
        review_done_tasks()
    
    # 4. 领取新任务
    log("🔍 检查新任务...")
    new_tasks = claim_tasks_if_available()
    
    # 5. 执行新领取的任务
    for task in new_tasks:
        try:
            result, learnings = execute_task(task)
            complete_task(task, result, learnings)
            log(f"✅ 完成新任务并提交审核: {task['title']}")
            
            # 保存学习成果
            if learnings:
                save_learning(
                    title=f"任务完成: {task['title']}",
                    content=json.dumps(result, ensure_ascii=False, indent=2),
                    tags=['task', 'completed', SHRIMP_ID]
                )
        except Exception as e:
            log(f"❌ 任务执行失败: {e}")
    
    # 6. 同步知识
    sync_knowledge_from_team()
    
    # 7. 提交并推送
    git_push()
    
    log("=" * 50)
    log(f"🦐 {SHRIMP_NAME} 自主轮回完成")
    log("=" * 50)

if __name__ == "__main__":
    main()
