# Waterloo Works

> A set of utilities used for interacting with Waterloo Works.

This project contains a set of utilities for interacting with Waterloo Works
for employers.

## Getting started

```shell
pip3 install waterlooworks

# Required for Apache Tika
brew cask install java8

# Required for pdftotext
brew install poppler # https://formulae.brew.sh/formula/poppler
```

This package depends on [tika-python](https://github.com/chrismattmann/tika-python) which requires
Java 7+.

This package relies on the great [pdf-redactor](https://github.com/JoshData/pdf-redactor) library created by
[Joshua Tauberer](https://github.com/JoshData). The the core of the `pdf-redactor` library is embedded in `waterlooworks`
since it is not available on pypi.

## Usage

```
$ waterlooworks --help
Usage: waterlooworks [OPTIONS] COMMAND [ARGS]...

  A set of utilities for analyzing and processing WaterlooWorks intern
  packages

Options:
  --help  Show this message and exit.

Commands:
  anonymize  Anonymize WaterlooWorks intern packages
  score      Analyze WaterlooWorks intern packages
```

### Download the full resume package for interns from Waterloo Works

When logged into Waterloo Works, copy and past the contents of `ww.js` into the
console. This script will trigger a dowload of the intern resume packages into
your browser's `Downloads` folder. The script only downloads the packages visible
on the current page, and not on additional paginated application pages.

```shell
pbcopy < ww.js

# 1. Log onto Waterloo Works, and navigate the the page containing applications
#    for your posting.
# 2. Paste into the console
# 3. Resumes for that page will be downloaded.
```

### Print a table of scored / ranked waterlooworks packages

This script will output the metadata for resumes, in descending order based on
the mean of term averages.

```
$ waterlooworks score data
1337 packages found
data/foo.pdf
data/bar.pdf
data/baz.pdf
...
| Foo | 4A | 11111111 | 4A Software Engineering |  {'OUTSTANDING': 2, 'EXCELLENT': 2} | [80.0, 80.0, 80.0, 80.0, 80.0] |
...
```

## Anonymize Packages

This is a simple attempt to try and remove references to names, gender and other information irrelevant
to a package.

```
 $ waterlooworks anonymize ~/wwdata/ ~/anon1
1337 packages found
data/foo.pdf
data/bar.pdf
data/baz.pdf
...
```

# Caveats

These utilities are _best effort_ and do not guarantee the data is accurate. If the format for packages changes,
this library will break.

These scripts should not be the sole way of evaluating candidates, they should augment typical hiring workflows.

# Contributing

If you have any ideas, just [open an issue](https://github.com/dang3r/waterlooworks) and tell me what you think.

If you'd like to contribute, please fork the repository and make changes as
you'd like. Pull requests are warmly welcome.

# Licensing

MIT License.
