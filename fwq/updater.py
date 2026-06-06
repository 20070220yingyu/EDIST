# updater.py - EDIST 独立更新器
"""
EDIST Auto Updater - 独立更新程序

功能:
1. 接收新版本目录和目标目录参数
2. 等待主程序完全退出
3. 将新版本文件复制/覆盖到目标目录
4. 自动重启主程序

用法:
    updater.exe <new_version_dir> <target_dir>

参数:
    new_version_dir: 解压后的临时目录（新版本文件所在）
    target_dir: 当前程序所在目录（需要被更新的目录）
"""

import sys
import os
import time
import shutil
import subprocess
import logging
from datetime import datetime

def setup_logging():
    """配置日志系统"""
    log_file = os.path.join(os.path.dirname(sys.executable), 'updater.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file, mode='a', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

logger = setup_logging()

def wait_for_process_exit(process_name, max_wait=30, interval=1):
    """
    等待指定进程完全退出
    
    Args:
        process_name: 进程名称 (如 'EDIST.exe')
        max_wait: 最大等待时间（秒）
        interval: 检查间隔（秒）
    
    Returns:
        bool: 进程是否已退出
    """
    logger.info(f"等待进程 {process_name} 退出 (最多 {max_wait} 秒)...")
    
    waited = 0
    while waited < max_wait:
        # 检查进程是否还在运行
        try:
            result = subprocess.run(
                ['tasklist', '/FI', f'IMAGENAME eq {process_name}', '/NH'],
                stdout=subprocess.PIPE,  # 兼容 Python 3.6
                stderr=subprocess.PIPE,
                universal_newlines=True,  # 等同于 text=True (Python 3.6 兼容)
                timeout=5
            )
            
            if process_name not in result.stdout:
                logger.info(f"✓ 进程 {process_name} 已退出")
                return True
                
        except Exception as e:
            logger.warning(f"检查进程时出错: {e}")
        
        time.sleep(interval)
        waited += interval
    
    logger.warning(f"⚠ 等待 {max_wait} 秒后进程仍在运行，继续执行更新...")
    return False

def backup_current_version(target_dir):
    """
    备份当前版本
    
    Args:
        target_dir: 目标目录
    
    Returns:
        str: 备份目录路径，失败返回 None
    """
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = os.path.join(os.path.dirname(target_dir), f'backup_{timestamp}')
        
        logger.info(f"正在备份当前版本到: {backup_dir}")
        shutil.copytree(target_dir, backup_dir)
        
        logger.info(f"✓ 备份完成: {backup_dir}")
        return backup_dir
        
    except Exception as e:
        logger.error(f"备份失败: {e}")
        return None

def update_files(new_dir, target_dir):
    """
    将新版本文件复制/覆盖到目标目录

    Args:
        new_dir: 新版本文件所在目录
        target_dir: 目标目录（需要被更新的目录）

    Returns:
        bool: 是否成功
    """
    try:
        if not os.path.exists(new_dir):
            raise FileNotFoundError(f"新版本目录不存在: {new_dir}")

        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
            logger.info(f"创建目标目录: {target_dir}")

        items = os.listdir(new_dir)
        if len(items) == 1:
            single_item = os.path.join(new_dir, items[0])
            if os.path.isdir(single_item):
                logger.info(f"检测到单层目录包装 '{items[0]}'，使用内层目录作为源")
                new_dir = single_item

        logger.info("开始更新文件...")
        updated_files = []
        skipped_files = []

        for item in os.listdir(new_dir):
            src = os.path.join(new_dir, item)
            dst = os.path.join(target_dir, item)

            if os.path.basename(src).lower() == 'updater.exe':
                logger.info(f"跳过 updater.exe 自身")
                continue

            try:
                if os.path.isdir(src):
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                    updated_files.append(f"[DIR]  {item}/")
                else:
                    shutil.copy2(src, dst)
                    updated_files.append(f"[FILE] {item}")

            except PermissionError as e:
                logger.warning(f"跳过 (权限不足): {item} - {e}")
                skipped_files.append(item)
            except Exception as e:
                logger.error(f"失败: {item} - {e}")
                skipped_files.append(item)

        logger.info(f"✓ 文件更新完成")
        logger.info(f"  成功: {len(updated_files)} 个项目")

        if updated_files:
            logger.debug("更新的文件列表:")
            for f in updated_files[:10]:
                logger.debug(f"  + {f}")
            if len(updated_files) > 10:
                logger.debug(f"  ... 还有 {len(updated_files) - 10} 个文件")

        if skipped_files:
            logger.warning(f"  跳过: {len(skipped_files)} 个项目")
            for f in skipped_files:
                logger.warning(f"  - {f}")

        return len(skipped_files) == 0

    except Exception as e:
        logger.error(f"更新文件失败: {e}")
        return False

def cleanup_temp_directory(temp_dir):
    """清理临时目录"""
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
            logger.info(f"✓ 清理临时目录: {temp_dir}")
    except Exception as e:
        logger.warning(f"清理临时目录失败: {e}")

def launch_main_program(target_dir):
    """
    启动主程序
    
    Args:
        target_dir: 主程序所在目录
    
    Returns:
        bool: 是否成功启动
    """
    possible_exe_names = [
        'EDIST.exe',
        'EDIST.py',  # 源码模式
        'X反极域v3.2.exe'  # 兼容旧版
    ]
    
    for exe_name in possible_exe_names:
        exe_path = os.path.join(target_dir, exe_name)
        
        if os.path.exists(exe_path):
            try:
                logger.info(f"正在启动主程序: {exe_path}")
                
                if exe_name.endswith('.py'):
                    # Python 源码模式
                    subprocess.Popen([sys.executable, exe_path], cwd=target_dir)
                else:
                    # EXE 模式
                    subprocess.Popen([exe_path], cwd=target_dir)
                
                logger.info(f"✓ 主程序已启动: {exe_path}")
                return True
                
            except Exception as e:
                logger.error(f"启动主程序失败 ({exe_name}): {e}")
                continue
    
    logger.error("未找到可执行的主程序文件")
    return False

def main():
    """主函数"""
    print("="*60)
    print("EDIST Auto Updater v1.0")
    print("="*60)
    
    # 参数验证
    if len(sys.argv) != 3:
        print("用法: updater.exe <new_version_dir> <target_dir>")
        print("\n参数:")
        print("  new_version_dir - 解压后的新版本目录")
        print("  target_dir     - 当前程序安装目录")
        input("\\n按任意键退出...")
        sys.exit(1)
    
    new_dir = sys.argv[1]       # 解压后的临时目录（新版本文件所在）
    target_dir = sys.argv[2]    # 当前程序所在目录（需要被更新的目录）
    
    logger.info(f"新版本目录: {new_dir}")
    logger.info(f"目标目录:   {target_dir}")
    
    # 验证目录存在
    if not os.path.exists(new_dir):
        logger.error(f"错误: 新版本目录不存在: {new_dir}")
        input("按任意键退出...")
        sys.exit(1)
    
    if not os.path.exists(target_dir):
        logger.warning(f"警告: 目标目录不存在，将创建: {target_dir}")
    
    # Step 1: 等待主程序完全退出
    print("\n[Step 1/5] 等待主程序退出...")
    wait_for_process_exit('EDIST.exe', max_wait=30)
    time.sleep(2)  # 额外等待2秒确保文件释放
    
    # Step 2: 备份当前版本
    print("[Step 2/5] 备份当前版本...")
    backup_dir = backup_current_version(target_dir)
    
    # Step 3: 复制新版本文件
    print("[Step 3/5] 更新文件...")
    success = update_files(new_dir, target_dir)
    
    if not success:
        logger.error("⚠ 部分文件更新失败！")
    
    # Step 4: 清理临时文件
    print("[Step 4/5] 清理临时文件...")
    cleanup_temp_directory(new_dir)
    
    # Step 5: 启动新版本
    print("[Step 5/5] 启动新版本...")
    launch_success = launch_main_program(target_dir)
    
    if launch_success:
        print("\n" + "="*60)
        print("✓ 更新完成！主程序已自动启动")
        print("="*60)
        logger.info("✓ 更新流程完成")
    else:
        print("\n" + "="*60)
        print("⚠ 更新完成但未能自动启动主程序")
        print("请手动启动程序")
        print("="*60)
        logger.warning("更新完成但未能自动启动主程序")
        input("\\n按任意键退出...")
    
    # 延迟退出，让用户看到结果
    time.sleep(3)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.critical(f"更新器发生严重错误: {e}", exc_info=True)
        print(f"\n严重错误: {e}")
        input("\\n按任意键退出...")
        sys.exit(1)
