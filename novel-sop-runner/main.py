#!/usr/bin/env python3
"""
Novel SOP Runner - Automated Novel Generation
基于 SOP v7.1
"""

import os
import sys
import yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.state import StateManager
from src.generator import ChapterGenerator
from src.quality import QualityChecker


def load_config():
    config_path = Path("config.yaml")
    if config_path.exists():
        with open(config_path) as f:
            return yaml.safe_load(f)
    return {}


def main():
    print("=" * 50)
    print("Novel SOP Runner")
    print("=" * 50)
    
    config = load_config()
    api_key = config.get("api_key")
    models = config.get("models", {})
    output_dir = config.get("output_dir", "output/")
    
    if not api_key:
        print("Error: API key not found in config.yaml")
        return
    
    novel_info = {
        "title": "test-novel",
        "outline": "A thriller about a detective solving mysteries in a small town",
        "genre": "suspense",
        "chapters": 3
    }
    
    print(f"\nTitle: {novel_info['title']}")
    print(f"Chapters: {novel_info['chapters']}")
    print(f"Model: {models.get('writing')}")
    print("=" * 50)
    
    state_mgr = StateManager(output_dir)
    generator = ChapterGenerator(api_key, models)
    checker = QualityChecker(api_key, models.get("checking", models.get("writing")))
    
    state_mgr.init(novel_info)
    
    for ch_num in range(1, novel_info["chapters"] + 1):
        print(f"\n--- Chapter {ch_num}/{novel_info['chapters']} ---")
        
        prev_state = state_mgr.get_previous_state(ch_num)
        chapter = generator.generate(ch_num, novel_info, prev_state)
        state_mgr.save_chapter(ch_num, chapter)
        
        issues = checker.check(chapter, prev_state)
        if issues:
            print(f"  Issues: {issues}")
        
        print(f"  Done! {len(chapter)} chars")
    
    state_mgr.finalize()
    
    print("\n" + "=" * 50)
    print("Done! Output:", output_dir)
    print("=" * 50)


if __name__ == "__main__":
    main()