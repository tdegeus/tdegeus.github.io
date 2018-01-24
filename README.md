
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

# Publishing

## Previewing

Open terminal, and run:

```bash
jekyll serve 
```

the preview can be viewed on http://127.0.0.1:4000/ 

## Commit changes

```bash
git add -A   # (only use -A to commit all changes)
git commit -m "type your message here"
git push 
```

## Publish site

```bash 
jekyll build 
cp -r _site/* _gh-pages/ 
cd _gh-pages
git add -A   # (only use -A to commit all changes)
git commit -m "type your message here"
git push 
```

