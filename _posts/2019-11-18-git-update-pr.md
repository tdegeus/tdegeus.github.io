---
layout: post
title:  "Update pull-request on GitHub"
categories: [git]
---

With only one remote:

```none
git fetch
git checkout test
```

With more than one remote:

```none
git checkout -b test origin/test
```

```
git checkout -t origin/test
```

See:

* [This answer of StackOverflow](https://stackoverflow.com/a/1783426/2646505)
