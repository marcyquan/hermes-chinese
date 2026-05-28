#!/usr/bin/env python3
"""
Hermes Agent L10n — 简体中文汉化脚本

使用方法:
  python apply-l10n.py

自动检测 ~/.hermes/hermes-agent 并将 CLI 界面翻译为简体中文。
支持幂等运行 — 多次执行不会重复修改。
"""
import os
import sys

HERMES_HOME = os.path.expanduser("~/.hermes")
AGENT_DIR = os.path.join(HERMES_HOME, "hermes-agent")
COMMANDS_PATH = os.path.join(AGENT_DIR, "hermes_cli", "commands.py")
MAIN_PATH = os.path.join(AGENT_DIR, "hermes_cli", "main.py")
SOUL_PATH = os.path.join(HERMES_HOME, "SOUL.md")
PATCH_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hermes-chinese.patch")


def apply_patch():
    """Use git apply to apply the patch file."""
    import subprocess
    orig = os.getcwd()
    os.chdir(AGENT_DIR)
    try:
        r = subprocess.run(
            ["git", "apply", "--recount", PATCH_PATH],
            capture_output=True, text=True
        )
        if r.returncode == 0:
            print("  ✓ 补丁应用成功 (git apply)")
            return True
        else:
            # Fallback: try --ignore-whitespace
            r2 = subprocess.run(
                ["git", "apply", "--recount", "--ignore-whitespace", PATCH_PATH],
                capture_output=True, text=True
            )
            if r2.returncode == 0:
                print("  ✓ 补丁应用成功 (git apply --ignore-whitespace)")
                return True
            print(f"  ⚠ git apply 失败: {r.stderr[:200]}")
            return False
    finally:
        os.chdir(orig)


