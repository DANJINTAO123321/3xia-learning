#!/usr/bin/env python3
"""
三虾自主协作系统 - 配置
"""

# ============ 虾米身份配置 ============
SHRIMP_ID = "shrimp_2"  # shrimp_1=新加坡, shrimp_2=本地, shrimp_3=笔记本
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
