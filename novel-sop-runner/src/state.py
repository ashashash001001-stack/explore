"""State Manager - Global state tracking"""

import json
from pathlib import Path


class StateManager:
    """Manages global state for novel generation"""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.chapters_dir = self.output_dir / "chapters"
        self.state_file = self.output_dir / "global-state.json"
    
    def init(self, novel_info: dict):
        """Initialize state"""
        # Create directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.chapters_dir.mkdir(parents=True, exist_ok=True)
        
        # Save novel info
        self.novel_info = novel_info
        self.state = {
            "novel": novel_info,
            "current_chapter": 0,
            "chapters": [],
            "hooks": [],  # 懸念追踪
            "foreshadows": [],  # 伏筆追蹤
        }
        
        with open(self.state_file, "w") as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)
        
        print(f"  Initialized: {self.output_dir}")
    
    def get_previous_state(self, ch_num: int):
        """Get state from previous chapter"""
        if ch_num == 1:
            return None
        
        prev_file = self.chapters_dir / f"ch{ch_num-1:02d}.md"
        if prev_file.exists():
            with open(prev_file) as f:
                content = f.read()
            
            # Extract state record from end
            if "全局狀態記錄" in content:
                # Parse state from chapter
                return self._parse_state_from_chapter(content)
        
        return self.state
    
    def _parse_state_from_chapter(self, content: str):
        """Extract state from chapter content"""
        # Simple extraction - look for state record
        lines = content.split("\n")
        state = {}
        in_state = False
        
        for line in lines:
            if "全局狀態記錄" in line:
                in_state = True
                continue
            if in_state and line.strip().startswith(">"):
                continue
            if in_state and line.strip() == "":
                break
        
        return state
    
    def save_chapter(self, ch_num: int, content: str):
        """Save chapter file"""
        # Update state
        self.state["current_chapter"] = ch_num
        self.state["chapters"].append({
            "number": ch_num,
            "word_count": len(content)
        })
        
        # Save chapter
        chapter_file = self.chapters_dir / f"ch{ch_num:02d}.md"
        with open(chapter_file, "w") as f:
            f.write(content)
        
        # Save state
        with open(self.state_file, "w") as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)
        
        print(f"  Saved: {chapter_file}")
    
    def finalize(self):
        """Finalize and create summary"""
        self.state["status"] = "completed"
        
        with open(self.state_file, "w") as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)
        
        # Create TOC
        toc = "# 目錄\n\n"
        for ch in self.state["chapters"]:
            toc += f"- 第{ch['number']:02d}章 ({ch['word_count']}字)\n"
        
        with open(self.output_dir / "toc.md", "w") as f:
            f.write(toc)
        
        print(f"  Created TOC: {self.output_dir / 'toc.md'}")