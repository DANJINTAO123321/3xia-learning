# HEARTBEAT.md - 自动检查配置（台式虾米 shrimp_2）

## 检查频率
- 每5分钟自动检查一次

---

## 🕐 固定学习时段（每天6个）

| 时间 | 任务 | 时长 | 备注 |
|------|------|------|------|
| 08:00 | 晨间检查：clawhub.ai新技术 + Git更新 | ~10分钟 | 检查仓库更新 |
| 10:00 | 编程技能学习（Python/设计模式/代码） | ~15分钟 | 代码能力 |
| 12:00 | 玲珑矩阵相关学习 + 飞书API | ~15分钟 | 项目相关 |
| 14:00 | 深入技能学习（读文档/源码分析） | ~15分钟 | 技能提升 |
| 16:00 | 实践练习（写代码/自动化脚本） | ~15分钟 | 动手实践 |
| 18:00 | 今日总结 + 记忆整理 + 计划明天 | ~10分钟 | 复盘反思 |

---

## 🦐 三虾操作时间窗口

**每小时的20-40分为我的活跃窗口**（如16:20-16:40）

- 这个时间段内：
  1. 检查Git仓库更新（`git pull --rebase origin main`）
  2. 查看questions/shrimp_2/是否有新问题
  3. 执行主动学习
  4. 记录学习到 `3xia-learning/daily/shrimp_2/`
  5. 推送Git

---

## 📚 学习内容池（4个维度轮换）

### 1. 代码能力
- Python异步编程、TypeScript、Docker、设计模式
- Windows PowerShell高级用法
- API设计、数据库SQL

### 2. 玲珑矩阵相关
- 三虾通讯系统开发
- 飞书API深度应用
- AutoCAD/SketchUp插件开发

### 3. OpenClaw生态
- 官方文档更新
- clawhub.ai新技能（每日必查）
- 技能开发与发布

### 4. 实用工具
- Git高级用法、Vim
- Windows Terminal优化
- VSCode/开发工具技巧

---

## 🔄 心跳检查流程

### 每次心跳必须执行：
1. 检查学习时段是否到达，到达则执行学习
2. 检查Git仓库更新（每窗口期一次）
3. 检查questions/shrimp_2/是否有待处理问题
4. 更新heartbeat-state.json记录状态

### 异常检测：
- 发现异常立即记录到memory/YYYY-MM-DD.md
- 必要时向涛哥汇报

---

## 📁 关键路径

| 类型 | 路径 |
|------|------|
| 三虾学习仓库 | C:\Users\25383\.openclaw\workspace\3xia-learning |
| 学习记录 | C:\Users\25383\.openclaw\workspace\3xia-learning\daily\shrimp_2\ |
| 问题接收 | C:\Users\25383\.openclaw\workspace\3xia-learning\questions\shrimp_2\ |
| 回答归档 | C:\Users\25383\.openclaw\workspace\3xia-learning\answers\shrimp_2\ |
| 本地记忆 | C:\Users\25383\.openclaw\workspace\memory\YYYY-MM-DD.md |
| 心跳状态 | C:\Users\25383\.openclaw\workspace\memory\heartbeat-state.json |

---

## ✅ 学习记录标准

每次学习后必须记录：
```markdown
## HH:MM 学习主题
- [核心概念]: [具体学到什么]
- [使用场景]: [什么时候可以用]
```

**不记录等于没学！**

---

## 🚀 主动学习流程

### 在时间窗口内（20-40分）：
1. `git pull --rebase origin main`
2. 检查questions/shrimp_2/有新问题立即回答
3. 从学习内容池选择一个主题学习
4. 记录到 `daily/shrimp_2/学习_shrimp_2_YYYYMMDD_HHMM_XX.md`
5. `git add . && git commit -m "[shrimp_2] HH:MM 学习更新" && git push origin main`

---

## 版本
- v2.0 - 2026-04-05 - 参考笔记本虾米经验更新
