from dataclasses import dataclass
from pathlib import Path
import typing as t

@dataclass
class Settings(object):
    username: t.Optional[str]
    password: t.Optional[str]
    token: t.Optional[str]
    outdir: Path
    list: bool

class Service(object):
    def __init__(self, settings: Settings, *args, **kwargs) -> None:
        self.settings = settings
    
    def setup(self) -> None:
        pass
    
    def validate(self) -> None:
        raise NotImplemented
    
    def request(self) -> None:
        pass
    
    def get_clone_urls(self) -> t.Optional[t.Iterable[str]]:
        return None