# Contributors Guide

## How to Contribute

**NOTE the rest of this guide needs an update [#37]()**

## Building a Compatible Template

Template folders should be placed in the `latex/` folder. The contents of a template folder should be:

- `template.yml` - The template specification file
- `template.tex` - The main template file with Curvenote template directives
- `example/` - contents of this folder are used to test pdf builds against the template
- `example/doc.yml` - Example DocModel data used to populate the template
- `example/content.tex` - Example content, usually taken from the original template
- `example/refs.bib` - Example bibligraphy, usually taken from the original template

### template specification (template.yml)

#### metadata

The following are valid fields. Descriptions provided where needed.

- `title` (required)
- `description` (required)
- `author` (required) - details the person who contributed the Curvenote port of this template
  - `name` (required)
  - `github` - github username
  - `twitter` - twitter handle
  - `affiliation`
- `source` - the name of the original source of the template, possibly a publishing body
- `version` (required) - freeform semantic version of the port of the template
- `license` (required) - a recognized license name e.g. MIT, CC-BY, CC-BY-SA
- `tag` (required) - a list of tags
  - `tagname` (required)
  - `tagname`
- `links` (required)
  - `source` - a download link to the source of the original tex, class, styles

#### tagged

- abstract
- appendix
- acknowledgements

#### options

##### builtins

- doc_class
- start_page
- page_numbers
- backlink

### Development - for project maintainers

- Branch off `main` in order to make changes or add a template
- Once you are ready, test in the Curvenote development environment by pushing your branch and opening a PR against `dev`
- New and changed templates will be deployed automatically to the Curvenote development servers
