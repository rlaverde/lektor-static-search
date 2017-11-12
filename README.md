# lektor-static-search

> This is under development

This is a plugin for [Lektor](https://www.getlektor.com/) that adds support for static search to projects. When enabled it can generate json files in the `static-search/` folder automatically when the server (or build process) is run with the `-f static-search` flag.

This json files can be used with js libraries like [Tipue search](http://www.tipue.com/search/) or [Lurn.js](http://lunrjs.com/).

## Enabling the Plugin

To enable the plugin add this to your project file, run this command while sitting in your Lektor project directory:

```bash
lektor plugins add lektor-static-search
```

## Configurations

There are some globals configurations:

`configs/static-search.ini:`

    output_directory = static_search


Also you should add an entry for any model that you want to be generated into de json file (it should start by `model`)

`configs/static-search.ini:`

```ini
[model.blog-post]
title = title
text = summary
tags = tags
```

The first part is the json key and the sepcond the model key, i.e the previous configuration correspod to a model:

`models/blog-post.ini:`

```ini
[model]
name = Blog Post

[fields.title]
label = Title
type = string

[fields.summary]
label = Summary
type = string

[fields.tags]
label = Tags
type = checkboxes
choices = some_tag, another_tag
```

and will generate a json file (for each alternative):

`static_search/static_search_en.json:`

```json
[{"url": "/blog/example",
"text": "This is the blog Summary",
"title": "Blog Example",
"tags": ["example", "some_tag"]},

]
```

## Usage

```bash
lektor build -f static-search
```
