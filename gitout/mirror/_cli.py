from argparse import ArgumentParser

DESCRIPTION = "Mirror your repositories from a remote location"

def make_parser() -> ArgumentParser:
    cli = ArgumentParser(description=DESCRIPTION)
    cli.add_argument("service", nargs=1)
    cli.add_argument("-U", "--username")
    cli.add_argument("-P", "--password")
    cli.add_argument("-T", "--token")
    cli.add_argument("-o", "--out")
    cli.add_argument("--list")
    return cli

def main():
    cli = make_parser()
    args = cli.parse_args()
    print(args)