# Instructor Examples

![PyPI version](https://img.shields.io/pypi/v/instructor_examples.svg)

Copy github examples to your local environment without needing to clone the entire repository.

* Created by **[Daniel Mouris](https://github.com/dgmouris)**
  * PyPI: https://pypi.org/user/dgmouris/
* PyPI package: https://pypi.org/project/instructor_examples/
* Free software: MIT License

## Features

Copies files and folders from GitHub to a local environment.

## Documentation

Documentation is built with [Zensical](https://zensical.org/) and deployed to GitHub Pages.

* **Live site:** https://dgmouris.github.io/instructor_examples/
* **Preview locally:** `just docs-serve` (serves at http://localhost:8000)
* **Build:** `just docs-build`

API documentation is auto-generated from docstrings using [mkdocstrings](https://mkdocstrings.github.io/).

Docs deploy automatically on push to `main` via GitHub Actions. To enable this, go to your repo's Settings > Pages and set the source to **GitHub Actions**.

## Development

To set up for local development:

```bash
# Clone your fork
git clone git@github.com:your_username/instructor_examples.git
cd instructor_examples

# Install in editable mode with live updates
uv tool install --editable .
```

This installs the CLI globally but with live updates - any changes you make to the source code are immediately available when you run `instructor_examples`.

Run tests:

```bash
uv run pytest
```

Run quality checks (format, lint, type check, test):

```bash
just qa
```

## Author

Instructor Examples was created in 2026 by Daniel Mouris.

Built with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.
