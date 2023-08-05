# mkgist

A small utility for making gists. When I need to share code snippets online, the formatting always ends up totally messed up when I copy-paste manually. This alleviates that.

## Setup

### With pip

The easiest way to get a copy is through `pip3`:

    pip3 install mkgist

Annoying things happen, at least on my system, without `pip3`. I'll look into it at some point.

### Manual

To install dependencies, run `pip install -r requirements.txt` after installing. I don't use this within a virtual environment, but doing so would look something like this:

```
virtualenv -p $(which python3) $HOME/virtualenv/mkgist
source $HOME/virtualenv/mkgist/bin/activate
```

## Usage

    mkgist filenames [-d "description"] [--public] [--raw] [--nocopy]

- If no filenames are entered, the contents of the gist are read from STDIN.
- The location of the created gist is printed to stdout.
- Gists are secret by default, but can be made public with `--public`. (Secret gists aren't indexed by search engines)
- `--raw` returns a link to the raw hosted file, which you can then get with `curl` or `wget`. If multiple files are created with this flag, the URLs are always printed to stdout.
- By default, the URL of the created Gist is copied to the clipboard. `--nocopy` prints the link to stdout instead, not overwriting the clipboard.
