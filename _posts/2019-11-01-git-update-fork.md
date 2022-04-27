---
layout: post
title:  "Update a git fork"
categories: [git]
---

## Using GitHub command-line tools

See [documentation](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork#syncing-a-fork-with-the-github-cli)

```bash
gh repo sync fork_owner/fork_name
````

## Manually

To update a git fork, proceed as follows:

```bash
git remote add upstream {url_to_remote}
git fetch upstream
git rebase upstream/main
```

## Removing a branch

Note that a common usage of a fork is to open a pull-request, in particular from a branch on the fork:

```bash
git checkout -b patch
... # commits here
```

Once merged, you can delete the branch:

```bash
git checkout main
git branch -D patch
git push --delete origin patch
```
