from __future__ import annotations
from pathlib import Path
import typing as t

class Walker(object):
    def __init__(
        self,
        starting_dirs: t.List[Path]
    ) -> None:
        self.next_dirs: t.List[Path] = starting_dirs
        self.visited: t.Set[Path] = set()
    
    def __iter__(self) -> Walker:
        return self
    
    def __next__(self) -> Path:
        while len(self.next_dirs) > 0:
            working_dir = self.next_dirs.pop(0).resolve() # Symlink and absolute
            # Skip already visited dirs and non-directories
            if working_dir in self.visited or not working_dir.is_dir():
                continue
            # Push subdirectories of work dir
            self.next_dirs.extend(filter(lambda p: p.is_dir(), working_dir.iterdir()))
            # Set this work dir as visited
            self.visited.add(working_dir)
            # Return work dir
            return working_dir
        raise StopIteration