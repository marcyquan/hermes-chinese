#!/usr/bin/env python3
"""检查 Hermes 服务器上还有哪些英文 help= 和 command 描述未翻译"""
import re, os

AGENT_DIR = os.path.expanduser("~/.hermes/hermes-agent")

# main.py
main_path = os.path.join(AGENT_DIR, "hermes_cli", "main.py")
print("=== main.py 剩余英文 help= ===")
with open(main_path, "r") as f:
    c = f.read()
for m in re.finditer(r'help="([^"]*)"', c):
    s = m.group(1)
    if s and not re.findall(r'[\u4e00-\u9fff]', s):
        print(f'  help="{s}"')

print("\n=== main.py 剩余英文 description= ===")
for m in re.finditer(r'description="([^"]*)"', c):
    s = m.group(1)
    if s and not re.findall(r'[\u4e00-\u9fff]', s):
        print(f'  description="{s}"')

# commands.py
cmd_path = os.path.join(AGENT_DIR, "hermes_cli", "commands.py")
print("\n=== commands.py 剩余英文描述 ===")
with open(cmd_path, "r") as f:
    c = f.read()
for m in re.finditer(r'CommandDef\("[^"]*",\s*"([^"]*)"', c):
    s = m.group(1)
    if s and not re.findall(r'[\u4e00-\u9fff]', s):
        print(f'  CommandDef("...", "{s}", ...)')