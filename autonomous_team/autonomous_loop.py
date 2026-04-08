#!/usr/bin/env python3
"""
三虾自主协作系统 - 主循环
自动领取任务、执行、提交、同步知识
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
    get_in_progress_tasks, complete_task, create_task
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
    code, out, err = run_cmd(f"git pull origin {GIT_BRANCH}", cwd=repo_path)
    if code == 0:
        log("✅ 拉取成功")
    else:
        log(f"⚠️ 拉取失败: {err[:200]}")
    return code == 0

def git_push():
    """推送代码"""
    log("📤 推送代码...")
    repo_path = LOCAL_REPO_PATH or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    code, out, err = run_cmd(f"git add {TASKS_DIR} {KNOWLEDGE_DIR} && git commit -m '[{SHRIMP_ID}] 自动提交: {datetime.now().strftime(\"%Y-%m-%d %H:%M\")}' && git push origin {GIT_BRANCH}", cwd=repo_path)
    if code == 0:
        log("✅ 推送成功")
    else:
        log(f"⚠️ 推送失败: {err[:200]}")
    return code == 0

def execute_task(task):
    """执行任务（示例模板，根据实际任务定制）"""
    log(f"🔧 执行任务: {task['title']}")
    
    task_id = task['id']
    description = task.get('description', '')
    
    # 根据任务类型生成执行结果
    # 这里需要根据实际情况扩展
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
        f"任务类型: {task.get('priority', 'normal')}优先级"
    ]
    
    return result, learnings

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
    log(f"🦐 {SHRIMP_NAME} ({SHRIMP_ROLE}) 自主循环开始")
    log(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("=" * 50)
    
    # 1. 确保目录存在
    ensure_dirs()
    
    # 2. 拉取最新代码
    git_pull()
    
    # 3. 检查是否有未完成的任务
    in_progress = get_in_progress_tasks()
    if in_progress:
        log(f"📋 发现 {len(in_progress)} 个进行中的任务，继续执行...")
        for task in in_progress:
            try:
                result, learnings = execute_task(task)
                complete_task(task, result, learnings)
                log(f"✅ 完成任务: {task['title']}")
                
                # 保存学习成果
                save_learning(
                    title=f"任务完成: {task['title']}",
                    content=json.dumps(result, ensure_ascii=False, indent=2),
                    tags=['task', 'completed', SHRIMP_ID]
                )
            except Exception as e:
                log(f"❌ 任务执行失败: {e}")
    
    # 4. 领取新任务
    log("🔍 检查新任务...")
    new_tasks = claim_tasks_if_available()
    
    # 5. 执行新领取的任务
    for task in new_tasks:
        try:
            result, learnings = execute_task(task)
            complete_task(task, result, learnings)
            log(f"✅ 完成新任务: {task['title']}")
            
            # 保存学习成果
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
    log(f"🦐 {SHRIMP_NAME} 自主循环完成")
    log("=" * 50)

if __name__ == "__main__":
    main()
