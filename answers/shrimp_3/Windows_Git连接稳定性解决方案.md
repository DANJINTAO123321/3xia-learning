# Windows系统Git连接稳定性问题解决方案

## 问题分析

### Windows系统Git连接不稳定的常见原因

1. **SSH连接频繁断开**
   - Windows防火墙或安全软件干扰
   - SSH客户端配置问题
   - 网络适配器节能设置

2. **Git Bash vs CMD vs PowerShell差异**
   - Git Bash (MSYS2) 兼容性最好
   - CMD次之
   - PowerShell有时有问题

3. **凭据缓存问题**
   - Windows凭据管理器冲突
   - Git Credential Helper配置不当

---

## 解决方案

### 方案1：优化SSH配置（推荐）

在Windows上创建/修改 `C:\Users\<用户名>\.ssh\config`：

```
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    TCPKeepAlive yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
    Compression yes
    Protocol 2
```

### 方案2：Git全局配置优化

```cmd
git config --global http.postBuffer 524288000
git config --global http.lowSpeedLimit 1000
git config --global http.lowSpeedTime 60
git config --global http.maxRequestBuffer 100M
git config --global http.version HTTP/1.1
git config --global core.compression 9
```

### 方案3：使用SSH替代HTTPS（最稳定）

```cmd
# 取消HTTPS，改用SSH
git config --global url."git@github.com:".insteadOf "https://github.com/"

# 或单独为当前仓库
git remote set-url origin git@github.com:DANJINTAO123321/3xia-learning.git
```

### 方案4：Windows特定优化

1. **关闭IPv6**（有时有干扰）：
```cmd
git config --global http.proxy ""
git config --global https.proxy ""
```

2. **设置SSH超时**：
```cmd
git config --global ssh.timeout 60
```

3. **使用Git Credential Manager**：
```cmd
git config --global credential.helper manager
```

### 方案5：网络稳定性优化

1. **ping测试**：
```cmd
ping github.com
```

2. **修改DNS**（改用Google DNS）：
```
8.8.8.8
8.8.4.4
```

3. **检查代理设置**：
```cmd
git config --global --unset http.proxy
git config --global --unset https.proxy
```

---

## 简化版快速修复（本地虾米专用）

在CMD或PowerShell中依次执行：

```cmd
:: 1. 设置SSH保活
git config --global ssh.timeout 60

:: 2. 设置HTTP优化
git config --global http.postBuffer 524288000
git config --global http.version HTTP/1.1

:: 3. 改用SSH地址
git remote set-url origin git@github.com:DANJINTAO123321/3xia-learning.git

:: 4. 验证连接
ssh -T git@github.com
```

---

## 判断是否成功

```cmd
:: 测试GitHub连接
ssh -T git@github.com

:: 测试仓库克隆
git ls-remote origin
```

成功会显示：
```
You've successfully authenticated, but GitHub does not provide shell access.
```

---

## 关键区别

| 设置 | HTTP | SSH |
|------|------|-----|
| 速度 | 较慢 | 快 |
| 稳定性 | 不稳定 | 稳定 |
| 防火墙问题 | 常有 | 少 |
| 凭据问题 | 常有 | 无 |

**推荐：使用SSH方式**

---

## 涛哥备注
- 笔记本虾米(我)是Linux系统，天然稳定
- 本地虾米是Windows系统，需要额外配置
- 核心是改用SSH方式，配置SSH保活参数
