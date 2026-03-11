# CyberStrikeAI 接口规范

## 1. 认证

### 1.1 登录

**请求**
```
POST /api/auth/login
Content-Type: application/json

{
  "password": "your-password"
}
```

**响应**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2024-01-01T12:00:00Z"
}
```

### 1.2 登出

**请求**
```
POST /api/auth/logout
Authorization: Bearer <token>
```

**响应**
```json
{
  "success": true
}
```

### 1.3 验证 Token

**请求**
```
GET /api/auth/validate
Authorization: Bearer <token>
```

**响应**
```json
{
  "valid": true
}
```

### 1.4 修改密码

**请求**
```
POST /api/auth/change-password
Authorization: Bearer <token>
Content-Type: application/json

{
  "old_password": "old-password",
  "new_password": "new-password"
}
```

**响应**
```json
{
  "success": true
}
```

## 2. 对话管理

### 2.1 创建对话

**请求**
```
POST /api/conversations
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Web应用安全测试"
}
```

**响应**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Web应用安全测试",
  "createdAt": "2024-01-01T00:00:00Z",
  "updatedAt": "2024-01-01T00:00:00Z"
}
```

### 2.2 获取对话列表

**请求**
```
GET /api/conversations
Authorization: Bearer <token>
```

**响应**
```json
{
  "conversations": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Web应用安全测试",
      "createdAt": "2024-01-01T00:00:00Z",
      "updatedAt": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### 2.3 获取对话详情

**请求**
```
GET /api/conversations/:id
Authorization: Bearer <token>
```

**响应**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Web应用安全测试",
  "status": "active",
  "createdAt": "2024-01-01T00:00:00Z",
  "updatedAt": "2024-01-01T00:00:00Z",
  "messages": [...]
}
```

### 2.4 AI 对话（非流式）

**请求**
```
POST /api/agent-loop
Authorization: Bearer <token>
Content-Type: application/json

{
  "message": "扫描 192.168.1.1 的开放端口",
  "conversationId": "550e8400-e29b-41d4-a716-446655440000",
  "role": ""
}
```

**响应**
```json
{
  "success": true,
  "response": "AI 响应内容",
  "conversationId": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 2.5 AI 对话（流式）

**请求**
```
POST /api/agent-loop/stream
Authorization: Bearer <token>
Content-Type: application/json

