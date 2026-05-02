# fix_text_display.py - 修复 EDIST.py 中的异常字符显示
"""
问题: [xxx] 方括号标记在某些字体下显示异常
解决: 替换为简洁的英文单词或直接使用中文
"""

# 读取文件
with open('EDIST.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("Starting text display fix...")
print("="*60)

replacements = {
    # 菜单和按钮文字 - 使用简洁英文
    '[更新]': 'Update',
    '[下载]': 'Download',
    '[新!]': 'NEW',
    '[列表]': 'Templates',
    '[工具]': 'Test',
    '[搜索]': 'Checking',
    '[游戏]': 'ADMIN',
    
    # 提示信息中的标记 - 删除或简化
    '[!][电脑]': '',
    '[电脑]': '',
    '[>>]': '',
    '[文件夹]': '',
    '[画笔]': 'Modern',
    '[主题]': 'Theme',
    '[手机]': '',
    '[锁]': '',
    '[瓜]': 'Honeydew',
    '[月]': 'Dark',
    '[波浪]': 'Blue',
    '[花]': 'Pink',
    '[皇冠]': 'Admin',
    '[灯泡]': 'Tips',
    '[图表]': '',
    '[!]': '!',
}

count = 0

for old_text, new_text in replacements.items():
    if old_text in content:
        occurrences = content.count(old_text)
        content = content.replace(old_text, new_text)
        count += occurrences
        print(f"  [OK] '{old_text}' -> '{new_text}' (x{occurrences})")

# 写回文件
with open('EDIST.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "="*60)
print(f"Total replacements: {count}")
print(f"File saved successfully!")
print("="*60)
