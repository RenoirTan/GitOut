from argparse import ArgumentParser

DESCRIPTION = "Mirror your repositories from a remote location"

def main():
    cli = ArgumentParser(description=DESCRIPTION)
    args = cli.parse_args()