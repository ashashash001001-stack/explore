"""SOP Prompt Templates - Direct use from novel-sop-universal.md"""

import json
from typing import Optional, Dict


# ============================================================================
# PLANNING PROMPTS
# ============================================================================

def get_planning_prompt(novel_info: dict) -> str:
    """Generate overall structure planning"""
    return f"""## 用户输入

标题: {novel_info.get('title', '待定')}
大纲: {novel_info.get('outline', '')}
类型: {novel_info.get('genre', 'suspense')}
目标章节数: {novel_info.get('chapters', 10)}

## 任务

根据上述信息，生成完整的结构规划：
1. 主角设定（姓名、背景、动机）
2. 反派设定
3. 世界观简述
4. 每章节的简单目标（1-2句话）
5. 主要悬念设计

请以JSON格式输出：
{{
  "protagonist": {{}},
  "antagonist": {{}},
  "world": {{}},
  "chapters": [{{}}],
  "hooks": [{{}}]
}}
"""


def get_chapter_outline_prompt(chapter_num: int, novel_info: dict, prev_state: Optional[dict] = None) -> str:
    """Generate chapter outline"""
    
    # Previous state info
    prev_info = ""
    if prev_state:
        prev_info = f"""
## 上一章状态

{prev_state}
"""
    
    return f"""## 当前任务

生成第 {chapter_num:02d} 章的大纲

## 小说信息

标题: {novel_info.get('title', '待定')}
类型: {novel_info.get('genre', 'suspense')}
目标章节数: {novel_info.get('chapters', 10)}

{prev_info}

## 要求

根据上述信息，生成第 {chapter_num:02d} 章的大纲：
1. 本章核心事件（1-2句话）
2. 主要冲突
3. 角色关键行为
4. 结尾悬念设计

格式：
```
# 第{chapter_num}章大纲：[标题]

## 本章目标
- 核心事件: 
- 主要冲突: 
- 角色行动: 

## 节奏安排
- 开头: 
- 发展: 
- 高潮: 
- 结尾（悬念）: 

## 角色状态变化
- 主角: 
- 配角: 
```
"""


def get_chapter_content_prompt(chapter_num: int, novel_info: dict, 
                             outline: str, prev_state: Optional[dict] = None) -> str:
    """Generate chapter content"""
    
    # Previous state info
    prev_info = ""
    if prev_state:
        prev_info = f"""
## 上一章结尾状态
{json.dumps(prev_state, ensure_ascii=False, indent=2)}
"""
    
    return f"""## 任务

生成第 {chapter_num:02d} 章的正文

## 小说信息

标题: {novel_info.get('title', '待定')}
类型: {novel_info.get('genre', 'suspense')}

## 大纲

{outline}

{prev_info}

## SOP要求（v7.1）

请严格按照以下规则生成：

1. **内容比例参考**：
   - 场景/动作: 40%
   - 对话: 30%
   - 心理: 20%
   - 描述/氛围: 10%

2. **每章必备元素**：
   - 至少一个冲突（大小均可）
   - 角色决定影响剧情
   - 为下一章留悬念

3. **正文格式规则**：
   - 段落之间用空行分隔
   - 支持 Markdown：`**粗体**`、`*斜体*`、`> 引用`
   - 不要使用 `#` 标题语法（系统会自动处理章节标题）
   - 使用 `---` 分隔线

4. **悬念设计**：
   - 每3章至少1个主要悬念
   - 每章结尾设置悬念

## 输出格式

```
# 第 {chapter_num} 章：[标题]

[时间/地点]: ...

---

[正文内容...]

---

> **全局状态记录：**
> * 当前章节: 第{chapter_num:02d}章
> * 角色状态: [情续/位置/关键物品]
> * 待揭开的悬念: [列表]
> * 待回收伏笔: [列表]
```
"""


# ============================================================================
# QUALITY CHECK PROMPTS
# ============================================================================

def get_quality_check_prompt(chapter: str, prev_state: Optional[dict] = None) -> str:
    """Quality check prompt"""
    return f"""## 任务

检查以下章节的质量

## 章节内容

{chapter}

## 检查清单

### 连贯性检查
- [ ] 角色行为是否符合性格？
- [ ] 场景切换是否合理？
- [ ] 时间线是否连贯？
- [ ] 规则应用是否一致？

### 情节检查
- [ ] 本章有冲突吗？
- [ ] 冲突有解决吗？
- [ ] 解决方式合理吗？
- [ ] 有为下一章留悬念吗？

### 角色检查
- [ ] 对话符合角色身份吗？
- [ ] 心理变化有铺垫吗？
- [ ] 角色有成长/改变吗？

### 读者体验
- [ ] 开头够吸引吗？
- [ ] 节奏流畅吗？
- [ ] 高潮够有力吗？

请输出JSON格式：
{{
  "issues": ["问题1", "问题2"],
  "score": 85,
  "pass": true/false
}}
"""


# ============================================================================
# AUTO-FILL PROMPTS
# ============================================================================

def get_auto_fill_prompt(novel_info: dict) -> str:
    """Auto-fill missing info"""
    return f"""## 任务

根据以下不完整的大纲，自动补充缺失的信息

## 当前信息

标题: {novel_info.get('title', '')}
大纲: {novel_info.get('outline', '')}
类型: {novel_info.get('genre', '')}

## 要求

请补充：
1. 主角姓名（如果缺失）
2. 主角背景/动机（如果缺失）
3. 反派设定（如果缺失）
4. 世界观细节（如果缺失）

对于缺失信息，使用SOP推荐的填充策略：
- 科幻→Alex/Maya, 奇幻→Aria/Kael, 都市→小雨/阿强
- 动机根据目标反推合理动机
- 反派必须有与主角对立的根本原因

请以JSON格式输出补充后的完整设定：
{{
  "protagonist": {{"name": "", "background": "", "desire": ""}},
  "antagonist": {{"name": "", "goal": "", "reason": ""}},
  "world": {{"type": "", "rules": []}},
}}
"""


import json