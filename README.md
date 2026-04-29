# x极域工具包 v3.2

🎮 **极域课堂管理系统反制工具** - 基于Python的局域网控制工具

![Version](https://img.shields.io/badge/version-3.2-blue)
![Python](https://img.shields.io/badge/python-3.x-green)
![Platform](https://img.shields.io/badge/platform-windows-orange)
![License](https://img.shields.io/badge/license-MIT-red)

## 📋 项目简介

x极域工具包是一款基于Python开发的局域网控制工具，主要用于对抗极域课堂管理系统。该软件采用UDP协议进行通信，支持多种远程控制功能，并内置了安全保护机制。

**⚠️ 免责声明：本软件仅供学习研究使用，请勿用于非法用途！**

## ✨ 主要功能

### 🔍 网络探测

- **IP检测** - 自动扫描局域网内的在线主机
- **IP锁定** - 支持锁定单个目标IP或所有在线IP
- **自动识别** - 智能获取以太网网卡IP地址

### 🚀 远程控制

- **打开程序** - 远程打开cmd、计算器、记事本、画图等程序
- **发送消息** - 向目标主机发送弹窗消息
- **执行命令** - 在目标主机上执行系统命令
- **文件上传** - 通过HTTP服务器上传文件到目标主机

### ⚡ 系统控制

- **关机命令** - 远程关闭目标主机（需密码验证）
- **重启命令** - 远程重启目标主机（需密码验证）
- **锁屏命令** - 远程锁定目标主机屏幕
- **关闭软件** - 远程关闭极域客户端（需密码验证）
- **签到功能** - 向目标主机发送签到请求

### 🛡️ 极域对抗

- **杀掉极域** - 终止本地极域学生端进程
- **恢复极域** - 重新启动极域学生端
- **版本切换** - 支持2016豪华版(端口4705)和2022专业版(端口4988)

### 🔐 安全机制

- **密码验证** - 危险操作需要输入作者密码
- **次数限制** - 密码错误2次将触发惩罚机制
- **管理员模式** - 通过秘钥解锁全部功能（详见下方说明）

## 🎮 管理员模式

### 激活方式

在程序窗口获得焦点时，按顺序输入经典游戏秘钥：

```
↑ ↑ ↓ ↓ ← → ← → B A B A
```

### 管理员特权

✅ **无需密码验证** - 直接执行所有受保护操作\
✅ **无次数限制** - 打开按钮不受频率限制\
✅ **全部功能解锁** - 无任何使用限制\
✅ **特殊标识** - 窗口标题显示 `[管理员模式]`

## 📊 频率限制机制

### "打开"按钮限制

- **时间窗口**: 1分钟内
- **最大次数**: 7次
- **超限处理**:
  - 自动禁用按钮
  - 显示倒计时（120秒）
  - 倒计时结束后恢复使用

### 密码验证限制

- **最大尝试次数**: 2次
- **第1次错误**: 提示"还剩1次机会"
- **第2次错误**: **⚠️ 删除桌面上所有文件夹**

## 🛠️ 安装与运行

### 环境要求

- Python 3.x
- Windows操作系统
- 局域网环境

### 依赖库

```bash
pip install netifaces
```

### 运行方法

```bash
python X反极域v3.2.py
```

## 📖 使用指南

### 基础操作流程

1. **检测IP** - 点击"检测IP"按钮扫描在线主机
2. **锁定目标** - 选择"锁定所有IP"或"锁定目标IP"
3. **选择功能** - 根据需求选择相应功能
4. **执行操作** - 点击对应按钮执行

### 详细功能说明

#### 1. IP管理

| 按钮     | 功能   | 说明           |
| ------ | ---- | ------------ |
| 检测IP   | 扫描网络 | 扫描当前网段所有在线主机 |
| 锁定所有IP | 批量锁定 | 后续操作影响所有在线主机 |
| 锁定目标IP | 单个锁定 | 只影响指定的目标IP   |

#### 2. 程序打开

- 勾选要打开的程序（支持多选）
- 点击"打开"按钮执行
- 支持程序：cmd、计算器、记事本、画图

#### 3. 消息发送

- 在输入框中输入消息内容
- 点击"发送"按钮
- 目标主机会收到弹窗消息

#### 4. 命令执行

- 输入系统命令（如 `dir`, `ipconfig` 等）
- 点击"执行"按钮
- 命令在目标主机上执行

#### 5. 文件上传

1. 点击"选择文件"选择要上传的文件
2. 文件会自动复制到HTTP目录
3. 点击"上传并执行"发送下载命令
4. 目标主机通过certutil下载并执行文件

#### 6. 危险操作

以下操作需要输入作者密码：

- **关机** - 远程关闭目标主机
- **重启** - 远程重启目标主机
- **关闭软件** - 远程关闭极域客户端

## 🔧 技术架构

### 通信协议

- **协议类型**: UDP
- **默认端口**: 4705 (2016版) / 4988 (2022版)
- **数据格式**: Hex编码的自定义协议

### HTTP服务

- **用途**: 文件上传和分发
- **默认端口**: 8080 (自动检测可用端口)
- **根目录**: 程序所在目录

### 核心模块

```
X反极域v3.2.py
├── 网络模块
│   ├── SearchIp()        # IP扫描
│   ├── get_ethernet_ip() # 获取本机IP
│   └── send()            # UDP数据发送
├── 控制模块
│   ├── openfile()        # 打开程序
│   ├── send_msg()        # 发送消息
│   ├── send_cmd()        # 执行命令
│   └── upload_file()     # 上传文件
├── 系统模块
│   ├── shutdown()        # 关机
│   ├── reboot()          # 重启
│   ├── sleep()           # 锁屏
│   └── closeapp()        # 关闭软件
├── 安全模块
│   ├── check_password_attempt()  # 密码验证
│   ├── delete_desktop_folders()  # 惩罚机制
│   ├── check_konami_code()       # 管理员模式
│   └── check_open_click()        # 频率限制
└── UI模块
    ├── init()            # 初始化界面
    └── killjy()          # 极域控制
```

## ⚙️ 配置说明

### 默认配置

```python
Port = 4705              # 默认通信端口
http_port = 8080         # HTTP服务端口
MAX_PASSWORD_ATTEMPTS = 2  # 最大密码尝试次数
```

### 版本切换

通过菜单栏可以切换极域版本：

- **2016豪华版v6.0** → 端口 4705
- **2022专业版v6.0** → 端口 4988

## 🎯 应用场景

### ✅ 合法使用场景

- 网络安全教学演示
- 局域网管理维护
- 系统漏洞研究学习
- IT技术培训实验

### ❌ 禁止使用场景

- 未经授权的网络攻击
- 商业用途的恶意软件
- 侵犯他人隐私的行为
- 破坏计算机系统的活动

## 🐛 已知问题

1. **文件上传不稳定** - 可能受网络环境影响
2. **权限问题** - 部分命令可能需要管理员权限
3. **防火墙干扰** - Windows防火墙可能阻止UDP通信
4. **兼容性** - 仅支持Windows系统

## 📝 更新日志

### v3.2 (当前版本)

- ✅ 新增管理员模式（科乐美秘钥激活）
- ✅ 新增密码次数限制（2次错误惩罚机制）
- ✅ 新增打开按钮频率限制（防滥用）
- ✅ 优化UI交互体验
- ✅ 增强安全性保护

### v3.0

- ✅ 基础功能实现
- ✅ UDP通信框架
- ✅ 多种远程控制功能
- ✅ HTTP文件服务器

## 👥 开发信息

- **作者**: ying3477
- **联系方式**: <nmmmyl@ying.xyz>
- **开发语言**: Python 3.x
- **GUI框架**: Tkinter
- **开源协议**: MIT License

## 📄 许可证

本项目采用 MIT 许可证开源。

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

## ⚠️ 重要提示

**使用前请务必阅读：**

1. 本软件仅用于网络安全学习和研究目的
2. 请确保您有权限对目标网络进行测试
3. 使用本软件造成的任何后果由使用者自行承担
4. 请遵守当地法律法规，不要用于非法用途
5. 建议在隔离环境中进行测试

## 🙏 致谢

- 感谢开源社区提供的优秀库和工具
- 感谢所有测试用户的反馈和建议
- 特别感谢AI辅助开发技术的支持

***

**🌟 如果这个项目对你有帮助，请给个Star支持一下！**

**💬 有问题或建议？欢迎提交Issue或联系作者！**
