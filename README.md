<img src="https://storage.googleapis.com/iooxa-prod-1-wordpress/1/2020/09/logo-horizontal-dark.png" width="200" />

# templates

A community curated collection of Curvenote compatible LaTeX templates.

We're developing a template mini-language based on Jinja that allows us to create templates that can be used with Curvenote articles and notebooks, allowing a Template Creator to:

- control Curvenote's package loading and configuration relative to template specific packages
- define tags that can be used to assign content to specific parts of the template like `abstract` or `appendix`
- expose user options in the Curvenote UI to allow an end user to configure the template on export

The min-language is still in beta but we'll publish a link to docs here soon. In the meantime, if you want to add a template open and issue or let us know on the Curvenote [Community Slack](http://slack.curvenote.dev) and we'll configure it for you!

# Building a Compatible Template

Template folders should be placed in the `latex/` folder. The contents of a template folder should be:

- `template.yml` - The template specification file
- `template.tex` - The main template file with Curvenote template directives
- `example/` - contents of this folder are used to test pdf builds against the template
- `example/doc.yml` - Example DocModel data used to populate the template
- `example/content.tex` - Example content, usually taken from the original template
- `example/refs.bib` - Example bibligraphy, usually taken from the original template

## template specification (template.yml)

### metadata

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

### tagged

- abstract
- appendix
- acknowledgements

### options

#### builtins

- doc_class
- start_page
- page_numbers
- backlink

## Development - for project maintainers

- In order to test in the Curvenote development environment, push to or open a PR against `dev-test` and templates will be deployed to development alone
