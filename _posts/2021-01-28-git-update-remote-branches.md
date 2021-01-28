---
layout: post
title:  "Update remote branches"
categories: [git]
---

When a remote branch is deleted from a repository, 
it can still show up in the local branch list.

Often
```bash
git fetch
```
should suffice. However, sometimes you'll have to do
```bash
git fetch --prune
```
See [this](https://stackoverflow.com/questions/32651627/how-do-i-update-the-remote-branches-list-in-git-from-the-server) StackOverflow discussion.