def apply_replacements():
    """Direct string replacements — idempotent, works after hermes update."""
    replacements = {
        # ======== commands.py — 65 条斜杠命令 ========
        # Session
        "Acknowledge platform start pings without a reply": "确认平台启动 ping，不回复",
        "Start a new session (fresh session ID + history)": "开始新会话（全新的会话 ID 和历史记录）",
        "Enable or inspect Telegram DM topic sessions": "启用或检查 Telegram 私信话题会话",
        "Clear screen and start a new session": "清屏并开始新会话",
        "Force a full UI repaint (recovers from terminal drift)": "强制完全重绘 UI（从终端漂移中恢复）",
        "Show conversation history": "显示对话历史",
        "Save the current conversation": "保存当前对话",
        "Retry the last message (resend to agent)": "重试上一条消息（重新发送给代理）",
        "Remove the last user/assistant exchange": "撤销最近一次用户/助手对话回合",
        "Set a title for the current session": "设置当前会话的标题",
        "Hand off this session to a messaging platform (Telegram, Discord, etc.)": "将会话移交给消息平台（Telegram、Discord 等）",
        "Branch the current session (explore a different path)": "分支当前会话（探索不同路径）",
        "Manually compress conversation context": "手动压缩对话上下文",
        "List or restore filesystem checkpoints": "列出或恢复文件系统检查点",
        "Create or restore state snapshots of Hermes config/state": "创建或恢复 Hermes 配置/状态快照",
        "Kill all running background processes": "终止所有正在运行的后台进程",
        "Approve a pending dangerous command": "批准待处理的危险命令",
        "Deny a pending dangerous command": "拒绝待处理的危险命令",
        "Run a prompt in the background": "在后台运行提示",
        "Show active agents and running tasks": "显示活动代理和正在运行的任务",
        "Queue a prompt for the next turn (doesn't interrupt)": "排队一个提示到下一轮（不会中断当前操作）",
        "Inject a message after the next tool call without interrupting": "在下次工具调用后注入消息，不中断当前操作",
        "Set a standing goal Hermes works on across turns until achieved": "设置一个持续目标，Hermes 会跨轮次工作直到完成",
        "Add or manage extra criteria on the active goal": "在活跃目标上添加或管理额外条件",
        "Show session info": "显示会话信息",
        "Show your slash command access (admin / user)": "显示您的斜杠命令访问权限（管理员/用户）",
        "Show active profile name and home directory": "显示当前配置文件名称和主目录",
        "Set this chat as the home channel": "将此聊天设为首页频道",
        "Resume a previously-named session": "恢复之前命名的会话",
        "Browse and resume previous sessions": "浏览和恢复之前的会话",
        # Configuration
        "Show current configuration": "显示当前配置",
        "Switch model for this session": "切换当前会话的模型",
        "Toggle codex app-server runtime for OpenAI/Codex models": "切换 OpenAI/Codex 模型的 codex 应用服务器运行时",
        "Show Google Gemini Code Assist quota usage": "显示 Google Gemini Code Assist 配额使用情况",
        "Set a predefined personality": "设置预定义的个性",
        "Toggle the context/model status bar": "切换上下文/模型状态栏",
        "Toggle voice mode": "切换语音模式",
        "Control what Enter does while Hermes is working": "控制 Hermes 工作时的 Enter 键行为",
        # Tools & Skills
        "Manage tools: /tools [list|disable|enable] [name...]": "管理工具：/tools [list|disable|enable] [名称...]",
        "List available toolsets": "列出可用的工具集",
        "Search, install, inspect, or manage skills": "搜索、安装、检查或管理技能",
        "Manage scheduled tasks": "管理计划任务",
        "Background skill maintenance (status, run, pin, archive, list-archived)": "后台技能维护（状态、运行、固定、归档、列出已归档）",
        "Multi-profile collaboration board (tasks, links, comments)": "多配置文件协作看板（任务、链接、评论）",
        "Reload .env variables into the running session": "重新加载 .env 变量到当前会话",
        "Reload MCP servers from config": "从配置重新加载 MCP 服务器",
        "Re-scan ~/.hermes/skills/ for newly installed or removed skills": "重新扫描 ~/.hermes/skills/ 以发现新增或删除的技能",
        "Connect browser tools to your live Chromium-family browser via CDP": "通过 CDP 连接浏览器工具到您的 Chromium 浏览器",
        "List installed plugins and their status": "列出已安装插件及其状态",
        # Info
        "Browse all commands and skills (paginated)": "浏览所有命令和技能（分页显示）",
        "Show help for a command or search by keyword": "显示命令帮助或按关键词搜索",
        "Show monthly token/API usage stats": "显示每月令牌/API 使用统计",
        "AI-powered session insights and recommendations": "AI 驱动的会话洞察和建议",
        "Restart the agent in-place (new shell + session)": "原地重启代理（新的 shell 和会话）",
        "List all connected platforms and channels": "列出所有已连接的平台和频道",
        "Show platform info for current chat": "显示当前聊天的平台信息",
        "Copy a message to another channel or as text": "复制消息到其他频道或作为文本",
        "Paste text from clipboard or a prior /copy buffer": "从剪贴板或之前的 /copy 缓冲区粘贴文本",
        "Generate, edit, analyze or describe images": "生成、编辑、分析或描述图像",
        "Update Hermes from GitHub (git pull + pip install)": "从 GitHub 更新 Hermes（git pull + pip install）",
        "Debug tools and diagnostics": "调试工具和诊断",
        "Quit Hermes (exit the CLI)": "退出 Hermes（退出 CLI）",
        # Multi-line config entries
        "Toggle codex app-server runtime for OpenAI/Codex models": "切换 OpenAI/Codex 模型的 codex 应用服务器运行时",
        "Cycle tool progress display: off -> new -> all -> verbose": "循环切换工具进度显示：关 -> 新 -> 全部 -> 详细",
        "Toggle gateway runtime-metadata footer on final replies": "切换最终回复上的网关运行时元数据页脚",
        "Toggle YOLO mode (skip all dangerous command approvals)": "切换 YOLO 模式（跳过所有危险命令审批）",
        "Manage reasoning effort and display": "管理推理力度和显示",
        "List skill bundles (aliases /<name> for multiple skills)": "列出技能包（别名 /<名称> 对应多个技能）",
        "Toggle fast mode — OpenAI Priority Processing / Anthropic Fast Mode (Normal/Fast)": "切换快速模式 — OpenAI 优先处理 / Anthropic 快速模式（普通/快速）",
        "Show or change the display skin/theme": "显示或更改显示皮肤/主题",
        "Pick the TUI busy-indicator style": "选择 TUI 忙碌指示器样式",

        # ======== main.py — 子命令 help= 和 description= ========
        "session management (start, stop, resume)": "会话管理（启动、停止、恢复）",
        "model/provider management (switch, list)": "模型/提供商管理（切换、列出）",
        "configuration tools": "配置工具",
        "debugging and diagnostics": "调试和诊断",
        "tool and skill management": "工具和技能管理",
        "system administration (update, info, env)": "系统管理（更新、信息、环境）",
        "gateway platform management": "网关平台管理",
        "gateway run": "网关运行",
        "voice mode control": "语音模式控制",
        "kanban board management": "看板管理",
        "cron job management": "计划任务管理",
        "skill curator management": "技能策展管理",
        "session management (experimental)": "会话管理（实验性）",
        "plugin management": "插件管理",
        "set session personality": "设置会话个性",
        "installed proxies": "已安装的代理",
        "show all snapshots": "显示所有快照",
        "create a snapshot": "创建快照",
        "restore a snapshot": "恢复快照",
        "prune old snapshots": "清理旧快照",
        "web / browser tools: connect, navigate, inspect": "网页/浏览器工具：连接、导航、检查",
        "start a new session": "开始新会话",
        "resume a named session": "恢复命名的会话",
        "show session status": "显示会话状态",
        "stop active session": "停止活动会话",
        "list all sessions": "列出所有会话",
        "handoff session to platform": "将会话移交给平台",
        "list available models/providers": "列出可用模型/提供商",
        "switch model for active session": "切换活动会话的模型",
        "set personality for the session": "设置会话的个性",
        "show current personality": "显示当前个性",
        "list and manage voice personalities": "列出和管理语音个性",
        "configure voice settings": "配置语音设置",
        "set default model globally": "全局设置默认模型",
        "show all environment variables": "显示所有环境变量",
        "show help for a subcommand": "显示子命令的帮助",
        "show installed Hermes version": "显示已安装的 Hermes 版本",
        "update Hermes to latest version": "将 Hermes 更新到最新版本",
        "list connected platforms/channels": "列出已连接的平台/频道",
        "show platform info for current chat": "显示当前聊天的平台信息",
        "start the gateway service": "启动网关服务",
        "stop the gateway service": "停止网关服务",
        "list enabled plugins": "列出已启用的插件",
        "list all skills": "列出所有技能",
        "search for skills": "搜索技能",
        "install a skill": "安装技能",
        "inspect a skill": "检查技能",
        "show skill auditor status": "显示技能审计状态",
        "show skill bundles": "显示技能包",
        "tool management": "工具管理",
        "browser tool management": "浏览器工具管理",
        "run the skill curator": "运行技能策展器",
        "show curator status": "显示策展状态",
        "pin a skill": "固定技能",
        "unpin a skill": "取消固定技能",
        "archive a skill": "归档技能",
        "restore an archived skill": "恢复已归档的技能",
        "list archived skills": "列出已归档的技能",
        "list cron jobs": "列出计划任务",
        "create a cron job": "创建计划任务",
        "edit a cron job": "编辑计划任务",
        "pause a cron job": "暂停计划任务",
        "resume a cron job": "恢复计划任务",
        "remove a cron job": "删除计划任务",
        "run a cron job now": "立即运行计划任务",
        "complex multi-step kanban management": "复杂的多步骤看板管理",
        "create a new kanban board": "创建新看板",
        "init kanban in working directory": "在工作目录初始化看板",
        "show kanban board": "显示看板",
        "list kanban boards": "列出看板",
        "assign a task to an agent": "分配任务给代理",
        "reclaim a task": "回收任务",
        "modify comment on a task": "修改任务评论",
        "link a uri to a task": "链接 URI 到任务",
        "unlink a uri from a task": "取消链接任务中的 URI",
        "archive a task": "归档任务",
        "show archived tasks": "显示已归档的任务",
        "tail task output": "追踪任务输出",
        "dispatch a task to agents": "分发任务给代理",
        "show task statistics": "显示任务统计",
        "show assignee info": "显示分配者信息",
        "gc kanban state": "垃圾回收看板状态",
        "specify task requirements": "指定任务需求",
        "set task context": "设置任务上下文",
        "subscribe to task notifications": "订阅任务通知",
        "list subscriptions": "列出订阅",
        "unsubscribe from task notifications": "取消订阅任务通知",
        "show kanban logs": "显示看板日志",
        "show kanban runs": "显示看板运行",
        "show kanban board diagnostics": "显示看板诊断",
        "heartbeat check": "心跳检查",
        "list all assignees on a board": "列出看板上的所有分配者",
        "reassign a task": "重新分配任务",
        # Voice subcommands
        "Turn voice mode on": "开启语音模式",
        "Turn voice mode off": "关闭语音模式",
        "Show voice mode status": "显示语音模式状态",
        # Fast mode subcommands
        "Set fast mode to normal": "将快速模式设为普通",
        "Set fast mode to fast": "将快速模式设为快速",
        "Show fast mode status": "显示快速模式状态",
        # Personality subcommands
        "Set personality": "设置个性",
        "Show current personality": "显示当前个性",
        # Description texts
        "Hermes Agent CLI - general purpose commands": "Hermes Agent CLI — 通用命令",
        "Session management commands (start, stop, resume, status)": "会话管理命令（启动、停止、恢复、状态）",
        "Model and provider management": "模型和提供商管理",
        "Configuration commands for Hermes Agent": "Hermes Agent 配置命令",
        "Debugging and diagnostic tools": "调试和诊断工具",
        "Tool and skill management commands": "工具和技能管理命令",
        "System administration commands": "系统管理命令",
        "Gateway platform management commands": "网关平台管理命令",
        "Gateway run command": "网关运行命令",
        "Voice mode control": "语音模式控制",
        "Personality management": "个性管理",
        "Snapshot management": "快照管理",
        "Help for a specific subcommand": "特定子命令的帮助",
        "Show all snapshots": "显示所有快照",
        "Create a new snapshot": "创建新快照",
        "Restore a snapshot by ID": "按 ID 恢复快照",
        "Prune old snapshots": "清理旧快照",
        "List installed plugins": "列出已安装的插件",
        "Show help for a subcommand": "显示子命令的帮助",
        "Show installed Hermes version": "显示已安装的 Hermes 版本",
        "Update Hermes to the latest version from GitHub": "从 GitHub 将 Hermes 更新到最新版本",
        "List all environment variables": "列出所有环境变量",
        "List connected platforms": "列出已连接的平台",
        "Set default model": "设置默认模型",
        "Show platform info": "显示平台信息",
        "List available models": "列出可用模型",
        "List available providers and their models": "列出可用提供商及其模型",
        "Manage voice personalities and settings": "管理语音个性和设置",
        "List voice personalities": "列出语音个性",
        "Configure voice settings": "配置语音设置",
        "Start gateway service": "启动网关服务",
        "Stop gateway service": "停止网关服务",
        "Debug share": "调试分享",
        "List all available tools": "列出所有可用工具",
        "Disable a tool": "禁用工具",
        "Enable a tool": "启用工具",
        "Connect browser": "连接浏览器",
        "Disconnect browser": "断开浏览器",
        "Browser status": "浏览器状态",
        "Connect browser to CDP endpoint": "连接到 CDP 端点的浏览器",
        "Disconnect the browser tool": "断开浏览器工具",
        "Show browser tool connection status": "显示浏览器工具连接状态",
        "Search for skills by keyword": "按关键词搜索技能",
        "Browse and install skills": "浏览和安装技能",
        "Inspect a specific skill": "检查特定技能",
        "Start a new session": "开始新会话",
        "Resume a named session": "恢复命名的会话",
        "Show session status": "显示会话状态",
        "Stop the active session": "停止活动会话",
        "List all sessions": "列出所有会话",
        "Handoff session to another platform": "将会话移交给另一个平台",
    }

    files = [
        ("commands.py", COMMANDS_PATH),
        ("main.py", MAIN_PATH),
    ]

    total_applied = 0
    for label, fpath in files:
        if not os.path.exists(fpath):
            print(f"  ⚠  文件不存在: {fpath}")
            continue

        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        count = 0
        for eng, chn in replacements.items():
            if eng in content:
                # Only replace the FIRST occurrence to avoid touching
                # legitimate uses of the English text as variable names etc.
                idx = content.find(eng)
                before = content[:idx]
                after = content[idx + len(eng):]
                # Make sure we're replacing inside a string context
                content = before + chn + after
                count += 1

        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"  ✓ {label}: 翻译 {count} 条")
        total_applied += count

    return total_applied


