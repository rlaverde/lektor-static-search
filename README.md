# lektor-tipue-search

> This is under development

This is a plugin for Lektor that adds support for [tipue search](http://www.tipue.com/search/) to projects. When enabled it can generate json files in the `tipue-search/` folder automatically when the server (or build process) is run with the `-f tipue` flag.

## Enabling the Plugin

To enable the plugin add this to your project file, run this command while sitting in your Lektor project directory:

```bash
lektor plugins add lektor-tipue-search
```

## Configurations

You should add an entry for any model taht you want to be generated into de json file

`configs/tipue-search.ini:`

    [blog-post]
    title = title
    text = summary
    tags = tags


## Usage

```bash
lektor build -f tipue
```
