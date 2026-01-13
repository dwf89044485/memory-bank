# Trae 可点击链接生成指南

## 基本格式

```markdown
[链接文本](file:///绝对路径/到/文件)
```

## 常见用法

### 1. 链接到文件

```markdown
[文件名](file:///完整/绝对/路径/文件名.扩展名)
```

**示例：**
```markdown
[brief.mdc](file:///Users/josephdeng/Downloads/openskills-main/.codebuddy/rules/brief.mdc)
```

### 2. 链接到特定行

```markdown
[文件名](file:///完整/绝对/路径/文件名.扩展名#L行号)
```

**示例：**
```markdown
[brief.mdc](file:///Users/josephdeng/Downloads/openskills-main/.codebuddy/rules/brief.mdc#L15)
```

### 3. 链接到行范围

```markdown
[文件名](file:///完整/绝对/路径/文件名.扩展名#L起始行-L结束行)
```

**示例：**
```markdown
[brief.mdc](file:///Users/josephdeng/Downloads/openskills-main/.codebuddy/rules/brief.mdc#L10-L20)
```

### 4. 链接到函数

```markdown
[函数名](file:///完整/绝对/路径/文件名.扩展名#L起始行)
```

**示例：**
```markdown
[install](file:///Users/josephdeng/Downloads/openskills-main/src/commands/install.ts#L10)
```

## 关键要点

- 使用 `file:///` 协议（注意是三个斜杠）
- 路径必须是绝对路径
- 使用 `#L行号` 链接到单行
- 使用 `#L起始行-L结束行` 链接到多行
- 链接文本建议使用文件名或函数名，简洁易读

## 实际效果

- [brief.mdc](file:///Users/josephdeng/Downloads/openskills-main/.codebuddy/rules/brief.mdc)
- [README.md](file:///Users/josephdeng/Downloads/openskills-main/README.md#L1-L10)
- [install.ts](file:///Users/josephdeng/Downloads/openskills-main/src/commands/install.ts)

点击以上链接，会自动在编辑器中打开对应文件。
