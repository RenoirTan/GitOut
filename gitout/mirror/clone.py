from pathlib import Path, PurePath
import typing as t
from urllib.parse import ParseResult

from git.repo import Repo
from git.remote import RemoteProgress
from tqdm import tqdm


class Progress(RemoteProgress):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._my_pbar = tqdm()
    
    def __call__(self, *args, **kwargs) -> t.Optional[str]:
        return self.update(*args, **kwargs)
    
    def update(
        self,
        op_code: int,
        cur_count: t.Union[str, float],
        max_count: t.Union[str, float, None] = None,
        message: str = ""
    ) -> t.Optional[str]:
        self._my_pbar.total = max_count
        self._my_pbar.n = cur_count
        self._my_pbar.refresh()


def get_repo_path(url: ParseResult, outdir: Path, use_url_path: bool) -> Path:
    url_path = PurePath(url.path)
    hostname = "git" if url.hostname is None else url.hostname
    repo_name = str(url_path)[1:] if use_url_path else url_path.name
    return (outdir / hostname) if repo_name == "" else (outdir / repo_name)


def clone(url: str, repo_path: Path) -> None:
    Repo.clone_from(url, repo_path, progress=Progress(), bare=True, mirror=True, recursive=True)