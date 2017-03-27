
# Blog 

## Adding a category

Add category to `_data/blog.yml`. For example:

```java
- name: Example
  href: '/blog/example'
```

Create a `html` file at the location specified under `href`. In this case `blog/example.html` with the following content:

```html
---
layout: blog
title: Example
permalink: /blog/example/
---
{% include category.html %}
```

The category is now ready for usage.
