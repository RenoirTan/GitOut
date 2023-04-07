from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path
import re
import typing as t

from git.repo import Repo
from tqdm import tqdm

from gitout.path import Filter
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
    cli.add_argument(
        "-s",
        "--skip",
        action="store_true",
        help="Skip a remote if an error occurs while fetching it."
    )
    cli.add_argument(
        "-y",
        "--yes",
        "--assume-yes",
        action="store_true",
        help="Automatically assumes 'yes' as answer to the prompt asking whether to update the \
of repos."
    )
    return cli


def confirm(assume_yes: bool = False) -> bool:
    if assume_yes:
        return True
    res = input("These repositories will be updated. Do you want to continue? [y/N] ")
    return re.match(r"^\s*[yY]\s*$", res) is not None


def update(repo: Repo, skip_error: bool = False) -> int:
    tqdm.write(f"Updating {repo.working_dir}")
    count = 0
    for remote in repo.remotes:
        tqdm.write(f"    {remote.name} -> {remote.url}")
        try:
            remote.fetch(verbose=True)
        except Exception as e:
            if skip_error:
                tqdm.write("An error occurred trying to fetch the remote!")
                tqdm.write(str(e))
            else:
                raise e
        else:
            count += 1
    return count


def main():
    cli = make_parser()
    args = cli.parse_args()
    
    # argparse 'append' behaviour stores list of lists,
    # cannot use 'extend' because we are targetting python 3.7
    directories: t.List[Path] = args.directories[0]
    if len(directories) == 0:
        directories.append(Path("."))
    
    pfilter = Filter(includes=args.include, excludes=args.exclude)
    
    repos: t.List[Repo] = list(Walker(directories, args.recursive, pfilter))
    print("Found these repositories:")
    for repo in repos:
        print(f" -> {repo.working_dir}")
    if not confirm(args.yes):
        print("Aborting!")
        return
    remote_count = 0
    for r in tqdm(repos, unit="repo"):
        remote_count += update(r, args.skip)
    print(f"Updated {len(repos)} repositories and fetched {remote_count} remotes.")