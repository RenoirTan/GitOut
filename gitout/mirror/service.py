from dataclasses import dataclass
from pathlib import Path
import typing as t

from .path import Filter

@dataclass
class Settings(object):
    username: t.Optional[str]
    password: t.Optional[str]
    token: t.Optional[str]
    outdir: Path
    preview: bool

class Service(object):
    def __init__(self, settings: Settings, *args, **kwargs) -> None:
        self.settings = settings
    
    def set_filter(self, pfilter: Filter) -> None:
        pass
    
    def setup(self) -> None:
        pass
    
    def validate(self) -> None:
        raise NotImplemented
    
    def request(self) -> None:
        pass
    
    def get_clone_urls(self) -> t.Optional[t.Iterable[str]]:
        return None