# Hermes Agent 简体中文汉化

## 目录

| 文件 | 说明 |
|------|------|
| `hermes-chinese.patch` | Git 补丁文件，可直接用 `git apply` 还原所有中文修改 |
| `apply-l10n.py` | 独立 Python 脚本，可重复运行以应用中文翻译 |

## 用法

### 方式 A：运行脚本（推荐）

```bash
# 确保 Hermes Agent 已安装
python apply-l10n.py

# 重启 Hermes CLI 使改动生效
hermes
```

### 方式 B：应用补丁

```bash
cd ~/.hermes/hermes-agent
git apply /path/to/hermes-chinese.patch
```

> **注意：** 执行 `hermes update` 后会覆盖这些修改，届时重新运行 `python apply-l10n.py` 即可恢复全部中文翻译。

## 翻译范围

- ✅ `/hermes_cli/commands.py` — 65 条斜杠命令的英文描述 → 简体中文
- ✅ `/hermes_cli/main.py` — 169 条子命令的 `help=` 和 `description=` → 简体中文
- ✅ `SOUL.md` — 新增中文语言指令：助手默认以简体中文回复
