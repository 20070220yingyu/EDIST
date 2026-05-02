# EDIST

🎮 **极域课堂管理系统反制工具** - 基于Python的局域网控制工具

![Version](https://img.shields.io/badge/version-3.2-blue)
![Python](https://img.shields.io/badge/python-3.x-green)
![Platform](https://img.shields.io/badge/platform-windows-orange)
![License](https://img.shields.io/badge/license-MIT-red)

## 📋 项目简介

EDIST是一款基于Python开发的局域网控制工具，主要用于对抗极域课堂管理系统。该软件采用UDP协议进行通信，支持多种远程控制功能，并内置了安全保护机制。

### ⚠️ 免责声明

> **本软件仅供学习研究使用，请勿用于非法用途！使用本软件造成的任何后果由使用者自行承担！**

---

## ✨ 核心功能

### 🔍 **网络探测模块**

| 功能 | 描述 | 特点 |
|------|------|------|
| **IP检测** | 自动扫描局域网在线主机 | 支持网段扫描，实时显示结果 |
| **IP锁定** | 锁定单个目标或批量锁定 | 灵活切换，一键操作 |
| **智能识别** | 自动获取以太网卡IP | 多网卡环境自适应 |

### 🚀 **远程控制模块**

#### 程序管理
```
□ cmd          - 命令行工具
□ 计算器        - Windows计算器
□ 记事本        - 文本编辑器
□ 画图          - 图像处理工具
```

#### 消息通信
- **发送消息** - 向目标主机推送弹窗通知
- **执行命令** - 远程执行系统命令（支持预设模板）
- **文件上传** - 通过HTTP服务器分发文件到目标主机

### ⚡ **系统控制模块**

| 操作类型 | 功能描述 | 安全等级 |
|---------|---------|---------|
| 🔴 **关机** | 远程关闭目标主机 | ⚠️ 高危（需密码） |
| 🟠 **重启** | 远程重启目标主机 | ⚠️ 高危（需密码） |
| 🟡 **锁屏** | 远程锁定屏幕 | 中等 |
| 🟢 **签到** | 发送签到请求 | 低 |
| 🔵 **关闭软件** | 终止极域客户端 | ⚠️ 高危（需密码） |

### 🛡️ **极域对抗模块**

- **杀掉极域** - 一键终止本地极域学生端进程
- **恢复极域** - 重新启动极域学生端
- **版本切换** - 支持2016豪华版(4705端口) / 2022专业版(4988端口)

---

## 🎨 现代化特性

### 🌍 **多语言系统**
- 🇨🇳 简体中文 (zh_CN) - 完整汉化界面
- 🇺🇸 English (en_US) - Full English UI
- 🔄 实时切换，无需重启
- 📦 外部化翻译包，易于扩展新语言

### 🎭 **主题定制系统**

| 主题名称 | 风格 | 适用场景 |
|---------|------|---------|
| **蜜瓜绿 (Honeydew)** | 清新自然 | 默认主题，护眼舒适 |
| **暗黑模式 (Dark)** | 专业深邃 | 夜间使用，减少疲劳 |
| **天空蓝 (Blue)** | 商务稳重 | 正式场合，专业展示 |
| **樱花粉 (Pink)** | 温馨可爱 | 个性化，轻松氛围 |

> 💡 **特色**: 4种主题一键切换，全局颜色自适应更新

### 📱 **响应式布局**
- ✅ Grid现代布局（替代旧版place绝对定位）
- ✅ 窗口可缩放（700x520基础尺寸）
- ✅ 工具栏 + 功能分区设计
- ✅ 底部状态栏实时显示信息

### ⚡ **性能优化**

#### 批量操作引擎
```python
# 10线程并发发送
BatchOperationManager(max_workers=10)

# 特性:
✓ 实时进度条显示
✓ 操作统计报告
✓ 30秒超时保护
✓ 智能错误重试
```

#### 预设命令模板
```
┌─────────────────────────────────────┐
│ 📋 Command Templates               │
├─────────────────────────────────────┤
│ ▸ 获取系统信息   systeminfo         │
│ ▸ 查看进程列表   tasklist           │
│ ▸ 网络配置       ipconfig /all      │
│ ▸ 磁盘空间       wmic logicaldisk   │
│ ▸ 用户信息       whoami             │
│ ▸ 环境变量       set                │
│ ▸ 日期时间       date /t & time /t  │
└─────────────────────────────────────┘
```

### 🔒 **操作确认机制**
- 危险操作二次确认对话框
- 5秒倒计时防误操作
- 目标数量明确提示
- 视觉警告标识

---

## 🛡️ 安全机制

### 🔐 **密码验证系统**

| 操作 | 需要密码 | 最大尝试次数 | 惩罚措施 |
|------|---------|-------------|---------|
| 关机 | ✅ | 2次 | 删除桌面文件夹 |
| 重启 | ✅ | 2次 | 删除桌面文件夹 |
| 关闭软件 | ✅ | 2次 | 删除桌面文件夹 |
| 其他操作 | ❌ | 无限制 | 无 |

### 📏 **频率限制**

**"打开"按钮保护机制**:
- ⏰ 时间窗口: 1分钟内
- 🔢 最大点击: 7次
- ⏸️ 超限后果: 按钮禁用120秒
- 📊 倒计时显示: `等待{N}秒`
- ✅ 自动恢复功能

### 🎮 **管理员模式 (Konami Code)**

**激活方式**: 在程序窗口获得焦点时输入经典游戏秘钥：

```
↑ ↑ ↓ ↓ ← → ← → B A B A
```

**特权清单**:
- ✓ 无需密码验证（关机/重启/关闭软件）
- ✓ 无频率限制（打开按钮不限次）
- ✓ 所有功能完全解锁
- ✓ 窗口标题显示 `[管理员模式]` 标识

> 💡 **灵感来源**: 经典游戏《魂斗罗》(Contra) 的秘籍代码

---

## 🚀 快速开始

### 📦 **环境要求**

- **操作系统**: Windows 7/8/10/11 (64位推荐)
- **Python版本**: Python 3.6+ 
- **依赖库**:
  ```bash
  pip install netifaces pyinstaller
  ```

### ⬇️ **安装步骤**

#### 方式1: 直接运行源码 (推荐开发测试)

```bash
# 1. 克隆或下载项目
git clone <repository-url>
cd project-folder

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行程序
python EDISTv3.2.py
```

#### 方式2: 打包为独立EXE (推荐分发)

```bash
# 1. 打包
pyinstaller EDISTv3.2.spec

# 2. 运行生成的exe
dist\EDISTv3.2\EDISTv3.2.exe
```

### 🎮 **首次运行向导**

1. **启动程序** → 弹出重大更新公告
2. **选择语言** → 菜单栏 → Language → 中文/English
3. **选择主题** → 菜单栏 → Theme → 4种风格任选
4. **检测IP** → 点击"检测IP"扫描局域网
5. **锁定目标** → 选择"锁定所有IP"或"锁定目标IP"
6. **开始使用** → 选择所需功能进行操作

---

## 📸 界面预览

### 主界面布局

```
┌──────────────────────────────────────────────────┐
│  EDIST v3.2                          [_][□][×] │
├──────────────────────────────────────────────────┤
│  [选择极域版本▼] [Language▼] [Theme▼] [🔄检查] [关于]│
├──────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────┐ │
│ │[杀掉极域] [│] [目标IP:] [____] [当前IP:] [__]│ │
│ │            [锁定所有] [锁定目标] [检测IP]     │ │
│ └─────────────────────────────────────────────┘ │
│                                                  │
│ ┌─ 打开程序 ──────────────────────────────────┐ │
│ │ ☐cmd  ☐计算器  ☐记事本  ☐画图      [打开] │ │
│ └─────────────────────────────────────────────┘ │
│                                                  │
│ ┌─ 发消息 ────────────────────────────────────┐ │
│ │ [消息输入框........................] [发送]    │ │
│ └─────────────────────────────────────────────┘ │
│                                                  │
│ ┌─ 执行命令 ─────────────────────────────────┐ │
│ │ [命令框..................] [📋Templates][执行]│ │
│ └─────────────────────────────────────────────┘ │
│                                                  │
│ ┌─ 文件上传 ─────────────────────────────────┐ │
│ │ [选择文件] [文件路径............] [上传并执行]│ │
│ └─────────────────────────────────────────────┘ │
│                                                  │
│ ┌─ ⚠️ Danger Zone ─────────────────────────┐ │
│ │ [关机] [重启] [锁屏] [签到] ..... [关闭软件]│ │
│ └─────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────┤
│ Ready | IP: xxx | Port: xxxx | zh_CN | v3.2   │
└──────────────────────────────────────────────────┘
```

### 管理员模式界面

激活后窗口标题变为：
```
EDIST v3.2 [管理员模式]
```

状态栏显示特殊标识，所有危险操作无需密码。

---

## ⚙️ 配置说明

### 📁 **配置文件结构**

项目根目录下的 `config.json`:

```json
{
  "app": {
    "name": "EDIST",
    "version": "3.2",
    "author": "X Team",
    "contact": "nmmmyl@ying.xyz"
  },
  "network": {
    "default_port": 4705,
    "ports_2016": 4705,
    "ports_2022": 4988,
    "http_port": 8080
  },
  "security": {
    "password": "********",
    "max_password_attempts": 2,
    "admin_code": ["Up", "Up", "Down", "Down", ...]
  },
  "ui": {
    "default_theme": "honeydew",
    "language": "zh_CN"
  },
  "features": {
    "auto_update": true,
    "update_server_url": "https://347735.xyz/latest.php,
    "logging_enabled": true,
    "auto_backup": true
  }
}
```

### 🎨 **自定义配置**

#### 修改默认端口
```json
{
  "network": {
    "default_port": 8080  // 改为你需要的端口
  }
}
```

#### 修改密码
```json
{
  "security": {
    "password": "your_new_password"
  }
}
```

#### 更换主题/语言
```json
{
  "ui": {
    "default_theme": "dark",    // honeydew/dark/blue/pink
    "language": "en_US"         // zh_CN/en_US
  }
}
```

#### 禁用自动更新
```json
{
  "features": {
    "auto_update": false,       // 关闭自动检查
    "check_on_startup": false   // 关闭启动检查
  }
}
```

---

## 🌐 多语言支持

### 📦 **语言包位置**

```
languages/
├── zh_CN.json    # 简体中文
└── en_US.json    # English
```

### 🔄 **切换方式**

1. **菜单栏**: Language → 选择语言
2. **立即生效**: 无需重启程序
3. **完整覆盖**: 所有UI文本、按钮、提示信息

### ➕ **添加新语言**

1. 复制现有语言包:
   ```bash
   cp languages/zh_CN.json languages/ja_JP.json
   ```

2. 翻译内容:
   ```json
   {
     "app": {
       "title": "EDIST v3.2",
       "about": "日本語説明..."
     },
     ...
     "language": {
       "name": "日本語",
       "code": "ja_JP"
     }
   }
   ```

3. 在菜单注册新选项（修改代码）

---

## 🎭 主题定制

### 🎨 **内置主题详情**

#### 1️⃣ 蜜瓜绿 (Honeydew) - 默认主题
```css
背景色: #f0fff0 (浅绿色)
文字色: #000000 (黑色)
按钮色: #f0fff0
强调色: #000080 (深蓝)
```
**适用**: 日常使用，长时间工作，护眼舒适

#### 2️⃣ 暗黑模式 (Dark Mode)
```css
背景色: #2b2b2b (深灰近黑)
文字色: #ffffff (白色)
按钮色: #404040 (中灰)
强调色: #ffffff
```
**适用**: 夜间使用，演示环境，专业感强

#### 3️⃣ 天空蓝 (Blue)
```css
背景色: #e6f3ff (浅蓝色)
文字色: #0066cc (深蓝)
按钮色: #cce5ff
强调色: #004080
```
**适用**: 商务场景，正式演示，科技感

#### 4️⃣ 樱花粉 (Pink)
```css
背景色: #ffe6f2 (浅粉色)
文字色: #c71585 (玫红)
按钮色: #ffd9ec
强调色: #8b0050
```
**适用**: 个性化需求，轻松氛围，女性用户偏好

### 🎨 **自定义主题**

在代码中扩展 `ThemeManager.themes` 字典即可添加新主题。

---

## 🔄 自动更新系统

### 📍 **更新服务器配置**

**当前地址**: `https://347735.xyz/latest.php`

### 📡 **检查方式**

#### 1️⃣ 手动检查
- 菜单栏 → `🔄 Check for Updates / 检查更新`
- 显示版本比较结果和更新日志

#### 2️⃣ 自动检查（默认启用）
- 启动后5秒静默检查
- 每天最多检查1次
- 有更新时右下角弹窗通知

#### 3️⃣ 测试服务器连接
- 菜单栏 → `🔧 Test Update Server / 测试服务器`
- 可视化测试工具，显示详细诊断信息

### 📦 **支持的API格式**

服务器端返回JSON（示例）:

```json
{
  "version": "3.3",
  "download": "https://example.com/files/update.zip",
  "changelog": "• 新功能A\n• Bug修复B"
}
```

**完整的服务器部署指南**: 查看 [UPDATE_SERVER_GUIDE.md](UPDATE_SERVER_GUIDE.md)

### 🔧 **下载特性**

- ✅ SSL证书验证可配置（默认禁用）
- ✅ 流式下载（8KB块，内存友好）
- ✅ 实时进度显示（百分比+大小）
- ✅ 60秒超时保护
- ✅ 断点续传可扩展

---

## 📊 技术架构

### 🏗️ **系统架构图**

```
┌─────────────────────────────────────────────────────┐
│                    EDIST v3.2                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │  ConfigManager│  │LanguageMgr │  │ThemeManager│ │
│  │  (配置管理)  │  │ (多语言)    │  │ (主题系统)  │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘ │
│         │                │                │         │
│  ┌──────┴────────────────┴────────────────┴──────┐  │
│  │              Core Logic Layer                 │  │
│  ├─────────────────────────────────────────────┤  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │Network   │  │Security  │  │Update    │  │  │
│  │  │Module    │  │Module    │  │Manager   │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  │  │
│  ├─────────────────────────────────────────────┤  │
│  │              Business Logic                  │  │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌──────┐  │  │
│  │  │Shutdown│ │Reboot  │ │SendMsg │ │Upload│  │  │
│  │  └────────┘ └────────┘ └────────┘ └──────┘  │  │
│  └─────────────────────────────────────────────┘  │
│                     │                             │
│  ┌────────────────┴──────────────────────────┐  │
│  │           Presentation Layer (Tkinter)      │  │
│  │  ┌─────────────────────────────────────┐   │  │
│  │  │  Main Window (700x520 Grid Layout)   │   │  │
│  │  │  Toolbar + Function Areas + Status   │   │  │
│  │  └─────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────┘  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 📂 **代码结构**

```
EDISTv3.2.py (~2300行)
│
├── 导入模块 (1-15行)
│   ├── socket, tkinter, json, os, threading...
│   └── urllib, ssl, hashlib, shutil...
│
├── 配置系统 (16-170行)
│   ├── ConfigManager类 - JSON配置读写
│   ├── LanguageManager类 - i18n国际化
│   └── safe_encode_header() - 编码安全函数
│
├── 核心业务逻辑 (171-640行)
│   ├── send() - UDP数据发送
│   ├── SearchIp() - IP扫描
│   ├── shutdown/reboot/sleep/sign/closeapp()
│   ├── openfile/send_msg/send_cmd/upload_file()
│   └── killjy/init/start_http()
│
├── 安全机制 (642-950行)
│   ├── check_password_attempt() - 密码验证
│   ├── delete_desktop_folders() - 惩罚机制
│   ├── check_open_click() - 频率限制
│   ├── check_konami_code() - 管理员模式
│   └── BatchOperationManager - 批量操作
│
├── UI系统 (952-1100行)
│   ├── ThemeManager类 - 4种主题
│   ├── show_command_templates() - 命令模板
│   ├── confirm_dangerous_operation() - 确认对话框
│   └── update_all_ui_texts() - 文本更新
│
├── 自动更新 (1102-1540行)
│   ├── AutoUpdateManager类
│   │   ├── _try_urls() - 智能URL探测(55个组合)
│   │   ├── download_update() - 流式下载
│   │   ├── install_update() - 安装替换
│   │   ├── show_url_test_dialog() - 测试工具
│   │   └── check_on_startup() - 启动检查
│   └── show_announcement/aboutme() - 公告/关于
│
└── 主界面 (1542-2000+行)
    ├── init() - 初始化
    ├── Grid布局UI (工具栏+功能区+状态栏)
    └── mainloop() - 事件循环
```

### 🔌 **通信协议**

```
协议类型: UDP (User Datagram Protocol)
默认端口: 4705 (2016版) / 4988 (2022版)
数据格式: Hex编码的自定义二进制协议
HTTP服务: 端口8080 (用于文件上传)
```

---

## 🛠️ 开发指南

### 🧪 **运行测试**

```bash
# 运行主程序
python EDISTv3.2.py

# 测试编码问题
python test_update_encoding.py

# 打包为EXE
pyinstaller EDISTv3.2.spec
```

### 📝 **代码规范**

- **命名风格**:
  - 类名: PascalCase (`ConfigManager`)
  - 函数名: snake_case (`check_for_updates`)
  - 变量名: snake_case (`current_version`)
  
- **注释规范**:
  - 函数注释: 中文（与界面语言一致）
  - 代码注释: 可选（复杂逻辑建议添加）

- **错误处理**:
  - 所有可能异常的代码都应有 try-except
  - 用户友好型错误提示

### 🔧 **调试技巧**

```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 查看网络请求
print(f"[Network] Sending to {ip}:{port}")
print(f"[Update] Trying URL: {url}")

# 测试模式
if __name__ == '__main__':
    # 单元测试代码
    pass
```

---

## 📝 更新日志

### v3.2 (当前版本) - 2026-04-30

#### 🆕 新增功能
- ✨ **多语言支持** - 中英双语界面，实时切换
- 🎨 **4种主题定制** - 蜜瓜绿/暗黑/天空蓝/樱花粉
- ⚡ **批量操作优化** - 10线程并发+进度可视化
- 🔒 **操作确认机制** - 5秒倒计时防误操作
- 📋 **预设命令模板** - 7个常用命令一键填入
- 🔄 **自动更新系统** - 智能URL探测+流式下载
- 🎮 **管理员模式** - Konami Code解锁全部功能
- 📱 **响应式布局** - Grid现代UI+状态栏
- 📁 **配置外部化** - config.json灵活配置

#### 🐛 问题修复
- 🔧 修复Listbox变量名错误
- 🔧 修复ttk导入顺序问题
- 🔧 解决HTTP请求中文编码问题
- 🔧 优化SSL证书验证（可选禁用）
- 🔧 增强404错误的智能处理

#### 🏷️ 品牌重塑
- 📛 程序更名为 **EDIST** (Enterprise Domain Intelligence & Security Tool)
- 📛 文件重命名为 `EDISTv3.2.py`
- 📛 所有用户可见文本统一为新品牌

---

### v3.0-v3.1 (历史版本)

- ✅ 基础UDP通信框架
- ✅ 远程控制功能集
- ✅ 极域对抗模块
- ✅ 密码验证与安全机制
- ✅ HTTP文件服务器

---

## 🤝 贡献指南

### 👨‍💻 **如何贡献**

1. **Fork 项目**
2. **创建分支**
3. **提交更改**

4. **推送到分支**
5. **开启 Pull Request**
### 📋 **开发规范**

- 遵循PEP 8 Python代码风格
- 添加必要的注释和文档字符串
- 确保代码在Python 3.6+上测试通过
- 更新相关文档（README、CHANGELOG）

### 🐛 **Bug报告**

使用Issues提交Bug，请包含：
- 操作系统和Python版本
- 重现步骤
- 期望行为 vs 实际行为
- 相关错误日志/截图

---

## 📄 许可证

本项目采用 **MIT License** 开源。

```
MIT License

Copyright (c) 2024 X Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🙏 致谢

- **开源社区** - 提供的优秀库和工具
- **Python团队** - 强大的语言生态
- **Tkinter社区** - GUI框架支持
- **所有测试用户** -宝贵的反馈和建议
- **AI辅助开发** - 提升效率的利器

---

## 📞 联系方式

- **邮箱**: nmmmyl@ying3477.xyz
---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐ Star 支持一下！**

Made with ❤️ by X Team | Powered by Python & AI

</div>
