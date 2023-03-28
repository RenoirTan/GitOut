from pathlib import Path, PurePath
from urllib.parse import ParseResult

from git.repo import Repo

def get_repo_path(url: ParseResult, outdir: Path, use_url_path: bool) -> Path:
    url_path = Path(url.path)
    hostname = "git" if url.hostname is None else url.hostname
    repo_name = str(url_path)[1:] if use_url_path else url_path.name
    return (outdir / hostname) if repo_name == "" else (outdir / repo_name)


def clone(url: str, repo_path: Path) -> None:
    Repo.clone_from(url, repo_path, bare=True, mirror=True, recursive=True)