# Instructions for Contributors

This repository contains **pyfpgrowth**, a Python implementation of the
Frequent Pattern Growth algorithm.

## Repository layout
- `pyfpgrowth/` holds the library code.
- `tests/` contains unit tests.
- `docs/` provides Sphinx documentation.

## Development guidelines
- Target Python 3.8 or newer and keep type hints.
- Follow PEP 8 style. Run `flake8 pyfpgrowth tests` to lint.
- Add or update tests for any code change.
- Run `python setup.py test` and ensure all tests pass before committing.
- Optionally run `tox` to test against multiple Python versions.
- When updating docs, build them with `make -C docs html`.
- Keep docstrings short and in double quotes.

