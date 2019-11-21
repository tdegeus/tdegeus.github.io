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
