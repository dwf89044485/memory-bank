# 推导指南

当收集到必要信息（产品名、对标竞品、当前工作焦点）后，按此指南推导更完整的产品上下文，然后**直接生成文件**。

## 0. 前置准备

### 信息来源过滤

**⚠️ 关键：检索项目文件时必须排除以下路径**

```
排除目录：
- .codebuddy/skills    (技能定义，不是用户项目)
- .codebuddy/agents    (代理定义，不是用户项目)
- .codebuddy/rules     (规则文件，不是用户项目)
- node_modules         (依赖包)
- .git                 (版本控制)
```

**只检索用户的实际项目文档**，如：

- PRD、需求文档、设计文档
- README、项目说明
- 业务代码中的注释和文档

### 时间获取

**在生成/更新记忆库文件前，必须获取当前精确时间**

```xml
<get_current_time>
  <method>执行系统命令获取当前时间</method>
  <command>date +"%Y-%m-%d %H:%M"</command>
  <format>YYYY-MM-DD HH:MM（不带时区）</format>
  <usage>
    - 决策记录的日期字段
    - 更新记录的时间戳
    - 当前状态的更新时间
  </usage>
</get_current_time>
```

## 1. 推导原则

### 1.1 粒度控制

| 维度     | 正确粒度             | 过细（避免）               |
| -------- | -------------------- | -------------------------- |
| 用户角色 | 数据工程师、产品经理 | 某公司的高级数据分析师 Tom |
| 场景     | 数据查询、协作编辑   | 在周一早上生成销售周报     |
| 痛点     | 查询复杂、性能慢     | 每次写 SQL 要花 30 分钟    |

### 1.2 推导来源优先级

1. **用户明确提供（对话中直接告知）** > **对话历史提取** > **项目文件提取** > **AI 知识库** > **竞品推理**

### 1.3 对话历史分析重点

从对话历史中提取以下信息：

- 产品名称和定位（用户可能在对话中描述过）
- 提及的竞品或类似产品
- 讨论过的功能或正在做的工作（当前焦点）
- 提到的用户角色、场景或需求
- 已做出的决策或达成的共识
- 提到的约束条件（技术、时间、资源）

### 1.3 不确定时

- 宁可留空标注 `[待补充]`，不做无意义猜测

## 2. 推导流程

```xml
<reasoning_process>
  <step name="产品定位推导">
    <input>产品名 + 竞品</input>
    <logic>
      <if condition="产品是知名产品（如飞书、Notion）">
        <action>从 AI 知识库提取产品定位、特点、用户群</action>
      </if>
      <if condition="产品不知名">
        <action>从竞品反推市场定位</action>
        <action>结合产品名推断产品类型</action>
      </if>
    </logic>
    <output>产品定位（一句话）、产品类型</output>
  </step>

  <step name="目标用户推导">
    <input>产品定位 + 竞品 + 当前工作焦点</input>
    <logic>
      <action>从竞品提取典型用户群（职业类型）</action>
      <action>根据当前焦点聚焦相关用户角色</action>
    </logic>
    <output>2-3 个职业类型</output>
    <constraint>只到职业类型级别，如：数据工程师、产品经理</constraint>
  </step>

  <step name="核心场景推导">
    <input>产品定位 + 当前工作焦点 + 目标用户</input>
    <logic>
      <action>从竞品提取典型使用场景</action>
      <action>根据当前焦点聚焦具体场景</action>
    </logic>
    <output>3-5 个功能级别场景</output>
    <constraint>只到功能级别，如：数据查询、协作编辑</constraint>
  </step>

  <step name="体验原则推导">
    <input>产品类型 + 竞品特点 + 当前焦点</input>
    <output>2-3 条体验原则</output>
    <examples>易用性优先、性能可靠、协作流畅</examples>
  </step>

  <step name="痛点推导">
    <input>场景 + 竞品常见问题</input>
    <output>2-3 个关键痛点</output>
    <constraint>不确定则标注 [待补充]</constraint>
  </step>
</reasoning_process>
```

