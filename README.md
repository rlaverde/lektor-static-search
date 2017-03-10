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
