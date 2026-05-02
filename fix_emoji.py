# fix_emoji.py - 修复 EDIST.py 中的 Tcl/Tk 不兼容字符
"""
问题: Tkinter/Tcl 只支持 U+0000-U+FFFF 范围内的 Unicode 字符
修复: 将所有 emoji (U+1Fxxx) 替换为安全的文本或简单符号
"""

import re
import sys

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8')

# 读取文件
with open('EDIST.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("Starting emoji fix...")
print("="*60)

count = 0

# 定义替换规则 (使用正则表达式匹配高位Unicode)
emoji_patterns = [
    # 格式: (pattern, replacement, description)
    (r'[\U0001f504]', '[更新]', 'clockwise arrow'),
    (r'[\U0001f4e5]', '[下载]', 'inbox tray'),
    (r'[\U0001f389]', '[新!]', 'party popper'),
    (r'[\U0001f4cb]', '[列表]', 'clipboard'),
    (r'[\U0001f527]', '[工具]', 'wrench'),
    (r'[\U0001f50d]', '[搜索]', 'magnifier'),
    (r'[\U0001f3ae]', '[游戏]', 'joystick'),
    (r'[\U0001f5a5\U0001f5a5\ufe0f]', '[电脑]', 'computer'),
    (r'[\U0001f310]', '[网络]', 'globe'),
    (r'[\U0001f6e1\U0001f6e1\ufe0f]', '[安全]', 'shield'),
    (r'[\U0001f680]', '[>>]', 'rocket'),
    (r'[\U0001f4c1]', '[文件夹]', 'folder'),
    (r'[\U0001f3a8]', '[画笔]', 'palette'),
    (r'[\U0001f3ad]', '[主题]', 'masks'),
    (r'[\U0001f4f1]', '[手机]', 'mobile phone'),
    (r'[\U0001f512]', '[锁]', 'lock'),
    (r'[\U0001f348]', '[瓜]', 'melon'),
    (r'[\U0001f311]', '[月]', 'moon'),
    (r'[\U0001f30a]', '[波浪]', 'wave'),
    (r'[\U0001f338]', '[花]', 'cherry blossom'),
    (r'[\U0001f451]', '[皇冠]', 'crown'),
    (r'[\U0001f4a1]', '[灯泡]', 'light bulb'),
    (r'[\U0001f4ca]', '[图表]', 'bar chart'),
    (r'[\u26a0\ufe0f]', '[!]', 'warning sign'),  # ⚠️
]

for pattern, replacement, desc in emoji_patterns:
    matches = re.findall(pattern, content)
    if matches:
        num = len(matches)
        content = re.sub(pattern, replacement, content)
        count += num
        print(f"  [OK] {desc}: {num} occurrences -> {replacement}")

# 移除所有剩余的高位 Unicode 字符 (U+10000+)
high_unicode_pattern = r'[\U00010000-\U0010ffff]'
remaining_matches = re.findall(high_unicode_pattern, content)

if remaining_matches:
    print(f"\n  [WARN] Found {len(remaining_matches)} additional high-range chars")
    content = re.sub(high_unicode_pattern, '', content)
    count += len(remaining_matches)

# 写回文件
with open('EDIST.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "="*60)
print(f"Total replacements: {count}")
print(f"File saved successfully!")
print("="*60)
