"""OpenRouter LLM Client"""

import json
import requests
from typing import List, Dict, Optional


class OpenRouterClient:
    """OpenRouter API client for multi-LLM support"""
    
    BASE_URL = "https://openrouter.ai/api/v1"
    
    def __init__(self, api_key: str, model: str = "deepseek/deepseek-chat"):
        self.api_key = api_key
        self.model = model
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://novel-sop-runner",
            "X-Title": "Novel SOP Runner"
        })
    
    def chat(self, messages: List[Dict], system_prompt: Optional[str] = None, 
            temperature: float = 0.7, max_tokens: int = 4000) -> str:
        """Send chat request"""
        # Build messages
        msgs = []
        if system_prompt:
            msgs.append({"role": "system", "content": system_prompt})
        msgs.extend(messages)
        
        # Request
        response = self.session.post(
            f"{self.BASE_URL}/chat/completions",
            json={
                "model": self.model,
                "messages": msgs,
                "temperature": temperature,
                "max_tokens": max_tokens
            },
            timeout=120
        )
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    def chat_with_json(self, messages: List[Dict], system_prompt: Optional[str] = None) -> dict:
        """Chat with JSON response"""
        content = self.chat(messages, system_prompt)
        
        # Try to parse JSON
        try:
            # Find JSON in content
            import re
            match = re.search(r'\{[\s\S]*\}', content)
            if match:
                return json.loads(match.group())
        except:
            pass
        
        return {"raw": content}


def create_client(api_key: str, model: str) -> OpenRouterClient:
    """Create a client instance"""
    return OpenRouterClient(api_key, model)