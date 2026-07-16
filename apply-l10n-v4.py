#!/usr/bin/env python3
"""Hermes Agent L10n v4 — 全量补丁：main.py + commands.py + SOUL.md"""
import re, os, subprocess

AGENT_DIR = os.path.expanduser("~/.hermes/hermes-agent")
PATCH_PATH = os.path.expanduser("~/hermes-chinese/hermes-chinese.patch")
SOUL_PATH = os.path.expanduser("~/.hermes/SOUL.md")

print("=" * 55)
print("  Hermes Agent L10n v4 — 补全翻译")
print("=" * 55)

# ===== Step 1: Try git apply first =====
print("\n→ 尝试 git apply --recount ...")
result = subprocess.run(
    ["git", "apply", "--recount", PATCH_PATH],
    cwd=AGENT_DIR,
    capture_output=True, text=True
)
if result.returncode == 0:
    print("  ✓ git apply 成功！")
else:
    print(f"  ⚠ git apply 失败: {result.stderr.split(chr(10))[0]}")
    print("  → 改用字符串替换...")

    # ===== Step 2: Read patch =====
    with open(PATCH_PATH, "r", encoding="utf-8") as f:
        patch = f.read()

    # ===== Step 3: Build translation maps =====
    # help= from main.py
    minus_h = re.findall(r'^-(?:.*?)(?:help|description)="([^"]+)"', patch, re.MULTILINE)
    plus_h  = re.findall(r'^\+(?:.*?)(?:help|description)="([^"]+)"', patch, re.MULTILINE)
    
    # Tight extraction: find adjacent -/+ pairs in the diff
    lines = patch.split('\n')
    replacements = {}
    for i in range(len(lines)-1):
        if lines[i].startswith('-') and not lines[i].startswith('---'):
            for j in range(i+1, min(i+5, len(lines))):
                if lines[j].startswith('+') and not lines[j].startswith('+++'):
                    # Extract key=value pairs
                    old = re.search(r'(help|description)="([^"]*)"', lines[i])
                    new = re.search(r'(help|description)="([^"]*)"', lines[j])
                    if old and new and old.group(2) != new.group(2):
                        key = f'{old.group(1)}="{old.group(2)}"'
                        val = f'{new.group(1)}="{new.group(2)}"'
                        replacements[key] = val
                    break

    print(f"  → 提取到 {len(replacements)} 条翻译映射")

    # ===== Step 4: Apply to main.py =====
    main_path = os.path.join(AGENT_DIR, "hermes_cli", "main.py")
    if os.path.exists(main_path):
        with open(main_path, "r", encoding="utf-8") as f:
            content = f.read()
        count = 0
        for old, new in replacements.items():
            if old in content:
                content = content.replace(old, new)
                count += 1
        with open(main_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✓ main.py: 翻译 {count} 条")
    else:
        print(f"  ✗ main.py 未找到: {main_path}")

    # ===== Step 5: Apply to commands.py =====
    cmd_path = os.path.join(AGENT_DIR, "hermes_cli", "commands.py")
    if os.path.exists(cmd_path):
        # Commands.py uses a different format: CommandDef("name", "description", ...)
        minus_cmd = re.findall(r'^-.*?CommandDef\("[^"]*",\s*"([^"]*)"', patch, re.MULTILINE)
        plus_cmd  = re.findall(r'^\+.*?CommandDef\("[^"]*",\s*"([^"]*)"', patch, re.MULTILINE)
        cmd_map = {}
        for i in range(min(len(minus_cmd), len(plus_cmd))):
            if minus_cmd[i] != plus_cmd[i]:
                cmd_map[minus_cmd[i]] = plus_cmd[i]
        
        with open(cmd_path, "r", encoding="utf-8") as f:
            content = f.read()
        count = 0
        for old, new in cmd_map.items():
            # Match: CommandDef("name", "old_description", ...)
            pattern = f'CommandDef("[^"]*", "{re.escape(old)}"'
            matches = list(re.finditer(pattern, content))
            if matches:
                # Replace the description part
                for m in matches:
                    full = m.group(0)
                    idx = full.index(f'"{old}"')
                    new_full = full[:idx] + f'"{new}"' + full[idx+len(old)+2:]
                    content = content.replace(full, new_full)
                    count += 1
        with open(cmd_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✓ commands.py: 翻译 {count} 条")
    else:
        print(f"  ✗ commands.py 未找到: {cmd_path}")

# ===== Step 6: SOUL.md =====
with open(SOUL_PATH, "w", encoding="utf-8") as f:
    f.write("You ALWAYS respond in Simplified Chinese (简体中文).\n")
print("  ✓ SOUL.md: 已写入中文语言指令")

# ===== Step 7: Verify =====
print("\n🔍 验证翻译...")
main_path = os.path.join(AGENT_DIR, "hermes_cli", "main.py")
if os.path.exists(main_path):
    with open(main_path, "r") as f:
        c = f.read()
    helps = re.findall(r'help="([^"]*)"', c)
    cn = [h for h in helps if re.search(r'[\u4e00-\u9fff]', h)]
    print(f"  main.py: {len(cn)}/{len(helps)} 条 help= 已汉化")
    if cn:
        print(f"  示例: help=\"{cn[0][:50]}...\"")

cmd_path = os.path.join(AGENT_DIR, "hermes_cli", "commands.py")
if os.path.exists(cmd_path):
    with open(cmd_path, "r") as f:
        c = f.read()
    descs = re.findall(r'CommandDef\("[^"]*",\s*"([^"]*)"', c)
    cn = [d for d in descs if re.search(r'[\u4e00-\u9fff]', d)]
    print(f"  commands.py: {len(cn)}/{len(descs)} 条命令描述已汉化")

if os.path.exists(SOUL_PATH):
    with open(SOUL_PATH, "r") as f:
        if "Simplified Chinese" in f.read():
            print("  SOUL.md: ✓")

print("\n✅ 汉化完成！重启 Hermes 即可查看效果")
print("💡 hermes update 后会覆盖，重新运行此脚本即可恢复")