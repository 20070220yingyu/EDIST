# build_bundle.py - EDIST 完整打包脚本
"""
功能:
1. 打包主程序 EDIST.py → EDIST.exe (GUI模式)
2. 打包更新器 fwq/updater.py → updater.exe (控制台模式)
3. 将两者合并到 build/EDIST_v3.2/ 目录

用法:
    python build_bundle.py
"""

import os
import sys
import shutil
import subprocess
from datetime import datetime

def print_header(text):
    """打印标题"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def run_command(cmd, description):
    """执行命令并显示进度"""
    print(f"\n[正在] {description}...")
    print(f"命令: {cmd}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"[完成] {description}")
        if result.stdout:
            print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
        return True
    else:
        print(f"[失败] {description}")
        print(f"错误输出: {result.stderr}")
        return False

def main():
    """主函数"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print_header("EDIST v3.2 完整打包工具")
    print(f"工作目录: {script_dir}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 输出目录
    output_dir = os.path.join(script_dir, 'build', 'EDIST_v3.2')
    dist_dir = os.path.join(script_dir, 'dist')
    
    # Step 1: 清理旧的构建文件
    print_header("Step 1/4: 清理旧文件")
    dirs_to_clean = [
        os.path.join(script_dir, 'build', 'EDIST'),
        os.path.join(script_dir, 'dist', 'EDIST'),
        output_dir,
        os.path.join(dist_dir, 'updater'),
    ]
    
    for d in dirs_to_clean:
        if os.path.exists(d):
            try:
                shutil.rmtree(d)
                print(f"  已删除: {os.path.basename(d)}")
            except Exception as e:
                print(f"  警告: 无法删除 {d}: {e}")
    
    # Step 2: 打包主程序 EDIST.py
    print_header("Step 2/4: 打包主程序 (EDIST.exe)")
    
    main_spec = os.path.join(script_dir, 'EDIST.spec')
    
    # 检查 spec 文件是否存在
    if not os.path.exists(main_spec):
        print("[错误] 未找到 EDIST.spec 文件")
        print("请确保 EDIST.spec 存在于项目根目录")
        return False
    
    success = run_command(
        f'pyinstaller --noconfirm --distpath "{dist_dir}" --workpath "{os.path.join(script_dir, "build")}" "{main_spec}"',
        "PyInstaller 打包主程序"
    )
    
    if not success:
        print("\n[错误] 主程序打包失败！")
        return False
    
    # Step 3: 打包更新器 updater.py
    print_header("Step 3/4: 打包更新器 (updater.exe)")
    
    updater_script = os.path.join(script_dir, 'fwq', 'updater.py')
    
    if not os.path.exists(updater_script):
        print(f"[错误] 未找到更新器脚本: {updater_script}")
        return False
    
    success = run_command(
        f'pyinstaller --onefile --console --name updater --distpath "{dist_dir}" --workpath "{os.path.join(script_dir, "build", "updater_build")}" "{updater_script}"',
        "PyInstaller 打包更新器"
    )
    
    if not success:
        print("\n[错误] 更新器打包失败！")
        return False
    
    # Step 4: 合并到最终目录
    print_header("Step 4/4: 合并文件到输出目录")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 复制主程序文件
    edist_dist = os.path.join(dist_dir, 'EDIST')
    if os.path.exists(edist_dist):
        print(f"\n  复制主程序文件...")
        for item in os.listdir(edist_dist):
            src = os.path.join(edist_dist, item)
            dst = os.path.join(output_dir, item)
            
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
                print(f"    [DIR]  {item}/")
            else:
                shutil.copy2(src, dst)
                print(f"    [FILE] {item}")
    
    # 复制 updater.exe (--onefile 模式会直接输出到 dist/ 根目录)
    updater_exe = os.path.join(dist_dir, 'updater.exe')
    if not os.path.exists(updater_exe):
        # 备选路径：dist/updater/updater.exe
        updater_exe = os.path.join(dist_dir, 'updater', 'updater.exe')
    if os.path.exists(updater_exe):
        shutil.copy2(updater_exe, os.path.join(output_dir, 'updater.exe'))
        print(f"    [FILE] updater.exe [OK]")
    else:
        print(f"    [警告] 未找到 updater.exe")
    
    # 显示结果
    print_header("打包完成！")
    
    print(f"\n输出目录: {output_dir}\n")
    print("生成的文件:")
    print("-" * 50)
    
    if os.path.exists(output_dir):
        for item in sorted(os.listdir(output_dir)):
            item_path = os.path.join(output_dir, item)
            size = os.path.getsize(item_path)
            
            if os.path.isfile(item_path):
                size_str = f"{size / (1024*1024):.2f} MB"
                print(f"  [FILE] {item:<30} {size_str:>10}")
            else:
                print(f"  [DIR]  {item}/")
        
        print("-" * 50)
        
        # 计算总大小
        total_size = sum(
            os.path.getsize(os.path.join(output_dir, f))
            for f in os.listdir(output_dir)
            if os.path.isfile(os.path.join(output_dir, f))
        )
        print(f"\n总大小: {total_size / (1024*1024):.2f} MB")
    
    print("\n[OK] 打包成功！")
    print(f"位置: {output_dir}")
    print("\n使用方法:")
    print("  1. 将整个 EDIST_v3.2 文件夹分发给用户")
    print("  2. 用户运行 EDIST.exe 启动程序")
    print("  3. 自动更新时，updater.exe 会自动被调用")
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n用户取消操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n严重错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")
        sys.exit(1)
