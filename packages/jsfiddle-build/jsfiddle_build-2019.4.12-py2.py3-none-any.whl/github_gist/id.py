#!/usr/bin/env python
"""print gist id"""
import click
import github_gist
import os

MODULE_NAME = "github_gist.id"
USAGE = 'python -m %s path' % MODULE_NAME
PROG_NAME = 'python -m %s' % USAGE


@click.command()
@click.argument('path', required=True)
def _cli(path):
    os.chdir(path)
    gist_id = github_gist.getid()
    if gist_id:
        print(gist_id)


if __name__ == "__main__":
    _cli()
