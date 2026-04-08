#!/usr/bin/env python3
"""
三虾自主协作系统 - 任务池管理
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from config import (
    PENDING_DIR, IN_PROGRESS_DIR, DONE_DIR, 
    SHRIMP_ID, SHRIMP_NAME, MAX_TASKS_PER_CYCLE
)

def ensure_dirs():
    """确保任务目录存在"""
    for d in [PENDING_DIR, IN_PROGRESS_DIR, DONE_DIR]:
        os.makedirs(d, exist_ok=True)

def get_pending_tasks():
    """获取所有待领取任务"""
    ensure_dirs()
    pending = []
    for f in os.listdir(PENDING_DIR):
        if f.endswith('.json'):
            with open(os.path.join(PENDING_DIR, f), 'r', encoding='utf-8') as fp:
                pending.append(json.load(fp))
    # 按优先级排序
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    pending.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 3))
    return pending

def claim_task(task):
    """领取任务"""
    task['status'] = 'in_progress'
    task['assigned_to'] = SHRIMP_ID
    task['assigned_name'] = SHRIMP_NAME
    task['claimed_at'] = datetime.now().isoformat() + 'Z'
    
    # 移动到进行中
    src = os.path.join(PENDING_DIR, f"{task['id']}.json")
    dst = os.path.join(IN_PROGRESS_DIR, f"{task['id']}.json")
    shutil.move(src, dst)
    
    with open(dst, 'w', encoding='utf-8') as fp:
        json.dump(task, fp, indent=2, ensure_ascii=False)
    
    return task

def complete_task(task, result, learnings=None):
    """完成任务"""
    task['status'] = 'done'
    task['completed_at'] = datetime.now().isoformat() + 'Z'
    task['result'] = result
    task['learnings'] = learnings or []
    
    # 移动到已完成
    src = os.path.join(IN_PROGRESS_DIR, f"{task['id']}.json")
    dst = os.path.join(DONE_DIR, f"{task['id']}.json")
    shutil.move(src, dst)
    
    with open(dst, 'w', encoding='utf-8') as fp:
        json.dump(task, fp, indent=2, ensure_ascii=False)
    
    return task

def get_in_progress_tasks():
    """获取我正在进行的任务"""
    ensure_dirs()
    tasks = []
    for f in os.listdir(IN_PROGRESS_DIR):
        if f.endswith('.json'):
            with open(os.path.join(IN_PROGRESS_DIR, f), 'r', encoding='utf-8') as fp:
                t = json.load(fp)
                if t.get('assigned_to') == SHRIMP_ID:
                    tasks.append(t)
    return tasks

def claim_tasks_if_available():
    """领取可用的任务"""
    pending = get_pending_tasks()
    claimed = []
    
    for task in pending[:MAX_TASKS_PER_CYCLE]:
        # 检查是否已经分配给别人
        if task.get('assigned_to') and task['assigned_to'] != SHRIMP_ID:
            continue
        claim_task(task)
        claimed.append(task)
        print(f"  ✅ 领取任务: {task['title']}")
    
    return claimed

def create_task(title, description, priority='medium', assigned_to=None):
    """创建新任务"""
    task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    task = {
        'id': task_id,
        'title': title,
        'description': description,
        'priority': priority,
        'assigned_to': assigned_to,
        'status': 'pending',
        'created_at': datetime.now().isoformat() + 'Z',
        'created_by': SHRIMP_ID,
        'result': None,
        'learnings': []
    }
    
    ensure_dirs()
    with open(os.path.join(PENDING_DIR, f"{task_id}.json"), 'w', encoding='utf-8') as fp:
        json.dump(task, fp, indent=2, ensure_ascii=False)
    
    return task
