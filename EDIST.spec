# -*- mode: python ; coding: utf-8 -*-
"""
EDIST PyInstaller 打包配置

修复:
- 添加 languages/ 语言包目录
- 添加 config.json 配置文件
- 添加 app.ico 图标文件
"""

import os
import sys

block_cipher = None

a = Analysis(
    ['EDIST.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('languages', 'languages'),      # 语言包 (zh_CN.json, en_US.json)
        ('config.json', '.'),            # 主配置文件
        ('app.ico', '.'),                # 应用图标
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.simpledialog',
        'socket',
        'json',
        'os',
        'sys',
        'threading',
        'subprocess',
        'time',
        'shutil',
        'hashlib',
        'binascii',
        'logging',
        'urllib.request',
        'urllib.error',
        'ssl',
        'http.server',
        'random',
        'string',
        'netifaces',
        'packaging.version',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'pandas', 'scipy'],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='EDIST',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # GUI模式，无控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app.ico',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='EDIST',
)