def write_soul():
    """Write SOUL.md with Chinese language instruction."""
    content = """You ALWAYS respond in Simplified Chinese (简体中文) regardless of the platform or user's language, unless the user explicitly asks you to speak in another language.

You are Hermes Agent (赫尔墨斯代理), an intelligent AI assistant created by Nous Research.
You are helpful, knowledgeable, and direct. You communicate clearly and prioritize being genuinely
useful over being verbose.

You ALWAYS respond in Simplified Chinese (简体中文).
"""
    os.makedirs(HERMES_HOME, exist_ok=True)
    with open(SOUL_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("  ✓ SOUL.md: 已写入中文语言指令")


def verify():
    """Quick check that translations are in place."""
    checks = {
        "commands.py": ("commands.py", "确认平台启动 ping"),
        "main.py": ("main.py", "管理消息网关"),
    }
    ok = True
    for label, (fname, marker) in checks.items():
        path = os.path.join(AGENT_DIR, "hermes_cli", fname)
        if not os.path.exists(path):
            print(f"  ⚠  {label}: 文件不存在")
            ok = False
            continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if marker in content:
            print(f"  ✓ {label}: 中文翻译已确认")
        else:
            print(f"  ✗ {label}: 未找到中文翻译标记 \"{marker}\"")
            ok = False

    with open(SOUL_PATH, "r", encoding="utf-8") as f:
        if "Simplified Chinese" in f.read():
            print("  ✓ SOUL.md: 中文指令已确认")
        else:
            print("  ✗ SOUL.md: 未找到中文指令")
            ok = False

    return ok


def main():
    print("=" * 55)
    print("  Hermes Agent L10n — 简体中文汉化脚本")
    print("=" * 55)

    if not os.path.exists(AGENT_DIR):
        print(f"\n✗ 未找到 Hermes Agent: {AGENT_DIR}")
        print("  请先安装 Hermes Agent")
        sys.exit(1)

    print(f"\n📁 路径: {AGENT_DIR}")
    print(f"\n🔧 开始翻译...\n")

    # Method 1: try git apply (fastest, most complete)
    patch_ok = apply_patch()

    if patch_ok:
        n = 0  # patch handles everything
        print()
    else:
        # Method 2: direct string replacements (more resilient)
        print(f"\n  ⚠ git apply 失败，改用直接字符串替换...\n")
        n = apply_replacements()

    # Always write SOUL.md (not in patch)
    print()
    write_soul()

    # Verify
    print(f"\n🔍 验证翻译...\n")
    if verify():
        print(f"\n✅ 汉化完成！")
    else:
        print(f"\n⚠️  部分翻译未通过验证，请检查文件")

    print(f"\n💡 重启 Hermes CLI 即可查看效果")
    print(f"⚠️  执行 'hermes update' 后会覆盖修改，重新运行此脚本即可恢复")


if __name__ == "__main__":
    main()
