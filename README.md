# GitOut

Manage your local git repository mirrors.

## Setup and Install

Clone the repository.

```bash
git clone https://github.com/RenoirTan/GitOut
cd GitOut
```

**Optional>** Create a virtual environment.

```bash
python -m venv venv/
source venv/bin/activate
```

Install package.

```bash
pip install .

# For testing purposes...
pip install --editable .
```

## Mirror

`gitout-mirror` obtains a list of repositories from a `service` like Github, then clones each of them into the current directory with git's `--mirror` flag.

```bash
# This command clones all public and private repos which you are a contributor
# of. You can pass your token using the `-t` option.
gitout-mirror github -t ghp_<token>

# You can specify another directory to clone the repositories to using the `-o`
# option.
gitout-mirror github -t ghp_<token> -o ~/backups

# `-w` tells gitout-mirror to list all repositories that would be cloned and
# what path they would be cloned to, without actually cloning them.
gitout-mirror github -t ghp_<token> -o ~/backups -w

# If you want to use the URL path as the local filesystem path for each repo,
# pass the `-y` flag.
gitout-mirror github -t ghp_<token> -o ~/backups -y
```