# test_update_local.py - 本地自动更新测试工具
"""
功能:
1. 启动本地 HTTP 服务器模拟更新服务器
2. 创建测试用的更新包
3. 验证 EDIST 客户端能否正确检测和下载更新

用法:
    python test_update_local.py
"""

import os
import sys
import json
import zipfile
import hashlib
import shutil
import subprocess
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread

def create_test_environment():
    """创建测试环境"""
    print("="*60)
    print("Creating local test environment...")
    print("="*60)
    
    # 创建目录结构
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_server')
    genxin_dir = os.path.join(base_dir, 'genxin')
    downloads_dir = os.path.join(genxin_dir, 'downloads')
    
    for d in [base_dir, genxin_dir, downloads_dir]:
        if not os.path.exists(d):
            os.makedirs(d)
            print(f"  [OK] Created: {d}")
    
    # 复制 latest.php 到 genxin/
    src_php = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fwq', 'latest.php')
    dst_php = os.path.join(genxin_dir, 'latest.php')
    
    if os.path.exists(src_php):
        shutil.copy2(src_php, dst_php)
        print(f"  [OK] Copied: latest.php")
    else:
        print(f"  [WARN] Not found: {src_php}")
    
    # 创建一个假的更新包 (zip 文件)
    version = "3.3"
    zip_filename = f"EDIST-v{version}.zip"
    zip_path = os.path.join(downloads_dir, zip_filename)
    
    print(f"\n  Creating test update package: {zip_filename}")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # 添加一些假文件
        zf.writestr('EDIST.py', '# Test version 3.3\nprint("Updated!")\n')
        zf.writestr('config.json', '{"app": {"version": "3.3"}}\n')
        zf.writestr('README.txt', f'EDIST v{version} - Test Update Package\n')
        
        # 添加 languages 目录
        zf.writestr('languages/zh_CN.json', '{"app": {"title": "EDIST v3.3 [TEST]"}}')
        zf.writestr('languages/en_US.json', '{"app": {"title": "EDIST v3.3 [TEST]"}}')
        
        print(f"    + EDIST.py")
        print(f"    + config.json")
        print(f"    + languages/")
    
    # 生成 SHA256 校验值
    sha256_hash = hashlib.sha256()
    with open(zip_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256_hash.update(chunk)
    
    hash_value = sha256_hash.hexdigest()
    hash_file = zip_path + '.sha256'
    
    with open(hash_file, 'w') as f:
        f.write(hash_value)
    
    print(f"  [OK] Generated SHA256: {hash_value[:16]}...")
    
    print(f"\nTest environment ready!")
    print(f"  Server root: {base_dir}")
    print(f"  API URL: http://localhost:8080/genxin/latest.php")
    print(f"  Download URL: http://localhost:8080/genxin/downloads/{zip_filename}")
    
    return base_dir, genxin_dir, downloads_dir, version

class CustomHandler(SimpleHTTPRequestHandler):
    """自定义请求处理器"""
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"  [HTTP] {self.address_string()} - {format % args}")
    
    def end_headers(self):
        """添加 CORS 头"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

def start_server(base_dir):
    """启动 HTTP 服务器"""
    os.chdir(base_dir)
    
    server = HTTPServer(('localhost', 8080), CustomHandler)
    
    print("\n" + "="*60)
    print("Starting local update server...")
    print("="*60)
    print(f"  URL: http://localhost:8080/genxin/latest.php")
    print("  Press Ctrl+C to stop the server\n")
    
    # 在新线程中运行服务器
    server_thread = Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    
    time.sleep(1)  # 等待服务器启动
    
    return server

def test_api():
    """测试 API 是否正常工作"""
    import urllib.request
    
    print("\n[TEST] Checking API endpoint...")
    
    try:
        url = 'http://localhost:8080/genxin/latest.php'
        req = urllib.request.Request(url)
        
        with urllib.request.urlopen(req, timeout=5) as response:
            data = response.read().decode('utf-8')
            
        result = json.loads(data)
        
        if result.get('success'):
            print(f"  [PASS] API returned success!")
            print(f"  Version: {result.get('version')}")
            print(f"  Download: {result.get('download_url')}")
            print(f"  Filename: {result.get('filename')}")
            return True
        else:
            print(f"  [FAIL] API returned error:")
            print(f"  Error: {result.get('error')}")
            if result.get('debug'):
                print(f"  Debug: {json.dumps(result['debug'], indent=2)}")
            return False
            
    except Exception as e:
        print(f"  [FAIL] Request failed: {e}")
        return False

def modify_config_for_test():
    """临时修改 config.json 使用本地服务器"""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    
    # 备份原配置
    backup_path = config_path + '.backup'
    if not os.path.exists(backup_path):
        shutil.copy2(config_path, backup_path)
        print(f"\n[CONFIG] Backed up original config to: {backup_path}")
    
    # 读取并修改
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    old_url = config.get('features', {}).get('update_server_url', '')
    config['features']['update_server_url'] = 'http://localhost:8080/genxin/latest.php'
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
    
    print(f"[CONFIG] Changed update URL:")
    print(f"  From: {old_url}")
    print(f"  To:   http://localhost:8080/genxin/latest.php")

def restore_config():
    """恢复原始配置"""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    backup_path = config_path + '.backup'
    
    if os.path.exists(backup_path):
        shutil.copy2(backup_path, config_path)
        print(f"\n[CONFIG] Restored original configuration")
        os.remove(backup_path)

def main():
    """主函数"""
    try:
        # Step 1: 创建测试环境
        base_dir, genxin_dir, downloads_dir, version = create_test_environment()
        
        # Step 2: 启动服务器
        server = start_server(base_dir)
        
        # Step 3: 测试 API
        api_ok = test_api()
        
        if not api_ok:
            print("\n[ERROR] API test failed! Please check the error messages above.")
            input("\nPress Enter to exit...")
            return
        
        # Step 4: 修改客户端配置
        modify_config_for_test()
        
        print("\n" + "="*60)
        print("Environment is ready!")
        print("="*60)
        print("""
Next steps:
1. Open another terminal and run:
   cd f:\\fanjiyu-3.0-main
   python EDIST.py
   
2. In EDIST, click menu -> Check for Updates
   
3. You should see a new version v{version} available!

4. When done testing, press Ctrl+C here to stop server.
   The original config will be restored automatically.
""".format(version=version))
        
        # 等待用户操作
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        
    finally:
        # 清理和恢复
        print("\n\nCleaning up...")
        restore_config()
        
        # 可选: 删除测试目录
        # test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_server')
        # if os.path.exists(test_dir):
        #     shutil.rmtree(test_dir)
        #     print(f"Removed test directory: {test_dir}")
        
        print("\nDone! Original configuration restored.")

if __name__ == '__main__':
    main()
