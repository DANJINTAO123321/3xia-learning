#!/usr/bin/env python3
"""
三虾自主协作系统 - 配置

正确ID对应：
- shrimp_1 = 笔记本虾米（代码猎手）
- shrimp_2 = 本地虾米（工程师）
- shrimp_3 = 新加坡虾米（总经理）
"""

# ============ 虾米身份配置 ============
SHRIMP_ID = "shrimp_2"  # 根据你的身份修改！
SHRIMP_NAME = "本地虾米"
SHRIMP_ROLE = "工程师"  # 总经理/代码猎手/工程师

# ============ Git 配置 ============
GIT_REPO = "https://github.com/DANJINTAO123321/3xia-learning.git"
GIT_BRANCH = "main"
LOCAL_REPO_PATH = None  # 自动检测，或手动指定如 "/root/.openclaw/workspace/3xia-learning"

# ============ 任务池路径 ============
TASKS_DIR = "autonomous_team/tasks"
PENDING_DIR = f"{TASKS_DIR}/pending"
IN_PROGRESS_DIR = f"{TASKS_DIR}/in_progress"
DONE_DIR = f"{TASKS_DIR}/done"

# ============ 知识库路径 ============
KNOWLEDGE_DIR = "autonomous_team/knowledge"

# ============ 日志 ============
LOG_DIR = "autonomous_team/logs"
LOG_FILE = f"{LOG_DIR}/autonomous_{SHRIMP_ID}.log"

# ============ 定时配置 ============
CHECK_INTERVAL_HOURS = 1  # 每小时检查一次
MAX_TASKS_PER_CYCLE = 3   # 每次最多领取3个任务
