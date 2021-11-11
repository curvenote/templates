<img src="https://curvenote.dev/images/logo.png" width="200" />

# Open Community Templates

A community curated collection of Curvenote compatible templates.

These templates allow us to export Articles and Notebooks in Curvenote as typeset and formatted documents. This means we can export to PDF and LaTeX formats while complying with an original source template, that would have been provided by a particular journal, conference organizer or university.

The templates here can also be browsed on the [Curvenote website](https://curvenote.com/templates).

Currently, all templates are LaTeX based but as of October'21, Curvenote can now [export to Microsoft Word](https://curvenote.com/blog/curvenote-microsoft-word-export). As this beta feature progresses, MS Word templates will appear here too.

## Contributing

Curvenote templates are LaTeX documents that have been marked up with a template syntax allowing them to be dynamically turned into documents with unique content and data.

Writing your own template from scratch should be easy if you know LaTeX or given a LaTeX template from your university or a publisher, it should be relatively easy to turn that template into a Curvenote template.

Once a new template is committed to the `main` branch in this repository, Curvenote will automatically add it to the list of available templates for export. 🧙🏼

There are a couple of different ways to get a template added to this repository:

- 📝 [open an issue](https://github.com/curvenote/templates/issues) - tell us about the template you'd like added. Provide a link to the template if it's online, or attach the files if you have them.
- 🏋🏽‍♀️ [open a PR](https://github.com/curvenote/templates/pulls) - with a port of the template. Even if it's partial or barely started we'll help test and get it over the line.

Templates in this repo can be tested and used in conjunction with [curvenote-template](https://github.com/curvenote/curvenote-template) a python based command line tool.
You'll need `python >= 3.6` to use it but you'll not need to write any code.

The README in that repository has plently of details on the basic templating syntax we use (which is based on our own custom Jinja environment) and how to run the tool.

For more details on contributing, learning about the structure of Curvenote templates specifically and how to build one. See the [Contributors Guide](CONTRIBUTING.md).
