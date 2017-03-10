# lektor-tipue-search

> This is under development

This is a plugin for Lektor that adds support for [tipue search](http://www.tipue.com/search/) to projects. When enabled it can generate json files in the `tipue-search/` folder automatically when the server (or build process) is run with the `-f tipue` flag.

## Enabling the Plugin

> The plugin isn't published yet so you have to clone the repo into the packages folder

```bash
mkdir papckages
cd packages
git clone git@github.com:rlaverde/lektor-tipue-search.git
```

## Configurations

There are some globals configurations:

`configs/tipue-search.ini:`

    output_directory = tipue_search


Also you should add an entry for any model that you want to be generated into de json file (it should start by `model`)

`configs/tipue-search.ini:`

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

fields.tags]
label = Tags
type = checkboxes
choices = some_tag, another_tag
```

and will generate a json file (for each alternative):

`tipue_search/tipue_search_en.ini:`

```json
[{"url": "/blog/example",
"text": "This is the blog Summary",
"title": "Blog Example",
"tags": ["example", "some_tag"]},

]
```

## Usage

```bash
lektor build -f tipue
```
