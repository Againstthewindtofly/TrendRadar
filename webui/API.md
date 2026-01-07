# TrendRadar WebUI API 文档

## API 端点列表

### 1. 完整配置

#### 获取完整配置
```
GET /api/config
```

**响应示例：**
```json
{
  "success": true,
  "data": {
    "app": {...},
    "platforms": [...],
    "rss": {...},
    "report": {...},
    "notification": {...},
    "storage": {...},
    "advanced": {...}
  }
}
```

#### 更新完整配置
```
POST /api/config
Content-Type: application/json
```

**请求体：** 完整的配置对象

---

### 2. 应用配置 (app)

#### 获取应用配置
```
GET /api/config/app
```

**配置项：**
- `timezone`: 时区设置（如 "Asia/Shanghai"）
- `show_version_update`: 是否显示版本更新提示（boolean）

#### 更新应用配置
```
POST /api/config/app
Content-Type: application/json
```

**请求体示例：**
```json
{
  "timezone": "Asia/Shanghai",
  "show_version_update": true
}
```

---

### 3. 平台配置 (platforms)

#### 获取平台列表
```
GET /api/config/platforms
```

#### 更新平台列表
```
POST /api/config/platforms
Content-Type: application/json
```

**请求体示例：**
```json
[
  {
    "id": "toutiao",
    "name": "今日头条"
  },
  {
    "id": "baidu",
    "name": "百度热搜"
  }
]
```

---

### 4. RSS 配置 (rss)

#### 获取 RSS 配置
```
GET /api/config/rss
```

#### 更新 RSS 配置
```
POST /api/config/rss
Content-Type: application/json
```

**请求体示例：**
```json
{
  "enabled": true,
  "freshness_filter": {
    "enabled": true,
    "max_age_days": 3
  },
  "feeds": [
    {
      "id": "hacker-news",
      "name": "Hacker News",
      "url": "https://hnrss.org/frontpage",
      "enabled": true
    }
  ]
}
```

---

### 5. 报告配置 (report)

#### 获取报告配置
```
GET /api/config/report
```

#### 更新报告配置
```
POST /api/config/report
Content-Type: application/json
```

**请求体示例：**
```json
{
  "mode": "current",
  "display_mode": "keyword",
  "rank_threshold": 5,
  "sort_by_position_first": false,
  "max_news_per_keyword": 0,
  "reverse_content_order": false
}
```

**配置说明：**
- `mode`: 报告模式
  - `daily`: 当日汇总模式
  - `current`: 当前榜单模式
  - `incremental`: 增量监控模式
- `display_mode`: 显示模式
  - `keyword`: 按关键词分组
  - `platform`: 按平台分组
- `rank_threshold`: 排名高亮阈值（数字）
- `sort_by_position_first`: 是否按配置位置优先排序（boolean）
- `max_news_per_keyword`: 每个关键词最大显示数量（0=不限制）
- `reverse_content_order`: 是否反转内容顺序（boolean）

---

### 6. 通知配置 (notification)

#### 获取通知渠道配置
```
GET /api/config/notification
```

#### 更新通知渠道配置
```
POST /api/config/notification
Content-Type: application/json
```

**请求体示例：**
```json
{
  "enabled": true,
  "channels": {
    "feishu": {
      "webhook_url": "https://..."
    },
    "dingtalk": {
      "webhook_url": "https://..."
    },
    "telegram": {
      "bot_token": "your_token",
      "chat_id": "your_chat_id"
    }
  }
}
```

**注意：** 如果某个渠道的配置来自环境变量，该字段将被标记为只读，保存时不会写入文件。

---

### 7. 推送时间窗口配置 (push_window)

#### 获取推送时间窗口配置
```
GET /api/config/push-window
```

#### 更新推送时间窗口配置
```
POST /api/config/push-window
Content-Type: application/json
```

**请求体示例：**
```json
{
  "enabled": false,
  "start": "20:00",
  "end": "22:00",
  "once_per_day": true
}
```

**配置说明：**
- `enabled`: 是否启用推送时间窗口（boolean）
- `start`: 开始时间（HH:MM 格式）
- `end`: 结束时间（HH:MM 格式）
- `once_per_day`: 窗口内只推送一次（boolean）

---

### 8. 存储配置 (storage)

#### 获取存储配置
```
GET /api/config/storage
```

#### 更新存储配置
```
POST /api/config/storage
Content-Type: application/json
```

