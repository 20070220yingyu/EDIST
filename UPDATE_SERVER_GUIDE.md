# 自动更新服务器配置指南

## 📍 更新地址

当前配置: `https://347735.xyz/genxin/`

---

## 📋 服务器端返回格式

你的服务器需要返回 **JSON格式** 的数据。支持以下3种格式（任选其一）：

### 格式1：推荐格式（自定义标准）
```json
{
    "version": "3.3",
    "download": "https://347735.xyz/genxin/X反极域v3.3.zip",
    "changelog": "• 添加自动更新功能\n• 优化UI界面\n• 修复已知bug"
}
```

### 格式2：GitHub API兼容格式
```json
{
    "tag_name": "v3.3",
    "zipball_url": "https://347735.xyz/genxin/v3.3.zip",
    "body": "## v3.3 更新内容\n\n- 新功能1\n- 新功能2"
}
```

### 格式3：简化格式
```json
{
    "latest": "3.3",
    "url": "https://347735.xyz/genxin/download?v=3.3",
    "notes": "版本更新说明"
}
```

---

## 🔧 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `version` | string | ✅ | 最新版本号（如 `3.3`, `4.0.1`） |
| `latest` | string | ✅ | 同上，备选字段名 |
| `tag_name` | string | ✅ | GitHub风格，支持带`v`前缀 |
| `download` | string | ✅ | 下载文件的完整URL |
| `url` | string | ✅ | 下载URL（备选字段名） |
| `download_url` | string | ❌ | 下载URL（备选字段名） |
| `file` | string | ❌ | 文件路径（相对路径会自动补全） |
| `changelog` | string | ❌ | 更新日志/说明 |
| `body` | string | ❌ | 更新日志（GitHub风格） |
| `notes` | string | ❌ | 备注信息 |

---

## 📝 示例配置

### 完整示例 (推荐)
```json
{
    "version": "3.3.0",
    "download": "https://347735.xyz/genxin/files/X反极域v3.3.0.zip",
    "changelog": "🎉 v3.3.0 重大更新\n\n✨ 新功能:\n• 自动更新系统\n• 多语言支持\n• 主题定制\n\n🐛 修复:\n• 修复UI布局问题\n• 优化性能\n\n⚠️ 注意:\n• 需要Python 3.x环境",
    "release_date": "2026-04-30",
    "min_version": "3.0",
    "size": "15.2MB"
}
```

### 最简示例
```json
{
    "version": "3.3",
    "download": "X反极域v3.3.zip"
}
```
> ⚠️ 相对路径会自动补全为: `https://347735.xyz/genxin/X反极域v3.3.zip`

---

## 🌐 服务器端实现示例

### PHP示例
```php
<?php
// update.php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

$latest_version = "3.3";
$download_url = "https://347735.xyz/genxin/downloads/X反极域_v{$latest_version}.zip";

$response = [
    'version' => $latest_version,
    'download' => $download_url,
    'changelog' => "• 新功能A\n• 新功能B\n• Bug修复C"
];

echo json_encode($response, JSON_UNESCAPED_UNICODE);
?>
```

### Python Flask示例
```python
from flask import jsonify, request
import json

@app.route('/genxin/', methods=['GET'])
def check_update():
    latest = {
        'version': '3.3',
        'download': 'https://347735.xyz/genxin/files/update.zip',
        'changelog': '• Auto-update feature\n• UI improvements'
    }
    
    # 可选：根据客户端版本号返回不同结果
    client_version = request.args.get('v', '0')
    if client_version < '3.3':
        return jsonify(latest)
    else:
        return jsonify({'version': client_version, 'changelog': '已是最新'})
```

### Node.js Express示例
```javascript
const express = require('express');
const app = express();

app.get('/genxin/', (req, res) => {
    res.json({
        version: '3.3',
        download: 'https://347735.xyz/genxin/releases/latest.zip',
        changelog: '• Added auto-update\n• Performance boost'
    });
});

app.listen(3000);
```

