import re
import typing as t

class Filter(object):
    def __init__(self, include: t.Optional[str]=None, exclude: t.Optional[str]=None) -> None:
        self.include = re.compile(r".*" if include is None else include)
        self.exclude = None if exclude == None else re.compile(exclude)
    
    def __call__(self, path: str) -> bool:
        return self.ok(path)
    
    def ok(self, path: str) -> bool:
        # if excluded, no
        # if included, yes
        if self.exclude is not None and self.exclude.search(path) is not None:
            return False
        return self.include.search(path) is not None