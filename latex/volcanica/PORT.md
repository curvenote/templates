# Changes made during port

The steps taken during the port were:

- `template.tex` is based on `original/a.tex` started with a copy-paste
- Added Title retaining the `\sc` command
- Added first author command wrapped in `options.blind`, if blind will default to empty
  - included `et al.` style for multiple authors
- Added Year
- modified initial package loading to dedupe and handle options
  - removed:
    - `[sectionbib,square,elide]{natbib}`
      - in template.yml:
        - `natbib: true`
        - `bibstyle: false`
        - `citestyle: false`
  - moved options out to PassOptionsToPackage for:
    - `[french,english]babel`
    - `[sectionbib,square,elide]{natbib}`
  - Added watermark with `options.watermark`
  - Added lineno with `options.line_numbers`
  - Added authors and affiliations with:
    - `options.blind`
    - corresponding author from author object
  - Added language choice option (english, french)
  - Added abstract as tagged block
  - Added acknowledgments as tagged block, if not blind
  - Added author contributions as tagged block, if not blind
  - Added data availability as tagged block
  - Removed the `\pdfsuppressptexinfo15` as xetex does not support it, added TODO for making the build reproducible
