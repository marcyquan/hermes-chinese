#!/usr/bin/env python3
"""Hermes Agent L10n v5 — 全量汉化：main.py + commands.py + SOUL.md"""
import re, os

AGENT_DIR = os.path.expanduser("~/.hermes/hermes-agent")
SOUL_PATH = os.path.expanduser("~/.hermes/SOUL.md")

# ===== 完整翻译映射 =====
HELP_MAP = {
    # MoA
    "Configure Mixture of Agents provider/model slots": "配置 Mixture of Agents 供应商/模型槽位",
    "Show current MoA model slots": "显示当前 MoA 模型槽位",
    "Interactively pick MoA models": "交互式选择 MoA 模型",
    "Preset name to create or update": "要创建或更新的预设名称",
    "Delete a MoA preset": "删除 MoA 预设",
    "Preset name to delete": "要删除的预设名称",
    # Secret management
    "Manage external secret sources (Bitwarden, 1Password)": "管理外部密钥源（Bitwarden、1Password）",
    "1Password (op:// references) integration": "1Password（op:// 引用）集成",
    # WhatsApp
    "Set up WhatsApp Business Cloud API integration": "设置 WhatsApp Business Cloud API 集成",
    # Checkpoints
    "Inspect / prune / clear ~/.hermes/checkpoints/": "检查/清理 ~/.hermes/checkpoints/",
    # Petdex
    "Browse, install, and select petdex animated pets": "浏览、安装和选择 petdex 动画宠物",
    # Timeline
    "Timeline of learned skills + memories over time": "技能和记忆的学习时间线",
    # Computer Use / CUA
    "Manage the Computer Use (cua-driver) backend (macOS/Windows/Linux)": "管理 Computer Use (cua-driver) 后端（macOS/Windows/Linux）",
    "Install or repair the cua-driver binary (macOS/Windows/Linux)": "安装或修复 cua-driver 二进制文件（macOS/Windows/Linux）",
    "Print whether cua-driver is installed and on PATH": "检查 cua-driver 是否已安装且在 PATH 中",
    "Run cua-driver `health_report` and surface the check matrix": "运行 cua-driver `health_report` 并展示检查矩阵",
    "Skip the listed checks. Repeat for multiple. Wins over --include.": "跳过列出的检查项，可重复使用，优先级高于 --include",
    "Emit the raw structured payload as JSON (same shape as `tools/call`).": "以 JSON 格式输出原始结构化负载",
    "Check or grant macOS Accessibility + Screen Recording (macOS)": "检查或授予 macOS 辅助功能+屏幕录制权限（macOS）",
    "Report Accessibility + Screen Recording grant state (read-only)": "报告辅助功能+屏幕录制授权状态（只读）",
    "Emit the normalized permission payload as JSON.": "以 JSON 格式输出标准化权限负载",
    "Request the grants (opens the dialog attributed to CuaDriver)": "请求授权（打开 CuaDriver 权限对话框）",
    # Sessions management
    "Manage session history (list, rename, export, prune, delete)": "管理会话历史（列出、重命名、导出、清理、删除）",
    "Only sessions in one workspace: a git repo root or project dir ": "仅匹配工作区中的会话：git 仓库根目录或项目目录 ",
    "Only match sessions started within the last AGE ": "仅匹配最近 AGE 时间内开始的会话 ",
    "Only match sessions started before TIME ": "仅匹配 TIME 之前开始的会话 ",
    "Only match sessions started at/after TIME ": "仅匹配 TIME 或之后开始的会话 ",
    "Only match sessions from this source": "仅匹配来自此来源的会话",
    "Only match sessions whose title contains this substring": "仅匹配标题包含此子串的会话",
    "Only match sessions with this end reason": "仅匹配具有此结束原因的会话",
    "Only match sessions whose working directory is under this path": "仅匹配工作目录在此路径下的会话",
    "Only match sessions with >= N messages": "仅匹配消息数 >= N 的会话",
    "Only match sessions with <= N messages": "仅匹配消息数 <= N 的会话",
    "Only match sessions whose model name contains this substring ": "仅匹配模型名称包含此子串的会话 ",
    "Only match sessions billed through this provider ": "仅匹配通过此提供商计费的会话 ",
    "Only match sessions from this user ID": "仅匹配来自此用户 ID 的会话",
    "Only match sessions from this chat/channel ID": "仅匹配来自此聊天/频道 ID 的会话",
    "Only match sessions with this chat type (e.g. dm, group)": "仅匹配此聊天类型（如私聊、群组）的会话",
    "Only match sessions whose git branch contains this substring": "仅匹配 git 分支包含此子串的会话",
    "Only match sessions with >= N total tokens (input+output)": "仅匹配总 token >= N 的会话",
    "Only match sessions with <= N total tokens (input+output)": "仅匹配总 token <= N 的会话",
    "Only match sessions costing >= N USD (actual or estimated)": "仅匹配花费 >= N USD 的会话",
    "Only match sessions costing <= N USD (actual or estimated)": "仅匹配花费 <= N USD 的会话",
    "Only match sessions with >= N tool calls": "仅匹配工具调用 >= N 次的会话",
    "Only match sessions with <= N tool calls": "仅匹配工具调用 <= N 次的会话",
    "List matching sessions without changing anything": "列出匹配的会话而不做任何更改",
    "Export sessions to JSONL, Markdown, or QMD": "将会话导出为 JSONL、Markdown 或 QMD",
    "trace --upload only: create/update a public dataset instead of private": "trace --upload 模式：创建/更新公开数据集而非私有",
    "Session ID or unique prefix to export": "要导出的会话 ID 或唯一前缀",
    "Redact secrets (API keys, tokens, credentials) from exported content": "从导出内容中隐藏密钥（API 密钥、令牌、凭证）",
    "md/qmd only: export one row or its compression lineage": "仅 md/qmd：导出一行或其压缩谱系",
    "md/qmd only: after verified single-session export, delete that session (needs --yes)": "仅 md/qmd：验证后删除该会话（需要 --yes）",
    "md/qmd only: overwrite an existing export file": "仅 md/qmd：覆盖现有导出文件",
    "Session ID to delete": "要删除的会话 ID",
    "Delete old sessions (filterable by time window, source, title, ...)": "删除旧会话（可按时间窗口、来源、标题等筛选）",
    "Also delete archived sessions (excluded by default)": "同时删除已归档会话（默认排除）",
    "Bulk-archive (soft-hide) sessions matching filters — no deletion": "批量归档匹配筛选的会话——不删除",
    "Reclaim disk space: merge FTS5 segments + VACUUM (no data change)": "回收磁盘空间：合并 FTS5 段 + VACUUM（数据不变）",
    "Repair a malformed state.db schema so hidden sessions reappear": "修复损坏的 state.db 架构，恢复隐藏会话",
    "Only report whether the database opens cleanly; do not modify it": "仅报告数据库是否能正常打开，不修改",
    "Skip the timestamped backup copy (not recommended)": "跳过带时间戳的备份副本（不推荐）",
    "Set or change a session's title": "设置或更改会话标题",
    "Session ID to rename": "要重命名的会话 ID",
    "New title for the session": "会话的新标题",
    "Interactive session picker — browse, search, and resume sessions": "交互式会话选择器——浏览、搜索和恢复会话",
    "Max sessions to load (default: 500)": "最多加载的会话数（默认：500）",
}

