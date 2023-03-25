from argparse import ArgumentParser
import typing as t

from .service import Settings, Service
from .github import GithubService

DESCRIPTION = "Mirror your repositories from a remote location"

def make_parser() -> ArgumentParser:
    cli = ArgumentParser(description=DESCRIPTION)
    cli.add_argument("service")
    cli.add_argument("-U", "--username")
    cli.add_argument("-P", "--password")
    cli.add_argument("-T", "--token")
    cli.add_argument("-o", "--out")
    cli.add_argument("--list")
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
    
    service_type = get_service(args.service)
    if service_type == None:
        raise ValueError(f"'{args.service}' is not supported.")
    settings = Settings(
        username=args.username,
        password=args.password,
        token=args.token,
        outdir=args.out,
        list=args.list
    )
    service = service_type(settings)
    service.setup()
    service.request()
    
    urls = service.get_clone_urls()
    if urls == None:
        raise ValueError("No clone urls found.")
    for url in urls:
        print(url)