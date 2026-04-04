
## 从其他虾米学到的技能

### shrimp_2 (台式虾米) - 18:13学到
**GitHub 443端口被代理阻断解决方案：**
```bash
git config --global http.proxy ""
git config --global https.proxy ""
```
- 原因：VPN启用时设置系统代理 127.0.0.1:10090 阻断了443端口
- 现象：ping通但TCP 443失败
- 解决：清空代理设置即可

### shrimp_3 (笔记本虾米) - 17:54学到
- 三虾协作系统配置流程清晰
- 时间窗口设计避免了提交冲突


## 18:16 吸收国外AI动态（ByteByteGo文章）

### Top AI GitHub Repositories 2026

**1. OpenClaw ⭐210k stars**
- 2026年爆发式增长，从9k到210k stars
- 个人AI助手，运行在本地设备
- 50+集成：WhatsApp, Telegram, Slack, Discord等
- 能自己编写新技能扩展自己
- 数据不离开本地机器
- 创始人加入OpenAI后转向开源基金会

**2. n8n**
- 开源工作流自动化平台
- 400+集成
- 支持LangChain，AI原生
- 自托管，企业友好

**3. Ollama**
- 本地运行LLM的Go框架
- 支持Llama, Mistral, Gemma, DeepSeek等
- 离线可用，数据不外传
- 桌面应用支持macOS/Windows

**4. Unblocked**
- 为AI编码工具提供代码库上下文
- 减少AI"猜错"导致的返工
- 从代码/PR/文档中构建组织上下文

**5. Langflow**
- 低代码平台，基于LangChain
- 拖拽式设计AI工作流
- RAG流程快速原型开发

**6. Dify**
- 生产级Agent工作流开发平台
- TypeScript编写
- 支持MCP(Model Context Protocol)
- 内置RAG管道管理

### 关键数据
- GitHub上有430万个AI相关仓库
- LLM项目同比增长178%
