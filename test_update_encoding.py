#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试自动更新功能的编码处理
"""

import sys
import os
import urllib.request
import urllib.error
import urllib.parse
import ssl
import json

def safe_encode_header(value):
    """
    安全编码HTTP头值，确保只包含ASCII字符
    
    Args:
        value: 原始字符串（可能包含中文或特殊字符）
    
    Returns:
        str: 安全的ASCII字符串
    """
    if not value:
        return ''
    
    # 如果已经是纯ASCII，直接返回
    try:
        value.encode('ascii')
        return value
    except UnicodeEncodeError:
        # 包含非ASCII字符，进行URL编码或移除
        # 方案1：使用URL编码（推荐用于查询参数）
        encoded = urllib.parse.quote(value, safe='')
        
        # 方案2：只保留ASCII可打印字符（用于Header）
        safe_value = ''.join(
            char if ord(char) < 128 and char.isprintable() else ''
            for char in value
        )
        
        # 如果过滤后为空，使用URL编码版本
        return safe_value if safe_value else encoded


def test_encoding():
    """测试各种字符串的编码安全性"""
    
    test_cases = [
        ('X反极域/3.2', '中文User-Agent'),
        ('XAntiDomain/3.2', '英文User-Agent'),
        ('Test/3.2 测试版', '混合中英文'),
        ('', '空字符串'),
        ('Special@#$%^&*()', '特殊字符'),
        ('Emoji🎉😊', 'Emoji表情'),
        ('Unicode测试_中文_日本語', '多语言混合'),
    ]
    
    print("=" * 60)
    print("🧪 编码安全测试")
    print("=" * 60)
    
    all_passed = True
    
    for test_input, description in test_cases:
        print(f"\n📝 测试: {description}")
        print(f"   原始值: {test_input!r}")
        
        # 使用safe_encode_header处理
        safe_value = safe_encode_header(test_input)
        print(f"   安全值: {safe_value!r}")
        
        # 验证是否可以安全编码为ASCII
        try:
            safe_value.encode('ascii')
            status = "✅ 通过"
        except UnicodeEncodeError:
            status = "❌ 失败"
            all_passed = False
        
        print(f"   状态: {status}")
        
        # 尝试在HTTP请求中使用（模拟）
        try:
            headers = {
                'User-Agent': safe_value,
                'Accept': 'application/json'
            }
            
            # 创建Request对象（不实际发送）
            req = urllib.request.Request('http://example.com', headers=headers)
            status = "✅ HTTP Request创建成功"
        except Exception as e:
            status = f"❌ HTTP Request失败: {e}"
            all_passed = False
        
        print(f"   HTTP: {status}")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 所有测试通过！编码问题已解决")
        return True
    else:
        print("❌ 存在失败的测试项！需要进一步检查")
        return False


def test_actual_request():
    """测试实际的HTTP请求（使用你的服务器地址）"""
    
    print("\n" + "=" * 60)
    print("🌐 实际HTTP请求测试")
    print("=" * 60)
    
    update_url = "https://347735.xyz/genxin/"
    current_version = "3.2"
    
    # 使用安全的User-Agent
    user_agent = f'XAntiDomain/{current_version}'
    
    print(f"\n📡 目标URL: {update_url}")
    print(f"🏷️  User-Agent: {user_agent}")
    
    try:
        # 创建SSL上下文
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        # 构建安全的请求头
        req = urllib.request.Request(
            update_url,
            headers={
                'User-Agent': safe_encode_header(user_agent),
                'Accept': safe_encode_header('application/json'),
                'Accept-Language': safe_encode_header('zh-CN,zh;q=0.9,en;q=0.8'),
                'Cache-Control': safe_encode_header('no-cache')
            }
        )
        
        print("\n⏳ 正在发送请求...")
        
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            content_type = response.headers.get('Content-Type', '')
            status_code = response.status
            
            print(f"\n✅ 请求成功!")
            print(f"   状态码: {status_code}")
            print(f"   Content-Type: {content_type}")
            
            # 读取响应内容
            content = response.read().decode('utf-8', errors='ignore')
            
            try:
                data = json.loads(content)
                print(f"\n📦 响应数据 (JSON):")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
                
                # 检查关键字段
                version = data.get('version') or data.get('latest') or data.get('tag_name', '')
                download = data.get('download') or data.get('url') or data.get('zipball_url', '')
                
                print(f"\n🔍 解析结果:")
                print(f"   最新版本: {version}")
                print(f"   下载链接: {download[:80]}..." if len(download) > 80 else f"   下载链接: {download}")
                
                return True
                
            except json.JSONDecodeError:
                print(f"\n⚠️  响应不是有效的JSON格式")
                print(f"   响应内容预览: {content[:200]}")
                return False
                
    except urllib.error.URLError as e:
        print(f"\n❌ 网络错误:")
        print(f"   错误类型: {type(e).__name__}")
        print(f"   错误信息: {str(e)}")
        print(f"\n💡 可能的原因:")
        print("   • 服务器不可达或未启动")
        print("   • URL地址错误")
        print("   • 网络连接问题")
        print("   • DNS解析失败")
        return False
        
    except Exception as e:
        print(f"\n❌ 未知错误:")
        print(f"   错误类型: {type(e).__name__}")
        print(f"   错误信息: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("自动更新编码问题诊断工具")
    print("=" * 60 + "\n")
    
    # 测试1：编码安全性
    encoding_ok = test_encoding()
    
    # 测试2：实际HTTP请求
    request_ok = test_actual_request()
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    print(f"   编码测试: {'✅ 通过' if encoding_ok else '❌ 失败'}")
    print(f"   HTTP测试: {'✅ 成功' if request_ok else '❌ 失败'}")
    
    if encoding_ok and request_ok:
        print("\n[OK] 所有测试通过！编码问题已完全解决！")
        return 0
    else:
        print("\n[WARNING] 部分测试失败，请检查网络或配置")
        return 1


if __name__ == '__main__':
    sys.exit(main())
