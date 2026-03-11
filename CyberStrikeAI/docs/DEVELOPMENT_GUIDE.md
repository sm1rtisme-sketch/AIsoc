# CyberStrikeAI 开发指南

## 1. 环境准备

### 1.1 依赖要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Go | 1.21+ | 后端语言 |
| Python | 3.10+ | 部分工具需要 |
| SQLite | - | 内置，无需单独安装 |

### 1.2 开发环境搭建

```bash
# 克隆项目
git clone https://github.com/Ed1s0nZ/CyberStrikeAI.git
cd CyberStrikeAI

# 运行启动脚本（自动安装依赖并启动）
chmod +x run.sh && ./run.sh

# 或手动启动
go mod download
go build -o cyberstrike-ai cmd/server/main.go
./cyberstrike-ai
```

### 1.3 配置修改

编辑 `config.yaml` 文件：

```yaml
# 必填配置
openai:
  base_url: https://api.deepseek.com/v1
  api_key: sk-your-key
  model: deepseek-chat

# 可选配置
server:
  host: 0.0.0.0
  port: 8080

auth:
  password: your-password
  session_duration_hours: 12
```

## 2. 项目结构

### 2.1 目录说明

```
CyberStrikeAI/
├── cmd/                    # 入口程序
│   ├── server/main.go      # 主服务器入口
│   ├── mcp-stdio/main.go   # MCP stdio 模式入口
│   └── test-*/             # 测试工具
├── internal/               # 内部包（核心逻辑）
│   ├── agent/              # AI 智能体实现
│   ├── mcp/                # MCP 协议核心
│   │   ├── server.go       # MCP 服务器
│   │   └── builtin/        # 内置工具
│   ├── handler/            # HTTP 请求处理
│   ├── security/           # 安全工具执行器
│   ├── knowledge/          # 知识库系统
│   ├── skills/            # 技能系统
│   ├── database/           # 数据库操作
│   ├── config/             # 配置管理
│   ├── logger/             # 日志系统
│   ├── storage/            # 结果存储
│   ├── openai/             # OpenAI API 客户端
│   ├── robot/              # 机器人集成
│   └── attackchain/        # 攻击链分析
├── web/                    # 前端资源
│   ├── static/             # 静态文件
│   └── templates/          # HTML 模板
├── tools/                 # 工具配置文件
├── roles/                 # 角色配置文件
├── skills/                # 技能配置文件
├── knowledge_base/        # 知识库内容
├── data/                  # 数据存储目录
├── config.yaml            # 主配置文件
└── run.sh                 # 启动脚本
```

## 3. 核心模块开发

### 3.1 Agent 模块

位置: `internal/agent/`

Agent 是 AI 智能体的核心实现，负责：
- 接收用户请求
- 决策工具调用
- 执行安全工具
- 返回结果

关键文件：
- `agent.go`: Agent 主逻辑
- `executor.go`: 工具执行器

### 3.2 MCP 模块

位置: `internal/mcp/`

MCP 协议实现，负责：
- 工具注册
- 工具调用
- 结果返回

关键文件：
- `server.go`: MCP 服务器
- `builtin/`: 内置工具定义

### 3.3 Handler 模块

位置: `internal/handler/`

HTTP API 处理器：

| 文件 | 功能 |
|------|------|
| agent.go | AI 对话接口 |
| auth.go | 认证接口 |
| vulnerability.go | 漏洞管理 |
| role.go | 角色管理 |
| skills.go | 技能管理 |
| knowledge.go | 知识库管理 |
| config.go | 配置管理 |
| monitor.go | 监控接口 |
| batch_task_manager.go | 批量任务 |

### 3.4 数据库模块

位置: `internal/database/`

使用 SQLite 存储：
- 对话历史
- 漏洞记录
- 执行日志
- 知识库索引

数据库表：
- conversations: 对话
- messages: 消息
- vulnerabilities: 漏洞
- execution_logs: 执行日志
- knowledge_items: 知识库项
- skill_stats: 技能统计

## 4. 调试与测试

### 4.1 本地调试

```bash
# 启动调试服务器
go run cmd/server/main.go

# 查看日志
# config.yaml 中设置 log.level: debug
```

### 4.2 API 测试

访问 Web 界面：`http://localhost:8080`

或使用 API 文档：`http://localhost:8080/api-docs`

### 4.3 MCP stdio 模式测试

```bash
# 编译 MCP stdio 客户端
go build -o cyberstrike-ai-mcp cmd/mcp-stdio/main.go

# 配置到 Cursor
# Settings → Tools & MCP → Add Custom MCP
```

## 5. 构建与部署

### 5.1 构建

```bash
# 构建主服务器
go build -o cyberstrike-ai cmd/server/main.go

# 构建 MCP stdio 客户端
go build -o cyberstrike-ai-mcp cmd/mcp-stdio/main.go
```

### 5.2 部署

```bash
# 复制可执行文件和配置
cp cyberstrike-ai /usr/local/bin/
cp config.yaml /etc/cyberstrike-ai/

# 创建数据目录
mkdir -p /var/lib/cyberstrike-ai/data
```

## 6. 常见问题

### 6.1 编译问题

Q: 编译失败，提示依赖缺失
A: 运行 `go mod download` 或 `go mod tidy`

### 6.2 运行问题

Q: 启动失败，提示端口占用
A: 修改 `config.yaml` 中的 `server.port`

### 6.3 API 问题

Q: AI 不工作
A: 检查 `config.yaml` 中的 `openai` 配置是否正确

## 7. 相关文档

- [项目概述](./PROJECT_OVERVIEW.md)
- [二次开发指南](./EXTENSION_GUIDE.md)
- [接口规范](./API_SPEC.md)
- [机器人配置](./robot.md)
