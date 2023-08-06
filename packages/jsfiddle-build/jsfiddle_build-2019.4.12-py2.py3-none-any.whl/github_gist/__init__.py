#!/usr/bin/env python
import github_remote
import os
import public

"""
git@gist.github.com:{id}.git
https://gist.github.com/{id}.git
"""

@public.add
def isgit():
    """return True if current directory is a git repository, else False"""
    path = os.getcwd()
    while path and len(path) > 1:
        if os.path.exists(os.path.join(path, ".git")):
            return True
        path = os.path.dirname(path)
    return False


@public.add
def getid():
    """return a string with gist id"""
    if not isgit():
        return
    url = github_remote.url()
    if not url:
        return
    if "git@" in url:
        return url.split(":")[1][:-4] if "/" in url else None
    if "https://" in url:
        return "%s/%s" % (url.split("/")[-2], url.split("/")[-1][:-4]) if url.count("/") == 4 else None
    raise ValueError("invalid url %s" % url)


@public.add
def isgist():
    """return True if repository is a github gist, else False"""
    return id() is not None
