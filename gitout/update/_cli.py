from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path
import typing as t

from .walker import Walker

DESCRIPTION = "Update all bare repositories in a directory with git fetch."
EPILOG = ""

def make_parser() -> ArgumentParser:
    cli = ArgumentParser(
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=RawDescriptionHelpFormatter
    )
    cli.add_argument(
        "directories",
        action="append",
        nargs="*",
        type=Path,
        help="Directories where the repositories are stored."
    )
    cli.add_argument(
        "-r",
        "--recursive",
        action="count",
        default=0,
        help="Git fetch repositories in <directory> recursively. \
If -r is passed, gitout-update assumes that a directory that is a git \
repository will not contain repository mirrors in any of its subdirectories. \
If -rr is passed, gitout-update will git fetch all repositories, even if they \
are inside another repo."
    )
    cli.add_argument(
        "-i",
        "--include",
        action="append",
        default=[],
        help="List of regex patterns to determine which absolute paths should be fetched. \
All repos are included by default (i.e. r'.*' implied)."
    )
    cli.add_argument(
        "-e",
        "--exclude",
        action="append",
        default=[],
        help="List of regex patterns to determine which absolute paths should not be fetched. \
If the repo's path matches an exclude pattern, that repo will be excluded from even if \
it matches one of the include patterns."
    )
    return cli


def main():
    cli = make_parser()
    args = cli.parse_args()
    
    # argparse 'append' behaviour stores list of lists,
    # cannot use 'extend' because we are targetting python 3.7
    directories: t.List[Path] = args.directories[0]
    print(directories)
    if len(directories) == 0:
        directories.append(Path("."))
    for d in Walker(directories):
        print(d)