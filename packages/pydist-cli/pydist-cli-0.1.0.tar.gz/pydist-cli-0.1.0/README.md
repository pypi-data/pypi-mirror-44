# pydist-cli

A command-line interface for [PyDist](https://pydist.com).

## Configuration

The only thing you *need* to configure is your PyDist API key, via:
- the `PYDIST_API_KEY` environment variable, or
- the `--api-key` command-line flag, or
- a `.pydist.json` file in your home directory or the directory you are running `pydist` from.

## Usage

- Installation: `pydist install <package>` will install a package from your PyDist account. If
the package is not available on PyDist or you cannot connect to PyDist for some reason, it will
fall back to PyPI.
- Publish: `pydist publish` in the root directory of your package will build, check,
and upload your packages to PyDist, in both source and binary wheel form.
