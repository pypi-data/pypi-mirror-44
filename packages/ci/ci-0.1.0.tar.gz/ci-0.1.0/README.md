# ci

Easily run common CI tasks in Python

## Getting started

Install this package with

```bash
pip install ci
```

## Example usage

Run `pip install codecov` only when we are using Python 3.7

```bash
ci --only 3.7 pip install codecov
```

Run `flake8` on all Python versions except `2.7`

```bash
ci --skip 2.7 flake8
```

## License

This project is licensed under the MIT License. See the [LICENSE] file.

[LICENSE]: LICENSE
