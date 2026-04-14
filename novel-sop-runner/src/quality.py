"""QA module for chapter validation"""

import json
import re
from src.openrouter import OpenRouterClient
from src.prompts import get_quality_check_prompt


class QualityChecker:
    def __init__(self, api_key: str, model: str):
        self.client = OpenRouterClient(api_key, model)
    
    def check(self, chapter: str, prev_state=None) -> list:
        prompt = get_quality_check_prompt(chapter, prev_state)
        messages = [{"role": "user", "content": prompt}]
        
        response = self.client.chat(
            messages,
            system_prompt="你是小说质量检查专家。严格按照检查清单验证章节质量。",
            temperature=0.3
        )
        
        try:
            match = re.search(r'\{[\s\S]*\}', response)
            if match:
                result = json.loads(match.group())
                return result.get("issues", [])
        except:
            pass
        
        return []
    
    def quick_check(self, chapter: str) -> dict:
        issues = []
        if len(chapter) < 500:
            issues.append("字数过少")
        if "全局狀態記錄" not in chapter:
            issues.append("缺状态")
        if "---" not in chapter:
            issues.append("缺分隔")
        
        return {"issues": issues, "word_count": len(chapter), "pass": len(issues) == 0}