DESC_MAP = {
    "Configure the provider/model set used by /moa <prompt>.": "配置 /moa <prompt> 使用的供应商/模型集。",
}

CMD_MAP = {
    "Compose your next prompt in $EDITOR (markdown), then send it": "在 $EDITOR 中编写下一条提示（Markdown），然后发送",
    "Back up N user turns and re-prompt (default 1)": "备份 N 轮用户对话并重新提示（默认 1）",
    "Compress conversation context (add 'here [N]' to keep recent N turns; --preview shows what would happen)": "压缩对话上下文（添加 'here [N]' 保留最近 N 轮；--preview 预览效果）",
    "Open the learning journey timeline": "打开学习历程时间线",
    "Run one prompt through the default Mixture of Agents preset, then restore your model": "通过默认 MoA 预设运行一次提示，然后恢复模型",
    "Show session, model, token, and context info": "显示会话、模型、token 和上下文信息",
    "Switch model (persists by default)": "切换模型（默认持久化）",
    "Toggle [HH:MM] timestamps on messages and /history": "切换消息和 /history 的时间戳显示",
    "Review pending memory writes / toggle the approval gate": "审查待处理的内存写入/切换审批开关",
    "Toggle or adopt a petdex mascot (/pet, /pet list, /pet <slug>)": "切换或领养 petdex 吉祥物（/pet, /pet list, /pet <slug>）",
    "Generate a new petdex pet from a description": "从描述生成新的 petdex 宠物",
    "Learn a reusable skill from anything you describe (dirs, URLs, this chat, notes)": "从你描述的任何内容中学习可复用技能（目录、URL、本对话、笔记）",
    "Review suggested automations (accept/dismiss)": "审查建议的自动化（接受/忽略）",
    "Set up an automation from a blueprint template": "从蓝图模板设置自动化",
    "Show token usage and rate limits; `reset` redeems a banked Codex limit reset": "显示 token 用量和速率限制；`reset` 使用存储的 Codex 重置",
    "Show Nous credit balance and top up": "显示 Nous 积分余额并充值",
    "Manage Nous terminal billing — buy credits, auto-reload, limits": "管理 Nous 终端计费——购买积分、自动充值、限制",
    "Attach clipboard image from your clipboard": "从剪贴板附加图片",
    "Attach a local image file for your next prompt": "为下一条提示附加本地图片文件",
    "Update Hermes Agent to the latest version": "更新 Hermes Agent 到最新版本",
    "Show Hermes Agent version": "显示 Hermes Agent 版本",
    "Upload debug report (system info + logs) and get shareable links": "上传调试报告（系统信息+日志）并获取分享链接",
    "Exit the CLI (use --delete to also remove session history)": "退出 CLI（使用 --delete 同时删除会话历史）",
}

