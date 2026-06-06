"""
EDIST v3.8 Windows 安装程序
"""
import sys
import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess

APP_NAME = "EDIST"
APP_VERSION = "3.8"

def get_data_dir():
    """获取打包数据目录"""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'edist_data')
    else:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'edist_data')

def create_shortcut(target_path, shortcut_path, working_dir, description=""):
    """创建 Windows 快捷方式"""
    try:
        import pythoncom
        from win32com.client import Dispatch
        
        pythoncom.CoInitialize()
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = target_path
        shortcut.WorkingDirectory = working_dir
        shortcut.Description = description
        shortcut.Save()
        pythoncom.CoUninitialize()
        return True
    except ImportError:
        # 回退到 PowerShell
        try:
            ps_cmd = (
                f'$ws = New-Object -ComObject WScript.Shell; '
                f'$s = $ws.CreateShortcut("{shortcut_path}"); '
                f'$s.TargetPath = "{target_path}"; '
                f'$s.WorkingDirectory = "{working_dir}"; '
                f'$s.Description = "{description}"; '
                f'$s.Save()'
            )
            subprocess.run(['powershell', '-Command', ps_cmd], capture_output=True)
            return True
        except:
            return False

class InstallerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} v{APP_VERSION} 安装程序")
        self.root.geometry("500x420")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')
        
        # 居中
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - 500) // 2
        y = (sh - 420) // 2
        self.root.geometry(f"+{x}+{y}")
        
        self.install_dir = tk.StringVar(value=os.path.join(
            os.environ.get('LOCALAPPDATA', os.path.expanduser('~')),
            'Programs', 'EDIST'
        ))
        self.create_desktop = tk.BooleanVar(value=True)
        self.create_startmenu = tk.BooleanVar(value=True)
        
        self.build_ui()
    
    def build_ui(self):
        # 标题
        title = tk.Label(self.root, text=f"{APP_NAME} v{APP_VERSION} 安装向导",
                        font=("Microsoft YaHei", 16, "bold"), bg='#f0f0f0', fg='#1E88E5')
        title.pack(pady=(20, 10))
        
        desc = tk.Label(self.root, text="欢迎使用 EDIST 安装程序。\n本向导将引导您完成安装。",
                       font=("Microsoft YaHei", 9), bg='#f0f0f0', justify='center')
        desc.pack(pady=(0, 20))
        
        # 安装目录
        dir_frame = tk.Frame(self.root, bg='#f0f0f0')
        dir_frame.pack(fill='x', padx=30, pady=5)
        
        tk.Label(dir_frame, text="安装目录:", font=("Microsoft YaHei", 10),
                bg='#f0f0f0').pack(anchor='w')
        
        dir_row = tk.Frame(dir_frame, bg='#f0f0f0')
        dir_row.pack(fill='x', pady=(5, 0))
        
        self.dir_entry = tk.Entry(dir_row, textvariable=self.install_dir,
                                  font=("Microsoft YaHei", 9), width=45)
        self.dir_entry.pack(side='left', fill='x', expand=True)
        
        tk.Button(dir_row, text="浏览...", command=self.browse_dir,
                 font=("Microsoft YaHei", 9), width=8).pack(side='left', padx=(5, 0))
        
        # 选项
        opt_frame = tk.Frame(self.root, bg='#f0f0f0')
        opt_frame.pack(fill='x', padx=30, pady=15)
        
        tk.Checkbutton(opt_frame, text="创建桌面快捷方式", variable=self.create_desktop,
                      font=("Microsoft YaHei", 10), bg='#f0f0f0').pack(anchor='w', pady=3)
        tk.Checkbutton(opt_frame, text="创建开始菜单快捷方式", variable=self.create_startmenu,
                      font=("Microsoft YaHei", 10), bg='#f0f0f0').pack(anchor='w', pady=3)
        
        # 进度条
        self.progress = ttk.Progressbar(self.root, length=440, mode='indeterminate')
        self.progress.pack(pady=(10, 5))
        
        self.status_label = tk.Label(self.root, text="", font=("Microsoft YaHei", 9),
                                     bg='#f0f0f0', fg='#666')
        self.status_label.pack()
        
        # 按钮
        btn_frame = tk.Frame(self.root, bg='#f0f0f0')
        btn_frame.pack(pady=20)
        
        self.install_btn = tk.Button(btn_frame, text="  安装  ", command=self.do_install,
                                     font=("Microsoft YaHei", 11, "bold"),
                                     bg='#1E88E5', fg='white', relief='flat',
                                     padx=20, pady=6, cursor='hand2')
        self.install_btn.pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="  取消  ", command=self.root.quit,
                 font=("Microsoft YaHei", 11), bg='#ccc', relief='flat',
                 padx=20, pady=6).pack(side='left', padx=5)
    
    def browse_dir(self):
        path = filedialog.askdirectory(title="选择安装目录", initialdir=self.install_dir.get())
        if path:
            self.install_dir.set(path)
    
    def set_status(self, text):
        self.status_label.config(text=text)
        self.root.update()
    
    def do_install(self):
        install_path = self.install_dir.get().strip()
        if not install_path:
            messagebox.showerror("错误", "请选择安装目录！")
            return
        
        self.install_btn.config(state='disabled')
        self.progress.start(10)
        
        try:
            # 1. 创建安装目录
            self.set_status("正在创建安装目录...")
            os.makedirs(install_path, exist_ok=True)
            
            # 2. 复制文件
            data_dir = get_data_dir()
            self.set_status("正在安装文件...")
            
            total_files = sum(len(files) for _, _, files in os.walk(data_dir))
            copied = 0
            
            for root, dirs, files in os.walk(data_dir):
                rel_path = os.path.relpath(root, data_dir)
                dest_dir = os.path.join(install_path, rel_path) if rel_path != '.' else install_path
                os.makedirs(dest_dir, exist_ok=True)
                
                for f in files:
                    src = os.path.join(root, f)
                    dst = os.path.join(dest_dir, f)
                    shutil.copy2(src, dst)
                    copied += 1
                    if copied % 50 == 0:
                        self.set_status(f"正在安装文件... ({copied}/{total_files})")
            
            self.set_status(f"文件安装完成 ({total_files} 个文件)")
            
            # 3. 创建快捷方式
            exe_path = os.path.join(install_path, 'EDIST.exe')
            
            if self.create_desktop.get():
                self.set_status("正在创建桌面快捷方式...")
                desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
                shortcut_path = os.path.join(desktop, f'{APP_NAME}.lnk')
                create_shortcut(exe_path, shortcut_path, install_path, f'{APP_NAME} v{APP_VERSION}')
            
            if self.create_startmenu.get():
                self.set_status("正在创建开始菜单快捷方式...")
                startmenu = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', APP_NAME)
                os.makedirs(startmenu, exist_ok=True)
                shortcut_path = os.path.join(startmenu, f'{APP_NAME}.lnk')
                create_shortcut(exe_path, shortcut_path, install_path, f'{APP_NAME} v{APP_VERSION}')
            
            self.progress.stop()
            self.set_status("安装完成！")
            
            # 4. 完成
            if messagebox.askyesno("安装完成", 
                                   f"{APP_NAME} v{APP_VERSION} 安装成功！\n\n是否立即运行？"):
                try:
                    subprocess.Popen(exe_path, cwd=install_path)
                except:
                    os.startfile(exe_path)
            
            self.root.quit()
            
        except Exception as e:
            self.progress.stop()
            self.install_btn.config(state='normal')
            self.set_status(f"安装失败: {str(e)}")
            messagebox.showerror("安装失败", f"安装过程中出现错误:\n\n{str(e)}")
    
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = InstallerGUI()
    app.run()