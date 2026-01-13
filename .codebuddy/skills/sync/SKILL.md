---
name: sync
description: This skill should be used when users say "同步进度" to synchronize Memory-Bank project management files to the J-CORE master control server. Automatically pushes brief.mdc and decisions.mdc to a fixed directory without requiring any user input or path calculations.
---

# Memory-Bank 同步

## 触发

用户说"同步进度"

## 执行

直接运行同步脚本：

```bash
python3 /data/workspace/.codebuddy/skills/sync/scripts/sync.py
```

## 路径

**本地文件：**
- `/data/workspace/.codebuddy/rules/brief.mdc`
- `/data/workspace/.codebuddy/rules/decisions.mdc`

**远程服务器：**
- Host: `root@josephdeng-any20.devcloud.woa.com`
- Port: `36000`
- Directory: `/data/workspace/项目进度/memory-bank/`
