# Rotation Helper

## Building
- `python -m venv .venv`
- `.\.venv\Scripts\activate`
- `pip install -e .` or `pip install -e .[dev]`
- `deactivate`

# Linting
- `pylint $(git ls-files '*.py') --disable=missing-docstring`
- `autopep8 --in-place --aggressive --aggressive $(git ls-files '*.py')`