**请求体示例：**
```json
{
  "backend": "auto",
  "formats": {
    "sqlite": true,
    "txt": false,
    "html": true
  },
  "local": {
    "data_dir": "output",
    "retention_days": 0
  },
  "remote": {
    "endpoint_url": "",
    "bucket_name": "",
    "access_key_id": "",
    "secret_access_key": "",
    "region": "",
    "retention_days": 0
  },
  "pull": {
    "enabled": false,
    "days": 7
  }
}
```

**配置说明：**
- `backend`: 存储后端（auto/local/remote）
- `formats`: 数据格式选项
- `local`: 本地存储配置
- `remote`: 远程存储配置（S3 兼容）
- `pull`: 数据拉取配置

---

### 9. 高级配置 (advanced)

#### 获取高级配置
```
GET /api/config/advanced
```

#### 更新高级配置
```
POST /api/config/advanced
Content-Type: application/json
```

**请求体示例：**
```json
{
  "version_check_url": "https://...",
  "crawler": {
    "enabled": true,
    "request_interval": 1000,
    "use_proxy": false,
    "default_proxy": "http://127.0.0.1:10801"
  },
  "rss": {
    "request_interval": 2000,
    "timeout": 15,
    "use_proxy": false,
    "proxy_url": "",
    "notification_enabled": true
  },
  "weight": {
    "rank": 0.6,
    "frequency": 0.3,
    "hotness": 0.1
  },
  "max_accounts_per_channel": 3,
  "batch_size": {
    "default": 4000,
    "dingtalk": 20000,
    "feishu": 30000,
    "bark": 4000,
    "slack": 4000,
    "serverchan": 4000
  },
  "batch_send_interval": 3,
  "feishu_message_separator": "━━━━━━━━━━━━━━━━━━━"
}
```

---

### 10. 关键词配置

#### 获取关键词配置
```
GET /api/keywords
```

#### 更新关键词配置
```
POST /api/keywords
Content-Type: application/json
```

**请求体示例：**
```json
{
  "content": "关键词1\n关键词2\n关键词3"
}
```

---

### 11. 环境变量状态

#### 获取环境变量配置状态
```
GET /api/config/env-status
```

**响应示例：**
```json
{
  "success": true,
  "data": {
    "notification": {
      "channels": {
        "feishu": {
          "webhook_url": true
        },
        "telegram": {
          "bot_token": true,
          "chat_id": false
        }
      }
    }
  }
}
```

**说明：** 返回值为 `true` 的字段表示该配置来自环境变量，前端应将其设为只读。

---

### 12. 其他功能

#### 测试通知渠道
```
POST /api/test-notification
Content-Type: application/json
```

**请求体：**
```json
{
  "channel": "feishu",
  "config": {...}
}
```

#### 热重载配置
```
POST /api/reload
```

#### 重启容器
```
POST /api/restart
```

---

## 通用响应格式

### 成功响应
```json
{
  "success": true,
  "data": {...},
  "message": "操作成功"
}
```

### 失败响应
```json
{
  "success": false,
  "message": "错误信息"
}
```

---

## 环境变量优先级

当配置项同时存在于环境变量和配置文件中时：
1. **读取时**：环境变量优先级更高，会覆盖文件配置
2. **保存时**：只保存文件配置，不会覆盖环境变量控制的字段
3. **标记**：来自环境变量的配置会添加 `_from_env: true` 标记

使用 `/api/config/env-status` 可以查询哪些配置来自环境变量。

---

## 使用示例

### 示例 1: 更新报告模式

```bash
curl -X POST http://localhost:5000/api/config/report \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "incremental",
    "display_mode": "keyword",
    "rank_threshold": 10
  }'
```

### 示例 2: 设置推送时间窗口

```bash
curl -X POST http://localhost:5000/api/config/push-window \
  -H "Content-Type: application/json" \
  -d '{
    "enabled": true,
    "start": "08:00",
    "end": "18:00",
    "once_per_day": false
  }'
```

### 示例 3: 更新 RSS 订阅源

```bash
curl -X POST http://localhost:5000/api/config/rss \
  -H "Content-Type: application/json" \
  -d '{
    "enabled": true,
    "feeds": [
      {
        "id": "custom-feed",
        "name": "我的订阅源",
        "url": "https://example.com/feed.xml",
        "enabled": true
      }
    ]
  }'
```
