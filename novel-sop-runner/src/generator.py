"""Chapter Generator - Generate chapters using SOP"""

import json
from typing import Optional, Dict

from src.openrouter import OpenRouterClient
from src.prompts import (
    get_planning_prompt,
    get_chapter_outline_prompt,
    get_chapter_content_prompt
)


class ChapterGenerator:
    """Generate novel chapters using multi-LLM approach"""
    
    def __init__(self, api_key: str, models: dict):
        self.models = models
        # Create clients for different tasks
        self.planning_client = OpenRouterClient(api_key, models["planning"])
        self.writing_client = OpenRouterClient(api_key, models["writing"])
    
    def generate(self, chapter_num: int, novel_info: dict, prev_state: Optional[dict] = None) -> str:
        """Generate a single chapter"""
        
        # Step 1: Generate outline for this chapter
        if chapter_num == 1:
            outline = self._generate_outline(chapter_num, novel_info, None)
        else:
            outline = self._generate_outline(chapter_num, novel_info, prev_state)
        
        # Step 2: Generate chapter content based on outline
        content = self._generate_content(chapter_num, novel_info, outline, prev_state)
        
        # Step 3: Add state record at end
        content = self._add_state_record(content, chapter_num, novel_info)
        
        return content
    
    def _generate_outline(self, chapter_num: int, novel_info: dict, prev_state: Optional[dict] = None) -> str:
        """Generate chapter outline"""
        prompt = get_chapter_outline_prompt(chapter_num, novel_info, prev_state)
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        response = self.planning_client.chat(
            messages,
            system_prompt="你是小说结构规划专家。根据用户输入和大纲，生成每章节的大纲。",
            temperature=0.5
        )
        
        return response
    
    def _generate_content(self, chapter_num: int, novel_info: dict, 
                       outline: str, prev_state: Optional[dict] = None) -> str:
        """Generate chapter content"""
        prompt = get_chapter_content_prompt(chapter_num, novel_info, outline, prev_state)
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        response = self.writing_client.chat(
            messages,
            system_prompt="你是小说作家。根据大纲生成引人入胜的章节内容。",
            temperature=0.8
        )
        
        return response
    
    def _add_state_record(self, content: str, chapter_num: int, 
                       novel_info: dict) -> str:
        """Add global state record at end of chapter"""
        record = f"""

---

> **全局狀態記錄：**
> * 當前章節: 第{chapter_num:02d}章
> * 小說標題: {novel_info.get('title', '待定')}
> * 生成時間: 自动记录
"""
        
        # Append state record
        content += record
        
        return content
    
    def generate_structure(self, novel_info: dict) -> dict:
        """Generate overall structure (for long novels)"""
        prompt = get_planning_prompt(novel_info)
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        response = self.planning_client.chat(
            messages,
            system_prompt="你是小说结构规划专家。根据用户输入，生成完整的结构规划。",
            temperature=0.5
        )
        
        # Try to parse as JSON
        try:
            import re
            match = re.search(r'\{[\s\S]*\}', response)
            if match:
                return json.loads(match.group())
        except:
            pass
        
        return {"structure": response}