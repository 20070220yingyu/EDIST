import re

# 读取原文件
with open('EDIST.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到 AutoUpdateManager 类的开始和结束位置
start_marker = 'class AutoUpdateManager:'
end_marker = '# 全局自动更新管理器\nupdate_manager = AutoUpdateManager()'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print('ERROR: Could not find markers')
    exit(1)

print(f'Found AutoUpdateManager at line {content[:start_idx].count(chr(10))+1}')
print(f'Ends at line {content[:end_idx].count(chr(10))+1}')

# 保留类之前的内容
before_class = content[:start_idx]

# 保留类之后的内容  
after_class = content[end_idx + len(end_marker):]

print(f'Before class: {len(before_class)} chars')
print(f'After class: {len(after_class)} chars')
print('Successfully identified the section to replace')

# 新的 AutoUpdateManager 类代码（基于 latest.php + 1.txt 的逻辑）
new_autoupdate_class = '''class AutoUpdateManager:
    """
    自动更新管理器 - 基于 PHP API (latest.php) 的现代化更新系统
    
    工作流程:
    1. 启动时/手动触发 → 请求 latest.php 获取版本信息
    2. 发现新版本 → 下载 zip + SHA256 校验
    3. 校验通过 → 解压到临时目录
    4. 调用 updater.exe 替换文件并重启主程序
    """
    
    def __init__(self):
        self.current_version = config.get('app.version', '3.2')
        # 更新服务器地址 - 使用 latest.php
        self.update_api_url = config.get('features.update_server_url', 'https://347735.xyz/genxin/latest.php')
        self.update_check_enabled = config.get('features.auto_update', True)
        
        print(f"[Update] 初始化完成")
        print(f"[Update] 当前版本: v{self.current_version}")
        print(f"[Update] 服务器地址: {self.update_api_url}")
    
    def is_packaged(self):
        """判断当前是否运行在 PyInstaller 打包后的 exe 中"""
        return hasattr(sys, '_MEIPASS')
    
    def _compare_versions(self, v1, v2):
        """
        比较两个版本号
        
        Returns:
            int: 1(v1>v2), 0(v1==v2), -1(v1<v2)
        """
        try:
            from packaging import version as ver
            result = ver.parse(v1) > ver.parse(v2)
            return 1 if result else (-1 if ver.parse(v1) < ver.parse(v2) else 0)
        except ImportError:
            # 如果没有 packaging 库，使用简单的版本比较
            try:
                v1_parts = [int(x) for x in v1.split('.')]
                v2_parts = [int(x) for x in v2.split('.')]
                max_len = max(len(v1_parts), len(v2_parts))
                v1_parts.extend([0] * (max_len - len(v1_parts)))
                v2_parts.extend([0] * (max_len - len(v2_parts)))
                for i in range(max_len):
                    if v1_parts[i] > v2_parts[i]:
                        return 1
                    elif v1_parts[i] < v2_parts[i]:
                        return -1
                return 0
            except:
                return 0
    
    def download_file(self, url, dest_path, progress_callback=None):
        """
        下载文件（支持进度回调）
        
        Args:
            url: 下载链接
            dest_path: 保存路径
            progress_callback: 进度回调函数 callback(downloaded, total)
        
        Returns:
            bool: 是否成功
        """
        try:
            import urllib.request
            import ssl
            
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            req = urllib.request.Request(url, headers={
                'User-Agent': f'EDIST/{self.current_version}',
                'Accept': '*/*'
            })
            
            with urllib.request.urlopen(req, timeout=60, context=ctx) as response:
                total_size = int(response.headers.get('Content-Length', 0))
                downloaded = 0
                
                with open(dest_path, 'wb') as f:
                    while True:
                        chunk = response.read(8192)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_callback:
                            progress_callback(downloaded, total_size or downloaded)
                
                return True
                
        except Exception as e:
            print(f"[Update] 下载失败: {e}")
            return False
    
    def verify_hash(self, filepath, expected_hash):
        """
        校验文件 SHA256
        
        Args:
            filepath: 文件路径
            expected_hash: 期望的哈希值 (格式: 'sha256:xxxxx' 或纯哈希值)
        
        Returns:
            bool: 校验是否通过
        """
        if not expected_hash:
            print("[Update] 未提供哈希值，跳过校验")
            return True
        
        import hashlib
        
        # 解析哈希格式
        if ':' in expected_hash:
            algo, expected_value = expected_hash.split(':')
        else:
            algo = 'sha256'
            expected_value = expected_hash
        
        print(f"[Update] 正在校验文件 ({algo})...")
        
        h = hashlib.new(algo)
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                h.update(chunk)
        
        actual_hash = h.hexdigest()
        is_valid = actual_hash == expected_value
        
        if is_valid:
            print(f"[Update] ✓ 文件校验通过")
        else:
            print(f"[Update] ✗ 文件校验失败!")
            print(f"[Update]   期望: {expected_value}")
            print(f"[Update]   实际: {actual_hash}")
        
        return is_valid
    
    def extract_zip(self, zip_path, extract_to):
        """解压 zip 到指定目录"""
        import zipfile
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(extract_to)
        print(f"[Update] 已解压到: {extract_to}")
    
    def check_for_updates(self, show_no_update_msg=True, silent=False):
        """
        检查是否有新版本可用（请求 latest.php）
        
        Args:
            show_no_update_msg: 如果没有更新是否显示提示
            silent: 静默模式（不弹窗）
        
        Returns:
            dict: {'has_update': bool, 'version': str, 'download_url': str, ...}
        """
        if not silent:
            progress_dialog = self._show_checking_dialog()
        
        try:
            import urllib.request
            import ssl
            
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            print(f"[Update] 正在检查更新: {self.update_api_url}")
            
            req = urllib.request.Request(
                self.update_api_url,
                headers={
                    'User-Agent': f'EDIST/{self.current_version}',
                    'Accept': 'application/json',
                    'Cache-Control': 'no-cache'
                }
            )
            
            with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
                content = response.read().decode('utf-8')
                data = json.loads(content)
            
            if not data.get('success'):
                error_msg = data.get('error', '未知错误')
                print(f"[Update] 服务器返回错误: {error_msg}")
                
                if not silent:
                    if progress_dialog:
                        progress_dialog.destroy()
                    messagebox.showerror(
                        t('app.title') + " - Update Error",
                        f"检查更新失败:\\n\\n{error_msg}"
                    )
                return {'has_update': False, 'error': error_msg}
            
            latest_version = data.get('version')
            download_url = data.get('download_url')
            file_hash = data.get('file_hash')
            filename = data.get('filename')
            changelog = data.get('release_notes', '')
            
            print(f"[Update] 最新版本: v{latest_version}")
            print(f"[Update] 下载地址: {download_url}")
            
            # 比较版本号
            if self._compare_versions(latest_version, self.current_version) > 0:
                print(f"[Update] ✓ 发现新版本 v{latest_version} (当前: v{self.current_version})")
                
                result = {
                    'has_update': True,
                    'version': latest_version,
                    'download_url': download_url,
                    'file_hash': file_hash,
                    'filename': filename,
                    'changelog': changelog
                }
                
                if not silent:
                    if progress_dialog:
                        progress_dialog.destroy()
                    self._show_update_available_dialog(result)
                
                return result
            else:
                print(f"[Update] 当前已是最新版本 v{self.current_version}")
                
                if not silent and show_no_update_msg:
                    if progress_dialog:
                        progress_dialog.destroy()
                    messagebox.showinfo(
                        t('app.title') + " - Update",
                        f"✅ 当前已是最新版本！\\n\\n当前版本: v{self.current_version}"
                    )
                elif not silent and progress_dialog:
                    progress_dialog.destroy()
                
                return {'has_update': False, 'version': self.current_version}
                
        except urllib.error.URLError as e:
            print(f"[Update] 网络错误: {e}")
            if not silent:
                if progress_dialog:
                    progress_dialog.destroy()
                messagebox.showerror(
                    t('app.title') + " - Update Error",
                    f"{t('messages.update_check_failed')}\\n\\n错误: {str(e)}\\n请检查网络连接或稍后重试。"
                )
            return {'has_update': False, 'error': str(e)}
            
        except Exception as e:
            print(f"[Update] 检查更新异常: {e}")
            if not silent:
                if progress_dialog:
                    progress_dialog.destroy()
                messagebox.showerror(
                    t('app.title') + " - Update Error",
                    f"{t('messages.update_error')}\\n\\n{str(e)}"
                )
            return {'has_update': False, 'error': str(e)}
    
    def check_and_update(self, show_progress=True):
        """
        完整的自动更新流程：检查→下载→校验→解压→调用updater→重启
        
        Args:
            show_progress: 是否显示GUI进度界面
        """
        print("\\n" + "="*60)
        print("[Update] 开始自动更新流程...")
        print("="*60 + "\\n")
        
        # 1. 请求版本信息
        print("[Step 1/5] 正在检查版本信息...")
        try:
            import urllib.request
            import ssl
            import tempfile
            
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            req = urllib.request.Request(
                self.update_api_url,
                headers={
                    'User-Agent': f'EDIST/{self.current_version}',
                    'Accept': 'application/json'
                }
            )
            
            with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
                content = response.read().decode('utf-8')
                data = json.loads(content)
            
            if not data.get('success'):
                print(f"[Update] ✗ 服务器返回错误: {data.get('error')}")
                if show_progress:
                    messagebox.showerror("Update Error", f"检查更新失败:\\n{data.get('error', '未知错误')}")
                return False
            
            latest_version = data['version']
            download_url = data['download_url']
            file_hash = data.get('file_hash')
            filename = data.get('filename', 'update.zip')
            
            print(f"[Update] 服务器版本: v{latest_version}")
            print(f"[Update] 当前版本: v{self.current_version}")
            
        except Exception as e:
            print(f"[Update] ✗ 网络错误: {e}")
            if show_progress:
                messagebox.showerror("Update Error", f"网络错误，无法检查更新:\\n{e}")
            return False
        
        # 2. 比较版本号
        print("\\n[Step 2/5] 比较版本号...")
        if self._compare_versions(latest_version, self.current_version) <= 0:
            print("[Update] ✓ 当前已是最新版本")
            if show_progress:
                messagebox.showinfo("Update", "✅ 当前已是最新版本！")
            return True
        
        print(f"[Update] ✓ 发现新版本 v{latest_version}")
        
        # 确认是否更新
        if show_progress:
            if not messagebox.askyesno(
                "发现新版本",
                f"发现新版本 v{latest_version}\\n\\n"
                f"当前版本: v{self.current_version}\\n"
                f"最新版本: v{latest_version}\\n\\n"
                f"是否立即下载并安装？"
            ):
                print("[Update] 用户取消更新")
                return False
        
        # 3. 下载 zip
        print(f"\\n[Step 3/5] 正在下载 {filename}...")
        tmp_dir = tempfile.gettempdir()
        zip_path = os.path.join(tmp_dir, filename)
        
        if show_progress:
            success = self._download_with_gui(download_url, zip_path, filename, latest_version)
        else:
            success = self.download_file(download_url, zip_path)
        
        if not success:
            print("[Update] ✗ 下载失败")
            if show_progress:
                messagebox.showerror("Download Error", "下载更新文件失败，请检查网络连接")
            return False
        
        print(f"[Update] ✓ 下载完成: {zip_path}")
        
        # 4. 校验哈希
        print(f"\\n[Step 4/5] 正在校验文件完整性...")
        if not self.verify_hash(zip_path, file_hash):
            print("[Update] ✗ 文件校验失败，可能文件已损坏")
            if show_progress:
                messagebox.showerror("Verification Error", 
                    "文件校验失败！\\n\\n下载的文件可能已损坏或不完整。\\n请稍后重试。")
            try:
                os.remove(zip_path)
            except:
                pass
            return False
        
        print("[Update] ✓ 文件校验通过")
        
        # 4.5 解压
        print(f"\\n[Step 4.5/5] 正在解压更新包...")
        extract_dir = tempfile.mkdtemp(prefix='EDIST_update_')
        
        try:
            self.extract_zip(zip_path, extract_dir)
        except Exception as e:
            print(f"[Update] ✗ 解压失败: {e}")
            if show_progress:
                messagebox.showerror("Extract Error", f"解压更新包失败:\\n{e}")
            shutil.rmtree(extract_dir, ignore_errors=True)
            try:
                os.remove(zip_path)
            except:
                pass
            return False
        
        try:
            os.remove(zip_path)
        except:
            pass
        
        print(f"[Update] ✓ 解压完成: {extract_dir}")
        
        # 5. 启动更新器并退出主程序
        print(f"\\n[Step 5/5] 准备启动更新器...")
        
        if not self.is_packaged():
            print("[Update] 检测到源码运行环境，无法自动替换文件")
            if show_progress:
                messagebox.showinfo(
                    "Update Info",
                    f"新版本 v{latest_version} 已下载并解压完成！\\n\\n"
                    f"解压位置: {extract_dir}\\n\\n"
                    f"由于您正在使用源码运行，无法自动替换文件。\\n"
                    f"请手动备份并替换文件后重启程序。"
                )
            return True
        
        current_dir = os.path.dirname(sys.executable)
        updater_exe = os.path.join(current_dir, 'updater.exe')
        
        if not os.path.exists(updater_exe):
            print(f"[Update] ✗ 更新器不存在: {updater_exe}")
            if show_progress:
                messagebox.showerror(
                    "Updater Not Found",
                    f"未找到更新器程序 (updater.exe)\\n\\n期望位置: {updater_exe}\\n\\n请确保 updater.exe 与主程序在同一目录下。"
                )
            return False
        
        print(f"[Update] ✓ 找到更新器: {updater_exe}")
        print(f"[Update] 当前目录: {current_dir}")
        print(f"[Update] 新版本目录: {extract_dir}")
        
        if show_progress:
            messagebox.showinfo(
                "Updating",
                f"正在准备更新...\\n\\n"
                f"程序将自动关闭并由更新器完成剩余工作。\\n"
                f"请稍候，程序会自动重新启动。"
            )
        
        print("[Update] 启动更新器进程...")
        subprocess.Popen([updater_exe, extract_dir, current_dir])
        
        print("[Update] 主程序即将退出...")
        print("="*60)
        
        time.sleep(1)
        sys.exit(0)
    
    def _download_with_gui(self, url, dest_path, filename, version):
        """带 GUI 进度显示的下载"""
        progress_window = tk.Toplevel(root)
        progress_window.title(f"Downloading v{version}...")
        progress_window.geometry("450x180")
        progress_window.resizable(False, False)
        progress_window.transient(root)
        progress_window.grab_set()
        
        tk.Label(progress_window, text=f"📥 Downloading v{version}", 
                font=('楷体', 14, 'bold')).pack(pady=15)
        
        tk.Label(progress_window, text=f"File: {filename}", 
                font=('Consolas', 9)).pack()
        
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(progress_window, variable=progress_var, 
                                     maximum=100, length=400, mode='determinate')
        progress_bar.pack(pady=10)
        
        status_label = tk.Label(progress_window, text="Connecting...", font=('Consolas', 10))
        status_label.pack()
        
        progress_window.update()
        
        def progress_callback(downloaded, total):
            if total > 0:
                percent = (downloaded / total) * 100
                progress_var.set(percent)
                status_label.config(
                    text=f"{downloaded/(1024*1024):.1f} MB / {total/(1024*1024):.1f} MB ({percent:.1f}%)"
                )
            else:
                status_label.config(text=f"{downloaded/(1024*1024):.1f} MB downloaded...")
            progress_window.update()
        
        success = self.download_file(url, dest_path, progress_callback)
        
        if success:
            status_label.config(text="✅ Download complete!", fg='green')
            progress_var.set(100)
            progress_window.update()
            progress_window.after(1500, progress_window.destroy)
            progress_window.wait_window()
        else:
            progress_window.destroy()
        
        return success
    
    def check_on_startup(self):
        """启动时自动检查更新（静默模式）"""
        if not self.update_check_enabled:
            print("[Update] 自动更新检查已禁用")
            return
        
        print("[Update] 将在5秒后进行启动检查...")
        root.after(5000, self._startup_check)
    
    def _startup_check(self):
        """执行启动时的静默检查"""
        import datetime
        
        last_check_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.last_update_check')
        
        should_check = True
        if os.path.exists(last_check_file):
            try:
                with open(last_check_file, 'r') as f:
                    last_check_str = f.read().strip()
                    last_check_time = datetime.datetime.fromisoformat(last_check_str)
                    if (datetime.datetime.now() - last_check_time).days < 1:
                        should_check = False
            except:
                pass
        
        if should_check:
            print("[Update] 执行启动时更新检查...")
            result = self.check_for_updates(show_no_update_msg=False, silent=True)
            
            with open(last_check_file, 'w') as f:
                f.write(datetime.datetime.now().isoformat())
            
            if result.get('has_update'):
                self._show_update_notification(result)
        else:
            print("[Update] 今日已检查过更新，跳过")
    
    def _show_update_notification(self, version_info):
        """显示更新通知（右下角弹出）"""
        notification = tk.Toplevel(root)
        notification.overrideredirect(True)
        notification.geometry("350x80+{}+{}".format(
            root.winfo_screenwidth() - 370,
            root.winfo_screenheight() - 100
        ))
        notification.attributes('-topmost', True)
        
        frame = tk.Frame(notification, bg='#4caf50', padx=15, pady=10)
        frame.pack(fill='both', expand=True)
        
        tk.Label(frame, 
                text=f"🎉 New version v{version_info['version']} available!",
                font=('楷体', 11, 'bold'), bg='#4caf50', fg='white').pack(anchor='w')
        
        tk.Label(frame,
                text="Click here to update now",
                font=('楷体', 9), bg='#4caf50', fg='#e8f5e9').pack(anchor='w', pady=(5,0))
        
        def on_click(e):
            notification.destroy()
            self.check_and_update(show_progress=True)
        
        def close_notification():
            notification.destroy()
        
        frame.bind('<Button-1>', on_click)
        notification.bind('<Button-1>', on_click)
        
        notification.after(15000, close_notification)
    
    def _show_checking_dialog(self):
        """显示检查更新对话框"""
        dialog = tk.Toplevel(root)
        dialog.title(t('app.title') + " - Checking for Updates...")
        dialog.geometry("320x120")
        dialog.resizable(False, False)
        dialog.transient(root)
        dialog.grab_set()
        
        tk.Label(dialog, text="🔍 Checking for updates...", font=('楷体', 12)).pack(pady=20)
        
        progress = ttk.Progressbar(dialog, length=270, mode='indeterminate')
        progress.pack(pady=10)
        progress.start(10)
        
        dialog.update()
        
        return dialog
    
    def _show_update_available_dialog(self, version_info):
        """显示有可用更新的对话框"""
        dialog = tk.Toplevel(root)
        dialog.title(f"🎉 New Version Available! - v{version_info['version']}")
        dialog.geometry("520x480")
        dialog.resizable(True, True)
        dialog.transient(root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = root.winfo_x() + (root.winfo_width() - 520) // 2
        y = root.winfo_y() + (root.winfo_height() - 480) // 2
        dialog.geometry(f"+{x}+{y}")
        
        header_frame = tk.Frame(dialog, bg='#4caf50')
        header_frame.pack(fill='x')
        tk.Label(header_frame, text=f"🎉 发现新版本 v{version_info['version']}", 
                font=('楷体', 16, 'bold'), bg='#4caf50', fg='white').pack(pady=15)
        
        info_frame = tk.Frame(dialog, padx=20, pady=10)
        info_frame.pack(fill='both', expand=True)
        
        tk.Label(info_frame, text=f"Current Version: v{self.current_version}", 
                font=('楷体', 11)).pack(anchor='w')
        tk.Label(info_frame, text=f"Latest Version:  v{version_info['version']}", 
                font=('楷体', 11, 'bold'), fg='#4caf50').pack(anchor='w', pady=(5,0))
        
        if version_info.get('changelog'):
            tk.Label(info_frame, text="\\n📋 Changelog:", font=('楷体', 11, 'bold')).pack(anchor='w', pady=(15,5))
            
            changelog_text = tk.Text(info_frame, height=8, wrap='word', font=('Consolas', 9))
            changelog_text.insert('1.0', version_info['changelog'])
            changelog_text.config(state='disabled')
            changelog_text.pack(fill='both', expand=True)
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(fill='x', pady=15)
        
        def on_update_now():
            dialog.destroy()
            self.check_and_update(show_progress=True)
        
        tk.Button(btn_frame, text="⬇️ 立即下载并安装", command=on_update_now,
                 font=('楷体', 11), bg='#4caf50', fg='white', width=18).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="稍后再说", command=dialog.destroy,
                 font=('楷体', 11), bg='#9e9e9e', fg='white', width=10).pack(side='right', padx=5)
        
        tk.Button(btn_frame, text="跳过此版本", 
                 command=lambda: [self._skip_version(version_info['version']), dialog.destroy()],
                 font=('楷体', 11), bg='#ff9800', fg='white', width=12).pack(side='right', padx=5)
    
    def _skip_version(self, version):
        """跳过指定版本"""
        skip_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.skipped_version')
        with open(skip_file, 'w') as f:
            f.write(version)
        print(f"[Update] 用户跳过版本: {version}")
    
    def is_version_skipped(self, version):
        """检查版本是否被跳过"""
        skip_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.skipped_version')
        if os.path.exists(skip_file):
            with open(skip_file, 'r') as f:
                skipped = f.read().strip()
                return skipped == version
        return False

'''

# 组合新的文件内容
new_content = before_class + new_autoupdate_class + '\\n\\n' + end_marker + after_class

# 写入新文件
with open('EDIST.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('\\n✅ Successfully replaced AutoUpdateManager class!')
print(f'New file size: {len(new_content)} chars')
