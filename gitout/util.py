import re


def confirm(prompt: str, assume_yes: bool = False) -> bool:
    if assume_yes:
        return True
    res = input(f"{prompt} [y/N] ")
    return re.match(r"^\s*[yY]\s*$", res) is not None