### Nginx静态JSON
```nginx
server {
    listen 443 ssl;
    server_name 347735.xyz;
    
    location /genxin/ {
        alias /var/www/genxin/;
        default_type application/json;
        
        # 允许跨域
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods 'GET';
    }
}
```

文件位置: `/var/www/genxin/index.json`

---

## 🔒 安全建议

### 1. HTTPS强制使用
```nginx
# 强制HTTPS
if ($scheme != "https") {
    return 301 https://$host$request_uri;
}
```

### 2. 请求频率限制
```php
// PHP示例：基于IP限流
$ip = $_SERVER['REMOTE_ADDR'];
$cache_file = "rate_limit_{$ip}";
if (file_exists($cache_file) && time() - filemtime($cache_file) < 60) {
    header('HTTP/1.1 429 Too Many Requests');
    exit('请求过于频繁，请稍后再试');
}
touch($cache_file);
```

### 3. 版本验证签名（高级）
```json
{
    "version": "3.3",
    "download": "...",
    "signature": "sha256:abc123...",
    "checksum": "md5:def456..."
}
```

---

## 🧪 测试方法

### 1. 直接访问URL测试
```bash
curl -H "User-Agent: X反极域/3.2" \
     -H "Accept: application/json" \
     https://347735.xyz/genxin/
```

预期返回：
```json
{"version":"3.3","download":"...","changelog":"..."}
```

### 2. 在软件中测试
1. 运行 X反极域v3.2.py
2. 点击菜单栏 → `🔄 Check for Updates / 检查更新`
3. 观察是否正确解析版本信息

### 3. 模拟旧版本测试
修改 [config.json](config.json) 中的版本号为旧版本：
```json
{
    "app": {
        "version": "1.0"  // 故意设为旧版本
    }
}
```
重启程序，应该能检测到更新。

---

## 📊 客户端请求头信息

每次检查更新时，客户端会发送：

```http
GET /genxin/ HTTP/1.1
Host: 347735.xyz
User-Agent: X反极域/3.2
Accept: application/json
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
```

你可以根据 `User-Agent` 识别客户端版本。

---

## ⚙️ 客户端配置修改

### 方式1: 编辑 config.json（推荐）
```json
{
    "features": {
        "update_server_url": "https://your-server.com/path/",
        "auto_update": true,
        "check_on_startup": true
    }
}
```

### 方式2: 硬编码（不推荐）
编辑 [X反极域v3.2.py](X反极域v3.2.py) 第1108行:
```python
self.update_url = "https://your-new-url.com/"
```

---

## 🎯 最佳实践

### ✅ 推荐做法
1. 使用 **HTTPS** 加密传输
2. 返回完整的 **changelog** 字段
3. 提供 **文件大小** 信息
4. 设置合理的 **缓存策略**
5. 实现 **请求频率限制**
6. 定期清理旧版本的下载文件

### ❌ 避免做法
1. 不要返回过大的响应（<10KB）
2. 不要在URL中包含敏感信息
3. 不要忽略错误处理
4. 不要忘记设置 CORS 头

---

## 🚀 快速部署清单

- [ ] 创建 `/genxin/` 路由或目录
- [ ] 准备 JSON 响应文件
- [ ] 上传最新版本的 ZIP 文件
- [ ] 配置 HTTPS 证书
- [ ] 测试 JSON 访问是否正常
- [ ] 测试文件下载链接是否有效
- [ ] 在软件中验证更新流程
- [ ] 配置日志监控（可选）

---

## 📞 技术支持

如果遇到问题：

1. **检查网络连通性**: `curl -I https://347735.xyz/genxin/`
2. **查看JSON格式**: 使用浏览器插件格式化JSON
3. **检查CORS设置**: 确保允许跨域请求
4. **查看服务器日志**: 确认是否有错误记录
5. **联系作者**: nmmmyl@ying.xyz

---

**最后更新**: 2026-04-30  
**适用版本**: X反极域 v3.2+
