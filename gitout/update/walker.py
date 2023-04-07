from __future__ import annotations
from pathlib import Path
import typing as t

from git import InvalidGitRepositoryError
from git.repo import Repo

from gitout.path import Filter

class Walker(t.Iterator, t.Iterable):
    def __init__(
        self,
        starting_dirs: t.List[Path],
        recursive: int,
        path_filter: t.Optional[Filter] = None
    ) -> None:
        self.starting_dirs: t.Set[Path] = set(starting_dirs)
        self.next_dirs: t.List[Path] = starting_dirs
        self.visited: t.Set[Path] = set()
        # self.recursive:
        #  0 -> search through starting_dirs but not its subdirectories
        #  1 -> search through subdirectories of the starting_dirs
        #  2 -> search subdirectories of repos for other directories
        self.recursive = recursive
        self.pfilter: Filter = Filter() if path_filter is None else path_filter
    
    def __iter__(self) -> Walker:
        return self
    
    def __next__(self) -> Repo:
        while len(self.next_dirs) > 0:
            working_dir = self.next_dirs.pop(0).resolve() # Symlink and absolute
            # Skip already visited dirs and non-directories
            if working_dir in self.visited or not working_dir.is_dir():
                continue
            # Set this work dir as visited
            self.visited.add(working_dir)
            # Repo object, None if working_dir is not a repo
            try:
                repo = Repo(working_dir)
            except InvalidGitRepositoryError as e:
                repo = None
            # Push subdirectories of work dir
            if (
                (working_dir in self.starting_dirs) or
                (self.recursive >= 1 and repo is None) or
                (self.recursive >= 2)
            ):
                self._extend(working_dir)
            # Return repo
            if repo is not None and self.pfilter.ok(str(working_dir)):
                return repo
        raise StopIteration
    
    # skip PermissionError from Path.iterdir
    def _extend(self, working_dir: Path) -> None:
        it = working_dir.iterdir()
        while True:
            try:
                child = next(it)
            except PermissionError as e:
                print(f"Skipping {e.filename}")
            except StopIteration:
                return
            else:
                if child.is_dir():
                    self.next_dirs.append(child)