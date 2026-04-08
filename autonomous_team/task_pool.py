#!/usr/bin/env python3
"""
三虾自主协作系统 - 任务池管理
支持完整任务生命周期：todo → doing → done → closed
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
    os.makedirs(PENDING_DIR, exist_ok=True)
    os.makedirs(IN_PROGRESS_DIR, exist_ok=True)
    os.makedirs(DONE_DIR, exist_ok=True)

def get_tasks_by_status(status):
    """获取指定状态的任务"""
    ensure_dirs()
    status_dir = {
        'todo': PENDING_DIR,
        'doing': IN_PROGRESS_DIR,
        'done': DONE_DIR
    }.get(status)
    
    if not status_dir:
        return []
    
    tasks = []
    for f in os.listdir(status_dir):
        if f.endswith('.json'):
            with open(os.path.join(status_dir, f), 'r', encoding='utf-8') as fp:
                tasks.append(json.load(fp))
    return tasks

def get_pending_tasks():
    """获取所有待领取任务（未分配或分配给当前虾米）"""
    ensure_dirs()
    pending = []
    for f in os.listdir(PENDING_DIR):
        if f.endswith('.json'):
            with open(os.path.join(PENDING_DIR, f), 'r', encoding='utf-8') as fp:
                task = json.load(fp)
                # 领取条件：未分配 或 分配给当前虾米
                if task.get('assigned_to') is None or task.get('assigned_to') == SHRIMP_ID:
                    pending.append(task)
    
    # 按优先级排序
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    pending.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 3))
    return pending

def get_my_tasks():
    """获取当前虾米的所有任务（doing和done）"""
    ensure_dirs()
    my_tasks = {'doing': [], 'done': []}
    
    for status, tasks_list in [('doing', my_tasks['doing']), ('done', my_tasks['done'])]:
        dir_path = IN_PROGRESS_DIR if status == 'doing' else DONE_DIR
        for f in os.listdir(dir_path):
            if f.endswith('.json'):
                with open(os.path.join(dir_path, f), 'r', encoding='utf-8') as fp:
                    task = json.load(fp)
                    if task.get('assigned_to') == SHRIMP_ID:
                        tasks_list.append(task)
    
    return my_tasks

def claim_task(task):
    """领取任务"""
    task['status'] = 'doing'
    task['assigned_to'] = SHRIMP_ID
    task['assigned_name'] = SHRIMP_NAME
    task['claimed_at'] = datetime.now().isoformat() + 'Z'
    task['started_at'] = datetime.now().isoformat() + 'Z'
    
    # 移动到进行中
    src = os.path.join(PENDING_DIR, f"{task['id']}.json")
    dst = os.path.join(IN_PROGRESS_DIR, f"{task['id']}.json")
    if os.path.exists(src):
        shutil.move(src, dst)
    
    with open(dst, 'w', encoding='utf-8') as fp:
        json.dump(task, fp, indent=2, ensure_ascii=False)
    
    return task

def complete_task(task, result, learnings=None):
    """完成任务，提交待审核"""
    task['status'] = 'done'
    task['completed_at'] = datetime.now().isoformat() + 'Z'
    task['completed_by'] = SHRIMP_ID
    task['result'] = result
    task['learnings'] = learnings or []
    task['submitted_for_review'] = True
    
    # 移动到已完成（待审核）
    src = os.path.join(IN_PROGRESS_DIR, f"{task['id']}.json")
    dst = os.path.join(DONE_DIR, f"{task['id']}.json")
    if os.path.exists(src):
        shutil.move(src, dst)
    
    with open(dst, 'w', encoding='utf-8') as fp:
        json.dump(task, fp, indent=2, ensure_ascii=False)
    
    return task

def approve_task(task):
    """审核通过任务（总经理权限）"""
    task['status'] = 'closed'
    task['approved_at'] = datetime.now().isoformat() + 'Z'
    task['approved_by'] = SHRIMP_ID
    
    # 移动到closed目录（如果有）
    closed_dir = os.path.join(DONE_DIR, '..', 'closed')
    os.makedirs(closed_dir, exist_ok=True)
    
    src = os.path.join(DONE_DIR, f"{task['id']}.json")
    dst = os.path.join(closed_dir, f"{task['id']}.json")
    if os.path.exists(src):
        shutil.move(src, dst)
        with open(dst, 'w', encoding='utf-8') as fp:
            json.dump(task, fp, indent=2, ensure_ascii=False)
    
    return task

def reject_task(task, reason):
    """驳回任务（打回重做）"""
    task['status'] = 'todo'
    task['rejected_reason'] = reason
    task['rejected_at'] = datetime.now().isoformat() + 'Z'
    task['rejected_by'] = SHRIMP_ID
    
    # 移回待办
    src = os.path.join(DONE_DIR, f"{task['id']}.json")
    dst = os.path.join(PENDING_DIR, f"{task['id']}.json")
    if os.path.exists(src):
        shutil.move(src, dst)
    
    with open(dst, 'w', encoding='utf-8') as fp:
        json.dump(task, fp, indent=2, ensure_ascii=False)
    
    return task

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
        'status': 'todo',
        'created_at': datetime.now().isoformat() + 'Z',
        'created_by': SHRIMP_ID,
        'result': None,
        'learnings': [],
        'subtasks': []
    }
    
    ensure_dirs()
    with open(os.path.join(PENDING_DIR, f"{task_id}.json"), 'w', encoding='utf-8') as fp:
        json.dump(task, fp, indent=2, ensure_ascii=False)
    
    return task
