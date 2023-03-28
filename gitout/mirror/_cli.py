from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path
import typing as t
from urllib.parse import urlparse

from .clone import get_repo_path, clone
from .path import Filter
from .service import Settings, Service
from .github import GithubService

DESCRIPTION = "Mirror your repositories from a remote location."

EPILOG = """\
Examples
--------

  # --include flag tells gitout-mirror to backup repos whose name start with
  # 'A' or 'a'.
  gitout-mirror github --token ghp_... --out ~/backups/ --include '/[Aa][^/]*/?$'
"""

def make_parser() -> ArgumentParser:
    cli = ArgumentParser(
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=RawDescriptionHelpFormatter
    )
    cli.add_argument("service", help="Name of service to query. For example: github")
    cli.add_argument(
        "-u",
        "--username",
        help="Username used for login. Use --token instead if <service> requires it."
    )
    cli.add_argument(
        "-p",
        "--password",
        help="Password used for login. Use --token instead if <service> requires it."
    )
    cli.add_argument("-t", "--token", help="Token used to access whatever API <service> needs.")
    cli.add_argument(
        "-o",
        "--out",
        default=".",
        help="Output directory. All repos mirrored will be stored here."
    )
    cli.add_argument(
        "-i",
        "--include",
        action="append",
        default=[],
        help="List of regex patterns to determine whether to include a repo based on its URL path. \
All repos are included by default (i.e. r'.*' implied)."
    )
    cli.add_argument(
        "-e",
        "--exclude",
        action="append",
        default=[],
        help="List of regex patterns to determine whether to exclude a repo based on its URL path. \
If the repo's path matches an exclude pattern, that repo will be excluded from mirroring even if \
it matches one of the include patterns."
    )
    cli.add_argument(
        "-y",
        "--use-url-path",
        action="store_true",
        help="Use the URL path as the repo path."
    )
    cli.add_argument(
        "-w",
        "--preview",
        action="store_true",
        help="Preview actions instead of doing them."
    )
    return cli


def get_service(name: str) -> t.Optional[t.Type[Service]]:
    lower_name = name.lower()
    if lower_name == "github":
        return GithubService
    else:
        return None


def main():
    cli = make_parser()
    args = cli.parse_args()
    print(args)
    
    pfilter = Filter(includes=args.include, excludes=args.exclude)
    
    service_type = get_service(args.service)
    if service_type == None:
        raise ValueError(f"'{args.service}' is not supported.")
    settings = Settings(
        username=args.username,
        password=args.password,
        token=args.token,
        outdir=args.out,
        preview=args.preview
    )
    service = service_type(settings)
    service.set_filter(pfilter)
    service.setup()
    service.request()
    
    urls = service.get_clone_urls()
    if urls == None:
        raise ValueError("No clone urls found.")
    outdir: str = "." if args.out == "" else args.out
    for url in urls:
        print(f"Cloning from {url}")
        repo_path = get_repo_path(urlparse(url), Path(outdir), args.use_url_path)
        print(f"  to {repo_path}")
        if not args.preview:
            clone(url, repo_path)