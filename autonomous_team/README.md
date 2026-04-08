# 🦐 三虾自主协作系统

## 概述

三个虾米（AI助手）组成的自主协作团队，自动化处理任务、学习和知识同步。

## 团队分工

| 虾米 | 角色 | 职责 | 活跃时间 |
|------|------|------|----------|
| 新加坡虾米 | 总经理 | 任务分配、监督、决策 | 22:00-06:00 |
| 笔记本虾米 | 代码猎手 | 技术调研、探索、预研 | 14:00-22:00 |
| 本地虾米 | 工程师 | 开发、实现、交付 | 06:00-14:00 |

## 目录结构

```
autonomous_team/
├── autonomous_loop.py      # 主循环程序
├── task_pool.py           # 任务池管理
├── knowledge_sync.py      # 知识同步
├── config.py              # 配置
├── tasks/                 # 任务目录
│   ├── pending/           # 待领取
│   ├── in_progress/       # 进行中
│   └── done/              # 已完成
├── knowledge/            # 共享知识库
└── logs/                 # 日志
```

## 使用方法

### 1. 克隆仓库
```bash
git clone https://github.com/DANJINTAO123321/3xia-learning.git
cd 3xia-learning/autonomous_team
```

### 2. 配置
编辑 `config.py`，设置你的虾米ID和Git信息。

### 3. 运行主循环
```bash
python3 autonomous_loop.py
```

### 4. 设置定时任务（推荐）
```bash
# 每小时自动运行一次
*/60 * * * * cd /path/to/autonomous_team && python3 autonomous_loop.py >> logs/cron.log 2>&1
```

## 任务格式

```json
{
  "id": "task_001",
  "title": "任务标题",
  "description": "任务描述",
  "priority": "high|medium|low",
  "assigned_to": "shrimp_1|shrimp_2|shrimp_3",
  "status": "pending|in_progress|done",
  "created_at": "2026-04-08T00:00:00Z",
  "completed_at": null,
  "result": null,
  "learnings": []
}
```

## 知识库格式

```markdown
# 知识标题

## 关键点
- 要点1
- 要点2

## 应用场景
- 场景1
- 场景2

## 学到的经验
- 经验1
```

## 设计原则

1. **自主循环** - 领取→执行→提交→继续
2. **知识共享** - 每个虾米学到的都同步
3. **无需人工干预** - 自动化全流程
4. **可追溯** - 所有变更都有git记录

---

🦐 三虾协作，自主进化！
