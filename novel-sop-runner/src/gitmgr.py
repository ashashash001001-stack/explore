"""Git operations for novel generation"""

import subprocess
from pathlib import Path


class GitManager:
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.repo_path = self.output_dir.parent
    
    def init(self):
        result = subprocess.run(
            ["git", "status"],
            cwd=self.repo_path,
            capture_output=True
        )
        if result.returncode != 0:
            subprocess.run(["git", "init"], cwd=self.repo_path)
    
    def add(self, files):
        file_list = " ".join(str(f) for f in files)
        subprocess.run(f"git add {file_list}".split(), cwd=self.repo_path)
    
    def commit(self, message: str):
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=self.repo_path
        )
    
    def push(self):
        subprocess.run(["git", "push"], cwd=self.repo_path)
    
    def auto_commit_chapter(self, ch_num: int, word_count: int):
        ch_file = self.output_dir / "chapters" / f"ch{ch_num:02d}.md"
        if ch_file.exists():
            self.add([ch_file])
            self.commit(f"chore: generate chapter {ch_num} ({word_count} words)")
    
    def auto_commit_state(self):
        state_file = self.output_dir / "global-state.json"
        if state_file.exists():
            self.add([state_file])
            self.commit("chore: update global state")