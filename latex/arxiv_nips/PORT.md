# Changes made during port

A list of changes made when porting the original tex and styles to the Curvenote template format.

- Based `template.tex` on a copy of `example.tex` shipped in the original
- Added `\input{curvenote.def}` to allow packages and configuration to be loaded
- Removed package includes that are already listed in Curvenote base packages
- Changed `fontenc` loading to use `\PassOptionsToPackage` for the `T1` option
- Inserted template blocks and vars for
  - Title
  - Date (Optional)
  - Authors - replaced placeholder content with Author, Affiliation blocks
- Using `doc.title` as `\shorttitle`
- Updated pdf metadata to pull `title` and `author` from LaTeX and `subject` and `keywords` from `doc.description` and `doc.tags`
- Added `abstract` as tagged block
- Added `keywords` from doc.tags
- Removed the non-bibtex option for inline references and pointed `bibliography` to `main.bib`
- Added `arxiv.sty` to root folder
- created `content.tex` with main content from `example.tex`
- Added optional `\usepackage{lipsum}` for testing purposes as example content in original uses it
- removed default fonts setting to allow compilation from xelatex and loaded lmodern
- added supported user defined options
