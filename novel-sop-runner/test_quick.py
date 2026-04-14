#!/usr/bin/env python3
"""Quick test - generate single chapter"""

import yaml
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.openrouter import OpenRouterClient
from src.state import StateManager
from src.prompts import get_chapter_content_prompt

config = yaml.safe_load(open("config.yaml"))
api_key = config["api_key"]
model = config["models"]["writing"]

print("Creating client...")
client = OpenRouterClient(api_key, model)

novel_info = {
    "title": "test-novel",
    "outline": "A detective solving mysteries",
    "genre": "suspense"
}

prompt = get_chapter_content_prompt(1, novel_info, "Chapter 1 outline: Detective finds first clue", None)

print("Sending request...")
messages = [{"role": "user", "content": prompt}]

response = client.chat(messages, system_prompt="你是小说作家。生成引人入胜的章节。", temperature=0.8, max_tokens=2000)

print("\n=== RESPONSE ===")
print(response[:1000])
print("=================")

Path("output/test-ch01.md").write_text(response)
print("\nSaved to output/test-ch01.md")