# -*- mode: python ; coding: utf-8 -*-
"""
EDIST 打包配置 - 主程序 + 更新器

生成文件:
- EDIST.exe (主程序 - GUI模式)
- updater.exe (独立更新器 - 控制台模式)

输出目录: build/EDIST_bundle/
"""

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_all

block_cipher = None

# ==================== 主程序分析 (EDIST.py) ====================
a_main = Analysis(
    ['EDIST.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.json', '.'),
        ('languages', 'languages'),
        ('app.ico', '.'),
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
    cipher=block_cipher,
)

pyz_main = PYZ(a_main.pure, a_main.zipped_data, cipher=block_cipher)

# ==================== 主程序 EXE (GUI模式) ====================
exe_main = EXE(
    pyz_main,
    a_main.scripts,
    a_main.binaries,
    a_main.zipfiles,
    a_main.datas,
    [],
    name='EDIST',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 无控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app.ico',
    version=None,
)

# ==================== 更新器分析 (updater.py) ====================
updater_path = os.path.join('fwq', 'updater.py')
a_updater = Analysis(
    [updater_path],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'os',
        'sys',
        'time',
        'shutil',
        'subprocess',
        'logging',
        'datetime',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy', 'pandas'],
    noarchive=False,
    cipher=block_cipher,
)

pyz_updater = PYZ(a_updater.pure, a_updater.zipped_data, cipher=block_cipher)

# ==================== 更新器 EXE (控制台模式) ====================
exe_updater = EXE(
    pyz_updater,
    a_updater.scripts,
    [],
    exclude_binaries=True,
    name='updater',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # 显示控制台（用于输出更新日志）
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 更新器不需要图标
    version=None,
)

# ==================== 收集所有文件到同一目录 ====================
coll = COLLECT(
    exe_main,
    a_main.binaries,
    a_main.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='EDIST',
)

# 将 updater.exe 也复制到同一个输出目录
# 注意：PyInstaller 不直接支持多 EXE 到同一目录，需要手动处理