{
  "message": "扫描 192.168.1.1 的开放端口",
  "conversationId": "550e8400-e29b-41d4-a716-446655440000"
}
```

**响应**
SSE 流式响应

## 3. 漏洞管理

### 3.1 创建漏洞

**请求**
```
POST /api/vulnerabilities
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "SQL 注入漏洞",
  "description": "参数 id 存在 SQL 注入",
  "severity": "high",
  "vulnerability_type": "SQL Injection",
  "target": "https://example.com/page?id=1",
  "status": "open"
}
```

**响应**
```json
{
  "id": "vuln-001",
  "title": "SQL 注入漏洞",
  "severity": "high",
  "status": "open",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

### 3.2 获取漏洞列表

**请求**
```
GET /api/vulnerabilities?severity=high&status=open
Authorization: Bearer <token>
```

**响应**
```json
{
  "vulnerabilities": [
    {
      "id": "vuln-001",
      "title": "SQL 注入漏洞",
      "severity": "high",
      "status": "open",
      "createdAt": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1
}
```

### 3.3 获取漏洞统计

**请求**
```
GET /api/vulnerabilities/stats
Authorization: Bearer <token>
```

**响应**
```json
{
  "total": 10,
  "critical": 2,
  "high": 3,
  "medium": 3,
  "low": 1,
  "info": 1,
  "by_status": {
    "open": 5,
    "confirmed": 3,
    "fixed": 1,
    "false_positive": 1
  }
}
```

### 3.4 更新漏洞

**请求**
```
PUT /api/vulnerabilities/:id
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "confirmed",
  "severity": "critical"
}
```

### 3.5 删除漏洞

**请求**
```
DELETE /api/vulnerabilities/:id
Authorization: Bearer <token>
```

## 4. 角色管理

### 4.1 获取角色列表

**请求**
```
GET /api/roles
Authorization: Bearer <token>
```

**响应**
```json
{
  "roles": [
    {
      "name": "渗透测试",
      "description": "专业渗透测试专家",
      "icon": "🎯",
      "tools": ["nmap", "sqlmap", ...],
      "skills": ["sql-injection-testing", ...],
      "enabled": true
    }
  ]
}
```

### 4.2 获取单个角色

**请求**
```
GET /api/roles/:name
Authorization: Bearer <token>
```

### 4.3 创建角色

**请求**
```
POST /api/roles
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "自定义角色",
  "description": "描述",
  "user_prompt": "系统提示词",
  "icon": "🔐",
  "tools": ["nmap", "httpx"],
  "skills": ["api-security-testing"],
  "enabled": true
}
```

### 4.4 更新角色

**请求**
```
PUT /api/roles/:name
Authorization: Bearer <token>
Content-Type: application/json

{
  "description": "新描述"
}
```

### 4.5 删除角色

**请求**
```
DELETE /api/roles/:name
Authorization: Bearer <token>
```

## 5. 技能管理

### 5.1 获取技能列表

**请求**
```
GET /api/skills
Authorization: Bearer <token>
```

**响应**
```json
{
  "skills": [
    {
      "name": "sql-injection-testing",
      "description": "SQL 注入测试技能",
      "category": "Web Security",
      "usage_count": 10
    }
  ]
}
```

### 5.2 获取单个技能

**请求**
```
GET /api/skills/:name
Authorization: Bearer <token>
```

**响应**
```json
{
  "name": "sql-injection-testing",
  "description": "SQL 注入测试技能",
  "content": "# SQL Injection Testing\n\n## 概述\n...",
  "usage_count": 10
}
```

### 5.3 获取技能统计

**请求**
```
GET /api/skills/stats
Authorization: Bearer <token>
```

## 6. 知识库管理

### 6.1 扫描知识库

**请求**
```
POST /api/knowledge/scan
Authorization: Bearer <token>
```

**响应**
```json
{
  "success": true,
  "scanned": 50,
  "added": 5,
  "updated": 3
}
```

### 6.2 重建索引

**请求**
```
POST /api/knowledge/index
Authorization: Bearer <token>
```

### 6.3 搜索知识库

**请求**
```
POST /api/knowledge/search
Authorization: Bearer <token>
Content-Type: application/json

{
  "query": "SQL 注入",
  "top_k": 5
}
```

**响应**
```json
{
  "results": [
    {
      "id": "kb-001",
      "title": "SQL 注入",
      "content": "...",
      "score": 0.95,
      "category": "Web Security"
    }
  ]
}
```

### 6.4 获取索引状态

**请求**
```
GET /api/knowledge/index-status
Authorization: Bearer <token>
```

**响应**
```json
{
  "enabled": true,
  "total_items": 100,
  "indexed_items": 100,
  "progress_percent": 100,
  "is_complete": true
}
```

## 7. 批量任务管理

### 7.1 创建任务队列

**请求**
```
POST /api/batch-tasks
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "批量扫描任务",
  "description": "描述"
}
```

**响应**
```json
{
  "id": "queue-001",
  "name": "批量扫描任务",
  "status": "pending",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

### 7.2 添加任务

**请求**
```
POST /api/batch-tasks/:queueId/tasks
Authorization: Bearer <token>
Content-Type: application/json

{
  "message": "扫描 192.168.1.1"
}
```

### 7.3 启动队列

**请求**
```
POST /api/batch-tasks/:queueId/start
Authorization: Bearer <token>
```

### 7.4 暂停队列

**请求**
```
POST /api/batch-tasks/:queueId/pause
Authorization: Bearer <token>
```

### 7.5 获取队列状态

**请求**
```
GET /api/batch-tasks/:queueId
Authorization: Bearer <token>
```

**响应**
```json
{
  "id": "queue-001",
  "name": "批量扫描任务",
  "status": "running",
  "progress": {
    "total": 10,
    "completed": 3,
    "running": 1,
    "pending": 6
  },
  "tasks": [...]
}
```

## 8. 监控管理

### 8.1 获取执行列表

**请求**
```
GET /api/monitor
Authorization: Bearer <token>
```

**响应**
```json
{
  "executions": [
    {
      "id": "exec-001",
      "tool": "nmap",
      "status": "running",
      "startedAt": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### 8.2 获取执行详情

**请求**
```
GET /api/monitor/execution/:id
Authorization: Bearer <token>
```

### 8.3 删除执行记录

**请求**
```
DELETE /api/monitor/execution/:id
Authorization: Bearer <token>
```

### 8.4 获取统计信息

**请求**
```
GET /api/monitor/stats
Authorization: Bearer <token>
```

## 9. 配置管理

### 9.1 获取配置

**请求**
```
GET /api/config
Authorization: Bearer <token>
```

### 9.2 更新配置

**请求**
```
PUT /api/config
Authorization: Bearer <token>
Content-Type: application/json

{
  "openai": {
    "api_key": "new-key"
  }
}
```

### 9.3 应用配置

**请求**
```
POST /api/config/apply
Authorization: Bearer <token>
```

## 10. 外部 MCP 管理

### 10.1 获取外部 MCP 列表

**请求**
```
GET /api/external-mcp
Authorization: Bearer <token>
```

### 10.2 添加外部 MCP

**请求**
```
PUT /api/external-mcp/:name
Authorization: Bearer <token>
Content-Type: application/json

{
  "transport": "http",
  "url": "http://127.0.0.1:8081/mcp",
  "description": "描述"
}
```

### 10.3 启动外部 MCP

**请求**
```
POST /api/external-mcp/:name/start
Authorization: Bearer <token>
```

### 10.4 停止外部 MCP

**请求**
```
POST /api/external-mcp/:name/stop
Authorization: Bearer <token>
```

## 11. 错误响应格式

所有 API 错误响应遵循以下格式：

```json
{
  "error": "错误描述",
  "code": "ERROR_CODE"
}
```

常见错误码：

| 错误码 | 说明 |
|--------|------|
| UNAUTHORIZED | 未认证 |
| FORBIDDEN | 无权限 |
| NOT_FOUND | 资源不存在 |
| INVALID_PARAMS | 参数错误 |
| INTERNAL_ERROR | 服务器内部错误 |

## 12. 速率限制

- 无认证: 60 请求/分钟
- 有认证: 120 请求/分钟

## 13. 相关文档

- [项目概述](./PROJECT_OVERVIEW.md)
- [开发指南](./DEVELOPMENT_GUIDE.md)
- [二次开发指南](./EXTENSION_GUIDE.md)
