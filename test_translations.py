import sys, os, json

base_path = os.path.dirname(os.path.abspath(__file__))
lang_code = 'zh_CN'
lang_path = os.path.join(base_path, 'languages', f'{lang_code}.json')

with open(lang_path, 'r', encoding='utf-8') as f:
    translations = json.load(f)

test_cases = [
    'app.title', 'menu.version_select', 'menu.version_2016', 'menu.version_2022', 'menu.about_software',
    'buttons.kill_jy', 'buttons.detect_ip', 'buttons.lock_all', 'buttons.lock_target',
    'buttons.open', 'buttons.send', 'buttons.execute',
    'buttons.choose_file', 'buttons.upload_execute',
    'buttons.shutdown', 'buttons.reboot', 'buttons.lock_screen', 'buttons.sign_in',
    'labels.target_ip', 'labels.ip_count',
    'labels.open_program', 'labels.send_message', 'labels.execute_command', 'labels.file_upload',
    'programs.cmd', 'programs.calculator', 'programs.notepad', 'programs.paint',
    'status.ready', 'status.executing',
    'themes.honeydew', 'themes.dark', 'themes.blue', 'themes.pink',
    'language.zh_CN', 'language.en_US',
    'confirmations.danger_title', 'confirmations.yes', 'confirmations.no',
    'messages.no_target_ip'
]

errors = []
for key in test_cases:
    parts = key.split('.')
    val = translations
    for p in parts:
        if isinstance(val, dict) and p in val:
            val = val[p]
        else:
            errors.append(key)
            break
    else:
        if not isinstance(val, str):
            errors.append(f'{key} (not string: {type(val).__name__})')

if errors:
    print('MISSING KEYS:')
    for e in errors:
        print(f'  [FAIL] {e}')
    sys.exit(1)
else:
    print(f'ALL {len(test_cases)} translation keys OK')
    for key in ['app.title', 'buttons.kill_jy', 'labels.target_ip', 'themes.honeydew', 'language.zh_CN']:
        parts = key.split('.')
        val = translations
        for p in parts:
            val = val[p]
        print(f'  {key} -> {val}')

print()
print('Language file is valid and all keys are present.')
