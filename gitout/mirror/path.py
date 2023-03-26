import re
import typing as t
from urllib.parse import ParseResult

class Filter(object):
    def __init__(self, includes: t.Iterable[str] = [], excludes: t.Iterable[str] = []) -> None:
        self.includes = [re.compile(i) for i in includes]
        self.excludes = [re.compile(e) for e in excludes]
    
    def __call__(self, path: str) -> bool:
        return self.ok(path)
    
    def _includes(self, path: str) -> bool:
        return (
            len(self.includes) == 0 or # match all
            any(map(lambda r: r.search(path) is not None, self.includes))
        )
    
    def _excludes(self, path: str) -> bool:
        return any(map(lambda r: r.search(path) is not None, self.excludes))
    
    def ok(self, path: str) -> bool:
        if self._excludes(path):
            return True
        else:
            return self._includes(path)
    
    def filter(self, urls: t.Iterable[ParseResult]) -> t.Iterator[ParseResult]:
        return filter(lambda u: self.ok(u.path), urls)