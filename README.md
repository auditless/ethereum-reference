# ethereum-reference
A Solidity and Vyper reference guide

## Outside dependencies

- `python ==3.7`
- `pipenv`
- OPTIONAL, only needed for live reload development: `entr` (`brew install entr`)

## Using the repository

### Resolving project dependencies

```bash
make install
```

### Running tests (`pytest)

```bash
make test
```

### Typechecking (`mypy`)

```bash
make types
```
