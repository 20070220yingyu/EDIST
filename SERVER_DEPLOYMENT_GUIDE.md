# 服务器部署指南 - EDIST 自动更新系统

## 📁 目录结构要求

```
你的网站根目录 (例如: /var/www/html 或 C:\xampp\htdocs)
└── genxin/                    ← 项目根目录
    ├── latest.php             ← 版本检查 API (必须)
    └── downloads/             ← 更新包存放目录 (必须创建)
        ├── EDIST-v3.3.zip     ← 更新包 (示例)
        ├── EDIST-v3.3.zip.sha256 ← 校验文件 (可选但推荐)
        └── EDIST-v3.4.zip     ← 新版本...
```

## 🔧 部署步骤

### Step 1: 创建目录

**Linux 服务器:**
```bash
cd /var/www/html  # 或你的网站根目录
mkdir -p genxin/downloads
chmod 755 genxin/downloads
chown www-data:www-data genxin/downloads  # Apache/Nginx 用户
```

**Windows 服务器 (XAMPP/WAMP):**
```bash
cd C:\xampp\htdocs
mkdir genxin\downloads
```

### Step 2: 上传文件

1. **上传 `latest.php` 到 `genxin/` 目录**

2. **上传更新包到 `genxin/downloads/` 目录**
   - 文件名格式: `EDIST-vX.Y.Z.zip`
   - 示例: `EDIST-v3.3.zip`

3. **(可选) 生成 SHA256 校验值**
   
   Linux:
   ```bash
   cd genxin/downloads
   sha256sum EDIST-v3.3.zip > EDIST-v3.3.zip.sha256
   ```
   
   Windows PowerShell:
   ```powershell
   cd genxin/downloads
   Get-FileHash EDIST-v3.3.zip -Algorithm SHA256 | Select-Object -ExpandProperty Hash | Out-File -Encoding utf8 EDIST-v3.3.zip.sha256
   ```

### Step 3: 配置 Web 服务器

#### Apache (.htaccess)

在 `genxin/` 目录创建 `.htaccess`:
```apache
<IfModule mod_rewrite.c>
    RewriteEngine On
    
    # 允许访问 downloads 目录
    RewriteCond %{REQUEST_URI} ^/downloads/ [NC]
    RewriteRule . - [L]
    
    # 其他请求转发到 index.php (如果需要)
</IfModule>

# 设置 downloads 目录的 MIME 类型
<Directory "downloads">
    ForceType application/zip
</Directory>
```

#### Nginx

在站点配置中添加:
```nginx
location /genxin/ {
    alias /var/www/html/genxin/;
    
    # 允许访问下载文件
    location /genxin/downloads/ {
        add_header Content-Disposition 'attachment';
        
        # 可选: 限制下载速度
        # limit_rate 512k;
    }
}
```

### Step 4: 测试 API 是否工作

在浏览器或命令行中访问:

```bash
# 应该返回 JSON 格式的版本信息
curl https://347735.xyz/genxin/latest.php
```

**期望响应:**
```json
{
    "success": true,
    "version": "3.3",
    "download_url": "https://347735.xyz/genxin/downloads/EDIST-v3.3.zip",
    "file_hash": "abc123...",
    "filename": "EDIST-v3.3.zip",
    "release_notes": "",
    "server_time": "2026-05-02 02:00:00"
}
```

**错误响应示例:**
```json
{
    "success": false,
    "error": "更新目录不存在",
    "debug": {
        "configured_path": "/genxin/downloads/",
        "current_dir": "/var/www/html/genxin",
        "suggestion": "请在服务器上创建该目录"
    }
}
```

## ⚙️ 常见问题排查

### Q1: 显示"更新目录不存在"

**原因**: `$dir` 路径配置不正确

**解决**: 
1. 打开 `latest.php`
2. 找到第 23 行: `$dir = __DIR__ . '/downloads/';`
3. 根据实际情况修改为绝对路径:
   ```php
   // Linux 示例
   $dir = '/var/www/html/genxin/downloads/';
   
   // Windows XAMPP 示例
   $dir = 'C:/xampp/htdocs/genxin/downloads/';
   ```

### Q2: 显示"未找到有效版本文件"

**原因**: downloads 目录中没有符合命名规范的 zip 文件

**解决**:
1. 确保文件名包含版本号: `EDIST-v3.3.zip` 或 `v3.3.zip`
2. 文件必须是 `.zip` 格式
3. 确保文件权限可读 (`chmod 644`)

### Q3: 可以检测到版本但下载失败 (404)

**原因**: 生成的下载 URL 不正确

**解决**:
1. 检查 `$web_path` 变量（第 144 行）
2. 确保 Web 服务器配置了 `/downloads/` 的静态文件服务
3. 在浏览器中直接测试下载 URL 是否可访问

### Q4: 权限问题 (Permission Denied)

**解决**:
```bash
# 设置正确权限
chmod -R 755 /path/to/genxin/
chown -R www-data:www-data /path/to/genxin/

# 检查 SELinux (如果启用)
setsebool -P httpd_read_user_content 1
```

## 🧪 本地测试方案 (无需真实服务器)

如果暂时没有服务器，可以使用以下方法本地测试:

### 方法 A: 使用 Python HTTP 服务器

```bash
# 1. 创建临时目录结构
mkdir -p test_server/genxin/downloads

# 2. 复制文件
cp fwq/latest.php test_server/genxin/
cp build/EDIST_v3.2/EDIST.exe test_server/genxin/downloads/EDIST-v3.3.zip

# 3. 启动 HTTP 服务器 (端口 8080)
cd test_server
python -m http.server 8080

# 4. 修改客户端配置指向本地
# config.json 中设置:
# "update_server_url": "http://localhost:8080/genxin/latest.php"
```

### 方法 B: 使用 PHP 内置服务器

```bash
cd test_server/genxin
php -S localhost:8080
```

然后访问: `http://localhost:8080/latest.php`

---

## 📝 安全建议

1. **不要在生产环境开启 debug_mode** - 将第 30 行改为 `$debug_mode = false;`
2. **限制访问频率** - 防止恶意刷接口
3. **使用 HTTPS** - 保护传输安全
4. **验证下载请求** - 添加 token 或签名验证
5. **定期清理旧版本** - 避免磁盘空间不足

---

## ✅ 部署清单

- [ ] 创建 `genxin/` 和 `genxin/downloads/` 目录
- [ ] 上传 `latest.php` 到 `genxin/`
- [ ] 上传至少一个更新包 zip 文件
- [ ] (可选) 生成 SHA256 校验文件
- [ ] 配置 Web 服务器允许下载
- [ ] 测试 API 返回正确的 JSON
- [ ] 测试下载链接可访问
- [ ] 在客户端测试完整更新流程

---

**最后更新**: 2026-05-02