print("=" * 55)
print("  Hermes Agent L10n v5 — 补全翻译")
print("=" * 55)

# ===== Apply main.py =====
main_path = os.path.join(AGENT_DIR, "hermes_cli", "main.py")
h_count = d_count = 0
if os.path.exists(main_path):
    with open(main_path, "r", encoding="utf-8") as f:
        content = f.read()
    for eng, chn in HELP_MAP.items():
        old = f'help="{eng}"'
        new = f'help="{chn}"'
        if old in content:
            content = content.replace(old, new)
            h_count += 1
    for eng, chn in DESC_MAP.items():
        old = f'description="{eng}"'
        new = f'description="{chn}"'
        if old in content:
            content = content.replace(old, new)
            d_count += 1
    with open(main_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ main.py: 翻译 {h_count} 条 help= + {d_count} 条 description=")
else:
    print(f"  ✗ main.py 未找到")

# ===== Apply commands.py =====
cmd_path = os.path.join(AGENT_DIR, "hermes_cli", "commands.py")
c_count = 0
if os.path.exists(cmd_path):
    with open(cmd_path, "r", encoding="utf-8") as f:
        content = f.read()
    for eng, chn in CMD_MAP.items():
        old = f'"{eng}"'
        new = f'"{chn}"'
        if old in content:
            content = content.replace(old, new)
            c_count += 1
    with open(cmd_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ commands.py: 翻译 {c_count} 条")
else:
    print(f"  ✗ commands.py 未找到")

# ===== SOUL.md =====
with open(SOUL_PATH, "w", encoding="utf-8") as f:
    f.write("You ALWAYS respond in Simplified Chinese (简体中文).\n")
print("  ✓ SOUL.md: 已写入中文语言指令")

# ===== Verify =====
print("\n🔍 验证翻译...")

with open(main_path, "r") as f:
    c = f.read()
all_helps = re.findall(r'help="([^"]*)"', c)
cn_helps = [h for h in all_helps if re.search(r'[\u4e00-\u9fff]', h)]
en_helps = [h for h in all_helps if h and not re.search(r'[\u4e00-\u9fff]', h)]
print(f"  main.py help=: {len(cn_helps)}/{len(all_helps)} 条已汉化")
if en_helps:
    print(f"  剩余 {len(en_helps)} 条英文:")
    for h in en_helps:
        print(f'    "{h[:60]}"')

with open(cmd_path, "r") as f:
    c = f.read()
all_cmds = re.findall(r'CommandDef\("[^"]*",\s*"([^"]*)"', c)
cn_cmds = [d for d in all_cmds if re.search(r'[\u4e00-\u9fff]', d)]
en_cmds = [d for d in all_cmds if d and not re.search(r'[\u4e00-\u9fff]', d)]
print(f"  commands.py: {len(cn_cmds)}/{len(all_cmds)} 条已汉化")
if en_cmds:
    print(f"  剩余 {len(en_cmds)} 条英文:")
    for d in en_cmds:
        print(f'    "{d[:60]}"')

if os.path.exists(SOUL_PATH):
    with open(SOUL_PATH, "r") as f:
        if "Simplified Chinese" in f.read():
            print("  SOUL.md: ✓")

print(f"\n✅ 汉化完成！重启 Hermes 即可查看效果")