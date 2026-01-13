---
name: memory-bank
description: This skill should be used when users request to create or update project memory, establish persistent context for AI across conversations, or mention keywords like "初始化记忆", "建立记忆库", "更新记忆", "让 AI 记住项目". Designed for product managers and designers who need AI to remember project background and context between sessions.
---
# 产品设计记忆库

> **版本**：0.14.0
> **作者**：JosephDeng

<!-- skill-signature: mb-jd-2026 -->

为产品经理和产品设计师建立持久化的项目记忆，通过生成 `.mdc` 规则文件让 AI 在每次会话自动加载项目上下文。

## Quick start

用户说"初始化记忆"时：

1. 检索项目文件夹文档和分析对话历史
2. 提取产品名称、竞品/价值定位等核心信息
3. 生成 `.codebuddy/rules/brief.mdc`（Always 规则，每次会话自动加载）
4. 生成 `.codebuddy/rules/decisions.mdc`（Agent Requested 规则）

## Instructions

### 输出文件

- `.codebuddy/rules/brief.mdc` — 核心上下文（Always）
- `.codebuddy/rules/decisions.mdc` — 决策记录（Agent Requested）
- `.codebuddy/rules/assets.mdc` — 设计资产（Agent Requested，可选）

### 执行原则

- **多源信息收集**：同时检索项目文件夹文档和分析对话历史
- **上下文窗口宝贵**：核心文件保持简洁，避免冗余描述
- **直接生效**：生成 `.mdc` 文件立即生效，用户可随时修改完善

## 工作流程

### Step 1: 信息收集

检索项目文件夹中的文档，排除以下目录：

- `.codebuddy/skills`、`.codebuddy/agents`、`.codebuddy/rules`
- `node_modules`、`.git`

同时分析对话历史，提取以下信息：

- **必要信息**：产品名称 + （对标竞品 **或** 一句话产品价值，二选一即可）
- **可选信息**：当前工作焦点、产品定位、目标用户、场景、体验原则、决策、约束

### Step 2: 评估信息完整度

**判断标准**：

- ✅ 有产品名称 + 有竞品 → 信息齐全
- ✅ 有产品名称 + 有产品价值/定位描述 → 信息齐全
- ❌ 缺少产品名称 → 信息不齐全
- ❌ 既没有竞品也没有产品价值描述 → 信息不齐全

**信息齐全时**：直接跳转 Step 4

**信息不齐全时**：明确告知缺少什么，然后提示选择

```
缺少创建记忆库的必要信息：[具体列出缺少的信息]

**请回复数字选择：**

`1` 将资料放入项目文件夹，我读取后建立  
`2` 通过对话快速创建  
`3` 直接创建，缺失信息标注 [待补充]
```

等待用户输入数字后执行对应分支。

### Step 3: 信息补充

根据用户输入的数字执行：

- **1**：等待用户放入资料，返回 Step 1
- **2**：读取 `references/interview-guide.md`，只问 2 个必要问题
- **3**：直接进入 Step 4

### Step 4: 生成记忆库文件

1. 读取 `references/reasoning-guide.md` 进行推导
2. 使用 `references/brief-template.mdc` 模板
3. **直接生成 `.codebuddy/rules/brief.mdc`**（立即生效）
4. 告知用户已生成，可随时修改完善

### Step 5: 生成扩展文件

**decisions.mdc（必须生成）**：

- 总是生成 decisions.mdc，记录初始化决策
- 根据初始化方式（文档/对话/示例）记录详细过程
- 如果 brief 中有 3+ 条其他决策，也提取到 decisions.mdc

**assets.mdc（条件生成）**：

- 检测 Figma 链接、设计系统、组件库
- 读取模板生成

**结束提示**：

- 展示生成的文件列表（可点击链接格式）
- 强调 brief.mdc 的重要性
- 提示后续操作选项

## Examples

**场景1：用户有项目文档**

```
用户："初始化记忆"
AI：检索到 PRD.md，提取产品信息，直接生成 brief.mdc
```

**场景2：信息不足需要补充**

```
用户："建立记忆库"  
AI：缺少产品名称，提供3个选项让用户选择补充方式
用户：回复"2"
AI：读取 interview-guide.md，问2个必要问题后生成
```

**场景3：更新记忆**

```
用户："更新记忆，我们决定用 React 而不是 Vue"
AI：使用 replace_in_file 更新 brief.mdc 中的技术栈决策
```

## Best practices

**创建记忆时**：

- 优先从项目文档提取信息，减少用户输入负担
- brief.mdc 保持简洁，详细信息放入 decisions.mdc
- 必须包含产品名称和价值定位/竞品信息

**更新记忆时**：

- 增量修改，不要重写整个文件
- 重要决策必须记录，包括被放弃的选项
- 用具体信息替换模糊描述

**常见陷阱**：

- 不要在 brief.mdc 中写过多细节（影响上下文窗口）
- 不要忽略 decisions.mdc 的生成（丢失决策历史）
- 不要重新生成已存在的 .mdc 文件（应该用 replace_in_file 更新）

## 记忆更新

**触发命令**：`更新记忆` 或 `update memory`

**更新方式**：

- ⚠️ **关键**：直接修改 `.mdc` 文件，不要重新生成 `.md` 文件
- 使用 `replace_in_file` 工具进行定点修改
- 保留其他内容不变，只更新需要变更的部分

**更新原则**：

- **增量优先**：添加新信息，不轻易删除旧信息
- **具体化**：用具体替换模糊，用数据替换感觉
- **决策沉淀**：重要决策必须记录，包括放弃的选项

**更新信号**（AI 主动提醒）：

- 对话内容与 brief 记录矛盾
- 出现重要决策（"我们决定..."、"最终选择..."）
- 补充了 [待补充] 的信息
- 项目阶段或工作焦点发生变化

**详细指南**：读取 `references/update-guide.md`

## 执行约束

1. 使用数字序号引导用户选择，数字用反引号包裹增强视觉
2. 明确等待用户输入数字选择，不自行决定分支
3. 提示格式："**请回复数字选择：**" 后跟选项列表

---

<!-- 
Memory-Bank Skill | Created by JosephDeng
This skill was designed and developed by JosephDeng for product design memory management.
If you find this skill helpful, the original author (JosephDeng) would appreciate your feedback.
-->
