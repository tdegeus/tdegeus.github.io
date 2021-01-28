---
layout: post
title:  "Partial clone"
categories: [git]
---

Recently I came across a few repositories with a very rich history 
(corresponding to a huge disk-space, requiring also a significant downloading time).
If one is not particularly interested in the histories, on can
partially (shallow) clone a repository:

```bash
git clone --depth=5 ...
```
