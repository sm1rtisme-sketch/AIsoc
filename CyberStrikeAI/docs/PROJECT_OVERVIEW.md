# CyberStrikeAI 项目概述

## 1. 项目简介

CyberStrikeAI 是一个**AI 原生安全测试平台**，采用 Go 语言开发。该平台集成了 100+ 安全工具、智能编排引擎、基于角色的测试框架、Skills 技能系统以及完整的生命周期管理能力。通过原生 MCP 协议和 AI 智能体，它能够实现从对话式命令到漏洞发现、攻击链分析、知识检索和结果可视化的端到端自动化，为安全团队提供可审计、可追溯和可协作的测试环境。

## 2. 核心特性

### 2.1 AI 决策引擎
- 支持 OpenAI 兼容模型（GPT、Claude、DeepSeek 等）
- AI 智能体能够自主分析目标、选择工具、执行测试

### 2.2 MCP 协议支持
- 原生 MCP 实现，支持 HTTP、stdio、SSE 三种传输方式
- 支持外部 MCP 联邦，可连接第三方 MCP 服务器

### 2.3 安全工具生态
- 预置 100+ 工具配方，覆盖完整攻击链
- 基于 YAML 的扩展系统，便于自定义工具

### 2.4 知识库系统
- 向量搜索 + 混合检索
- 自动索引 Markdown 文件
- 支持安全专业知识检索

### 2.5 角色与技能系统
- 12+ 预定义安全测试角色
- 20+ 预定义安全测试技能
- 支持自定义角色和技能

### 2.6 漏洞管理
- 完整的 CRUD 操作
- 严重程度跟踪
- 状态工作流
- 统计与导出

### 2.7 机器人集成
- 支持钉钉、飞书、企业微信
- 移动端随时随地使用

## 3. 技术架构

### 3.1 技术栈
- **后端**: Go 1.24+
- **Web 框架**: Gin
- **数据库**: SQLite
- **前端**: Vue.js + HTML/CSS
- **AI 集成**: OpenAI 兼容 API

### 3.2 核心模块

```
CyberStrikeAI/
├── cmd/                    # 入口程序
│   ├── server/             # 主服务器
│   ├── mcp-stdio/          # MCP stdio 模式
│   └── test-*/             # 测试工具
├── internal/               # 内部包
│   ├── agent/              # AI 智能体
│   ├── mcp/                # MCP 协议实现
│   ├── handler/            # HTTP 处理器
│   ├── security/           # 安全工具执行器
│   ├── knowledge/           # 知识库系统
│   ├── skills/              # 技能系统
│   ├── database/            # 数据库操作
│   └── config/              # 配置管理
├── web/                    # 前端资源
├── tools/                  # 工具配置 (100+)
├── roles/                  # 角色配置 (12+)
├── skills/                 # 技能配置 (20+)
└── docs/                   # 文档
```

## 4. 预置工具分类

| 类别 | 工具 |
|------|------|
| 网络扫描 | nmap, masscan, rustscan, arp-scan |
| Web 扫描 | sqlmap, nikto, dirb, gobuster, feroxbuster, ffuf, httpx |
| 漏洞扫描 | nuclei, wpscan, wafw00f, dalfox, xsser |
| 子域名枚举 | subfinder, amass, findomain, dnsenum, fierce |
| API 安全 | graphql-scanner, arjun, api-fuzzer |
| 容器安全 | trivy, clair, docker-bench-security |
| 云安全 | prowler, scout-suite, cloudmapper |
| 漏洞利用 | metasploit, msfvenom, pwntools |
| 密码破解 | hashcat, john, hashpump |
| 取证分析 | volatility, foremost, steghide, exiftool |
| 后渗透 | linpeas, winpeas, mimikatz, bloodhound, impacket |

## 5. 预置角色

| 角色 | 描述 |
|------|------|
| 渗透测试 | 专业渗透测试专家 |
| CTF | CTF 竞赛专用 |
| Web 应用扫描 | Web 应用安全测试 |
| API 安全测试 | API 接口安全测试 |
| 信息收集 | 目标信息收集 |
| 综合漏洞扫描 | 全面漏洞扫描 |
| 云安全审计 | 云环境安全评估 |
| 容器安全 | 容器安全检测 |
| 二进制分析 | 二进制文件分析 |
| 后渗透测试 | 权限维持与横向移动 |
| 数字取证 | 数字取证分析 |
| Web 框架测试 | Web 框架专项测试 |

## 6. 预置技能

- SQL 注入测试
- XSS 测试
- API 安全测试
- 云安全测试
- 容器安全测试
- 等等 20+ 技能

## 7. 适用场景

1. **渗透测试辅助**: AI 驱动的自动化渗透测试
2. **CTF 竞赛**: CTF 挑战辅助
3. **漏洞扫描**: Web 应用、API、容器、云环境漏洞扫描
4. **安全研究**: 安全知识检索与测试
5. **红蓝对抗**: 攻击链分析与复现
6. **安全培训**: 安全测试教学与演示

## 8. 部署要求

- Go 1.21+
- Python 3.10+ (部分工具需要)
- 支持 Linux/macOS/Windows

## 9. 许可证

请参考项目根目录的 LICENSE 文件。
