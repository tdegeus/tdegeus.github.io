---
layout: post
title:  "Update a git fork"
categories: [git]
---

To update a git fork, proceed as follows:

```bash
git remote add upstream {url_to_remote}
git fetch upstream
git rebase upstream/master
```

Note that a common usage of a fork is to open a pull-request, in particular from a branch on the fork:

```bash
git checkout -b patch
... # commits here
```

Once merged, you can delete the branch:

```bash
git checkout master
git branch -D patch
git push --delete origin patch
```
