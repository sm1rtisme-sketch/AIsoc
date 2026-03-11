# CyberStrikeAI 二次开发指南

## 1. 概述

CyberStrikeAI 采用模块化设计，支持多种形式的二次开发：

- 自定义安全工具
- 自定义角色
- 自定义技能
- 外部 MCP 集成
- API 扩展

## 2. 自定义安全工具

### 2.1 工具配置文件格式

在 `tools/` 目录下创建 YAML 文件：

```yaml
name: "工具名称"
command: "命令"
args: ["参数"]
enabled: true
short_description: "简短描述"
description: |
  详细描述
  支持多行
parameters:
  - name: "参数名"
    type: "string"
    description: "参数描述"
    required: true
    position: 0  # 位置参数
  - name: "ports"
    type: "string"
    flag: "-p"   # 标志参数
    description: "端口范围"
```

### 2.2 工具定义示例

创建 `tools/nmap.yaml`：

```yaml
name: "nmap"
command: "nmap"
args: ["-sT", "-sV", "-sC"]
enabled: true
short_description: "网络映射和服务指纹识别"
description: |
  Nmap（Network Mapper）是一款用于网络发现和安全审计的开源工具。
  支持端口扫描、服务版本检测、操作系统检测等功能。
parameters:
  - name: "target"
    type: "string"
    description: "目标 IP 或域名"
    required: true
    position: 0
  - name: "ports"
    type: "string"
    flag: "-p"
    description: "端口范围，如 1-1000"
  - name: "scripts"
    type: "string"
    flag: "--script"
    description: "NSE 脚本"
```

### 2.3 工具热加载

工具配置文件修改后：
1. 重启服务
2. 或在 Web 界面 Settings 中 reload

## 3. 自定义角色

### 3.1 角色配置文件格式

在 `roles/` 目录下创建 YAML 文件：

```yaml
name: "角色名称"
description: "角色描述"
user_prompt: |
  系统提示词
  定义角色行为
icon: "🎯"
tools:
  - 工具名称
  - 另一个工具
skills:
  - 技能名称
enabled: true
```

### 3.2 角色定义示例

创建 `roles/custom-pentest.yaml`：

```yaml
name: "自定义渗透测试"
description: "针对 API 的渗透测试角色"
user_prompt: |
  你是一名专业的 API 安全测试专家。
  专注于发现 API 中的安全漏洞，包括但不限于：
  - SQL 注入
  - XSS
  - 权限绕过
  - 认证问题
  请使用专业的工具和方法进行测试。
icon: "🔐"
tools:
  - nmap
  - httpx
  - sqlmap
  - nuclei
  - arjun
  - graphql-scanner
  - record_vulnerability
  - search_knowledge_base
skills:
  - api-security-testing
  - sql-injection-testing
enabled: true
```

### 3.3 角色字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| name | 是 | 角色名称 |
| description | 是 | 角色描述 |
| user_prompt | 否 | 系统提示词 |
| icon | 否 | 图标（emoji） |
| tools | 否 | 可用工具列表 |
| skills | 否 | 附加技能列表 |
| enabled | 是 | 是否启用 |

### 3.4 角色热加载

角色配置文件修改后自动生效，无需重启。

## 4. 自定义技能

### 4.1 技能目录结构

在 `skills/` 目录下创建目录：

```
skills/
└── my-skill/
    └── SKILL.md
```

### 4.2 SKILL.md 格式

```markdown
---
name: 技能名称
description: 技能描述
---

# 技能名称

## 概述

技能的详细介绍

## 测试方法

1. 方法一
2. 方法二

## 工具使用

### 工具 A

使用方法...

## 最佳实践

- 实践一
- 实践二

## 示例

```
示例命令
```
```

### 4.3 技能元数据

支持 YAML front matter：

```markdown
---
name: SQL Injection Testing
description: SQL 注入漏洞测试技能
tags:
  - sqli
  - injection
  - database
difficulty: intermediate
---

# SQL Injection Testing
...
```

### 4.4 技能使用

技能创建后：
1. 可在角色中附加技能
2. AI 可使用 `list_skills` 和 `read_skill` 工具动态调用

## 5. 外部 MCP 集成

### 5.1 添加外部 MCP

在 Web 界面：Settings → External MCP

### 5.2 MCP 配置格式

**HTTP 模式：**
```json
{
  "my-mcp": {
    "transport": "http",
    "url": "http://127.0.0.1:8081/mcp",
    "description": "HTTP MCP 服务器",
    "timeout": 30
  }
}
```

**stdio 模式：**
```json
{
  "my-mcp": {
    "transport": "stdio",
    "command": "python3",
    "args": ["/path/to/mcp-server.py"],
    "description": "stdio MCP 服务器",
    "timeout": 30
  }
}
```

**SSE 模式：**
```json
{
  "my-mcp": {
    "transport": "sse",
    "url": "http://127.0.0.1:8082/sse",
    "description": "SSE MCP 服务器",
    "timeout": 30
  }
}
```

## 6. API 扩展

### 6.1 添加新接口

在 `internal/handler/` 中创建新的 handler：

```go
// internal/handler/myhandler.go
package handler

import (
    "github.com/gin-gonic/gin"
)

type MyHandler struct {
    // 依赖
}

func NewMyHandler() *MyHandler {
    return &MyHandler{}
}

func (h *MyHandler) MyEndpoint(c *gin.Context) {
    // 处理逻辑
    c.JSON(200, gin.H{"message": "ok"})
}
```

### 6.2 注册路由

在 `internal/app/app.go` 的 `setupRoutes` 函数中添加：

```go
protected.POST("/my-endpoint", myHandler.MyEndpoint)
```

### 6.3 数据库扩展

在 `internal/database/` 中添加新的表操作：

```go
func (db *DB) CreateMyTable() error {
    _, err := db.DB.Exec(`
        CREATE TABLE IF NOT EXISTS my_table (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    `)
    return err
}
```

## 7. 知识库扩展

### 7.1 添加知识条目

在 `knowledge_base/` 目录下添加 Markdown 文件：

```
knowledge_base/
├── SQL Injection/
│   └── README.md
├── XSS/
│   └── README.md
└── API Security/
    └── README.md
```

### 7.2 知识库文件格式

```markdown
# SQL 注入

## 漏洞描述

SQL 注入是一种代码注入攻击。

## 测试方法

1. 确认输入点
2. 构造测试 payload
3. 观察响应

## 防御措施

- 参数化查询
- 输入验证
- 最小权限原则
```

### 7.3 知识库索引

在 Web 界面：Knowledge → Scan & Index

或调用 API：
```bash
POST /api/knowledge/scan
POST /api/knowledge/index
```

## 8. 机器人集成

### 8.1 支持平台

- 钉钉
- 飞书
- 企业微信

### 8.2 配置方法

编辑 `config.yaml`：

```yaml
robots:
  dingtalk:
    enabled: true
    client_id: xxx
    client_secret: xxx
  lark:
    enabled: true
    app_id: xxx
    app_secret: xxx
```

详细配置请参考 [robot.md](./robot.md)。

## 9. 最佳实践

### 9.1 工具开发

- 使用 YAML 格式定义工具
- 提供清晰的参数描述
- 编写详细的说明文档

### 9.2 角色开发

- 明确角色职责范围
- 合理限制工具列表
- 附加相关技能

### 9.3 技能开发

- 使用结构化文档格式
- 提供实际示例
- 包含最佳实践

## 10. 相关文档

- [项目概述](./PROJECT_OVERVIEW.md)
- [开发指南](./DEVELOPMENT_GUIDE.md)
- [接口规范](./API_SPEC.md)
