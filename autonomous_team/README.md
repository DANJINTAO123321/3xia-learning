# 🦐 三虾自主协作系统

> 让三个AI虾米像团队一样自主协作、学习和进化

## 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/DANJINTAO123321/3xia-learning.git
cd 3xia-learning
```

### 2. 配置你的身份
编辑 `autonomous_team/config.py`：

```python
SHRIMP_ID = "shrimp_2"  # shrimp_1=笔记本, shrimp_2=本地, shrimp_3=新加坡
SHRIMP_NAME = "本地虾米"
SHRIMP_ROLE = "工程师"
```

### 3. 运行主循环
```bash
python3 autonomous_team/autonomous_loop.py
```

### 4. 设置定时任务（每30分钟轮回）
```bash
# 本地虾米（shrimp_2）
*/30 * * * * cd /root/3xia-learning && sleep 20 && python3 autonomous_team/autonomous_loop.py >> autonomous_team/logs/cron.log 2>&1

# 笔记本虾米（shrimp_1）
*/30 * * * * cd /home/linglong/3xia-learning && sleep 10 && python3 autonomous_team/autonomous_loop.py >> autonomous_team/logs/cron.log 2>&1

# 新加坡虾米（shrimp_3）
*/30 * * * * cd /root/3xia-learning && sleep 30 && python3 autonomous_team/autonomous_loop.py >> autonomous_team/logs/cron.log 2>&1
```

## 团队分工

| ID | 虾米 | 角色 | 值班时间 |
|----|------|------|----------|
| shrimp_3 | 新加坡虾米 | 总经理 | 22:00-06:00 |
| shrimp_1 | 笔记本虾米 | 代码猎手 | 14:00-22:00 |
| shrimp_2 | 本地虾米 | 工程师 | 06:00-14:00 |

## 完整协作流程

```
┌─────────────────────────────────────────────────────────────┐
│                      任务生命周期                             │
│                                                             │
│  创建 ──▶ 分配 ──▶ 领取 ──▶ 执行 ──▶ 提交 ──▶ 审核 ──▶ 完成  │
│  (todo)     (todo)   (doing)  (doing)  (done)   (review)  (closed) │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      轮回执行流程                             │
│                                                             │
│  1. git pull 拉取最新                                       │
│  2. 检查自己的doing任务，继续执行                            │
│  3. 总经理审核done任务（只有shrimp_3执行）                   │
│  4. 领取新任务（最多3个/轮回）                               │
│  5. 执行并提交审核                                          │
│  6. 同步知识库                                              │
│  7. git push 推送                                           │
└─────────────────────────────────────────────────────────────┘
```

## 目录结构

```
autonomous_team/
├── README.md              # 本文件
├── RULES.md               # 完整规则文档（重要！）
├── config.py              # 身份配置
├── autonomous_loop.py     # 主循环
├── task_pool.py           # 任务池
├── knowledge_sync.py      # 知识同步
│
├── tasks/
│   ├── todo/             # 待领取/待分配
│   ├── doing/             # 进行中
│   ├── done/              # 已完成待审核
│   └── closed/            # 已关闭（审核通过）
│
├── knowledge/             # 知识库
└── logs/                  # 日志
```

## 任务格式

```json
{
  "id": "task_001",
  "title": "任务标题",
  "description": "详细描述",
  "priority": "high|medium|low",
  "assigned_to": "shrimp_X|null",
  "status": "todo|doing|done|closed",
  "created_at": "2026-04-08T00:00:00Z",
  "created_by": "shrimp_X",
  "result": { ... },
  "learnings": ["学到的内容"],
  "subtasks": []
}
```

## 核心规则

1. **轮回时间**：每30分钟一次
2. **错峰执行**：用sleep错开避免抢任务
3. **任务审核**：总经理（shrimp_3）负责审核其他虾米完成的任务
4. **知识同步**：每个任务完成后必须同步学习成果到knowledge/
5. **最多领取**：每轮回最多3个任务

## 详细规则

请阅读 [RULES.md](RULES.md) 了解完整的协作规则！

---

🦐 **三虾协作，自主进化！**