## 3. 输出行为

**推导完成后，必须直接生成文件，不要在对话中展示推导结果请求确认。**

```xml
<output_behavior>
  <step name="生成记忆库文件">
    <action>使用 brief-template.mdc 模板</action>
    <action>将推导结果填入模板</action>
    <action>直接生成文件到 .codebuddy/rules/brief.mdc（注意：.mdc 后缀，立即生效）</action>
  </step>
  
  <step name="通知用户">
    <notify>
      ✅ 记忆库已创建并生效！
      
      📁 生成的文件：`.codebuddy/rules/brief.mdc`
      
      💡 **说明**：
      - 记忆库已立即生效，下次对话时 AI 会自动了解项目背景
      - 如需完善内容，可以：
        1. 直接编辑 brief.mdc 文件
        2. 随时告诉我「更新记忆」来补充信息
      
      ⚠️ **重要**：记忆库会影响 AI 协作质量，建议抽空审阅和完善内容
    </notify>
    <action>进入 step_6，生成扩展文件</action>
  </step>
  
  <step name="生成扩展文件">
    <critical>在用户确认 brief 之后，生成 decisions.mdc 和 assets.mdc（如果需要）</critical>
  
    <notify>
      接下来我将生成决策记录文件，记录记忆库的初始化过程。
    
      这将帮助我们追踪项目的设计决策和历史，让 AI 更好地理解项目背景。
    </notify>
  
    <action>读取 references/decisions-template.mdc</action>
    <action>添加初始化决策节点（Decision #1），根据实际情况填写：</action>
  
    <initialization_decision>
      <if condition="初始化时检测到项目文档（PRD、README、需求文档等）">
        <decision_content>
          **时间**：[获取当前时间，格式：YYYY-MM-DD HH:MM]
        
          **问题**：如何建立产品设计记忆库
        
          **现象**：
          - 检测到项目文件夹中包含现有文档
          - 需要从这些文档中提取产品信息
        
          **根因**：已有文档可以作为信息来源，无需从头收集
        
          **决策**：基于现有文档建立记忆库
        
          **依据**：
          - 直接从已有文档中提取产品信息
          - 避免重复询问用户已知信息
          - 提高初始化效率
        
          **整理过程**：
          - 分析了 [文档1名称]
          - 分析了 [文档2名称]
          - 提取了产品名称、对标竞品、工作焦点等核心信息
        </decision_content>
      </if>
    
      <if condition="初始化时项目文件夹为空，通过对话引导创建">
        <decision_content>
          **时间**：[获取当前时间，格式：YYYY-MM-DD HH:MM]
        
          **问题**：如何建立产品设计记忆库
        
          **现象**：
          - 项目文件夹中没有检测到项目文档
          - 需要通过对话收集必要信息
        
          **根因**：缺少必要的产品信息，需要用户提供
        
          **决策**：通过对话引导收集信息后创建
        
          **依据**：
          - 保证记忆库信息的准确性
          - 避免从不确定的来源推断
          - 让用户直接确认核心信息
        
          **收集的信息**：
          - 产品名称：[用户提供的产品名称]
          - 对标竞品：[用户提供的竞品]
          - 当前工作焦点：[用户提供的工作焦点]
          - 其他补充信息：[如有，记录用户提供的其他内容]
        </decision_content>
      </if>
    
      <if condition="初始化时项目文件夹为空，直接创建示例">
        <decision_content>
          **时间**：[获取当前时间，格式：YYYY-MM-DD HH:MM]
        
          **问题**：如何建立产品设计记忆库
        
          **现象**：
          - 项目文件夹中没有检测到项目文档
          - 用户选择直接创建示例，跳过信息收集
        
          **根因**：用户可能希望快速开始，后续再补充具体信息
        
          **决策**：直接创建示例记忆库，缺失信息标注 [待补充]
        
          **依据**：
          - 快速完成初始化流程
          - 避免强制收集信息增加用户负担
          - 提供清晰的框架，便于后续补充
        </decision_content>
      </if>
    </initialization_decision>
  
    <action>按以下结构生成 decisions.mdc：</action>
      <decisions_structure>
        1. **快速索引表**（顶部）
           - 表格形式：# | 决策 | 核心要点 | 类别
           - 类别：交互/策略/流程/架构/规范/约束
           - 让 AI 和人都能一眼看全貌
      
        2. **决策详情**（主体）
           - 每条决策包含：时间、问题、决策、依据
           - 从问题中发现的决策用 ⚡ 标记，增加：现象、根因、洞察
           - 有替代方案时列出：方案 → 未采用原因
      
        3. **决策演变**（表格）
           - 记录决策的调整：时间 | 原决策 | 调整后 | 原因
      
        4. **关键洞察**（底部）
           - 从决策过程中提炼的设计原则
           - 格式：### 洞察主题 + 引用块总结
      
        5. **待决策事项**
           - 用 checkbox 列出待决策议题
      </decisions_structure>
    
      <action>检查 brief.mdc 中是否有其他决策记录</action>
      <if condition="brief.mdc 的'关键决策'部分有 3+ 条记录">
        <action>从 brief.mdc 中提取所有决策信息，按模板格式化</action>
        <action>从 brief.mdc 中删除详细决策，改为引用语句</action>
      </if>
      <else>
        <action>brief.mdc 中的决策少于 3 条，保留在 brief 中，decisions.mdc 仅记录初始化决策</action>
      </else>
    
      <action>生成 .codebuddy/rules/decisions.mdc（直接生成 .mdc）</action>
      <set_variable name="generated_decisions" value="true"/>
    </if>
  
    <step name="检测设计资产文件">
      <critical>检测是否需要生成 assets.mdc</critical>
  
    <if condition="检测到设计资产信息（Figma、组件库等）">
      <action>读取 references/assets-template.mdc</action>
      <action>从对话历史/项目文件中提取资产信息</action>
      <action>生成 .codebuddy/rules/assets.mdc（直接生成 .mdc）</action>
      <set_variable name="generated_assets" value="true"/>
    </if>
  </step>
  
  <step name="展示记忆库目录">
    <notify>
      ✅ **项目记忆库已创建完成！**
    
      **已生成的文件：**
    
      - `.codebuddy/rules/brief.mdc`  
        核心上下文：产品定位、目标用户、场景、决策等
    
      - `.codebuddy/rules/decisions.mdc`  
        设计决策记录：初始化过程和关键决策历史
    
      - `.codebuddy/rules/assets.mdc`  
        设计资产：Figma 链接、组件库、设计系统等（如适用）
    
      ---
    
      💡 **小提示**  
      `brief.mdc` 是记忆库的核心，信息越完整，AI 对项目的理解就越深，提供的帮助也会更有价值。  
      建议尽可能补充完善 — 你可以自己填写，或者随时告诉我来帮你完善。
    
      ---
    
      🎯 从现在开始，无论是在新会话还是当前会话，我都会始终记得你的项目背景。
    
      **继续你的项目吧！**
    </notify>
  </step>
</output_behavior>
```

## 4. 推导失败处理

```xml
<failure_handling>
  <case condition="产品和竞品都不知名">
    <action>只填写用户提供的信息</action>
    <action>其他字段标注 [待补充]</action>
    <action>仍然生成 brief.md 文件</action>
  </case>
  
  <case condition="当前焦点过于模糊">
    <action>只推导宏观信息</action>
    <action>场景和用户保持通用</action>
  </case>
</failure_handling>
```

## 5. 关键规则

1. **不要在对话中展示推导结果** — 直接写入文件
2. **先生成 .md 后缀** — 触发预览模式，方便用户阅读
3. **用户确认后改 .mdc** — 固化为规则文件
4. **打开文件** — 生成后必须打开文件让用户看到
