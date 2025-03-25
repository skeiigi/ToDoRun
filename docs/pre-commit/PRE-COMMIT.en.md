# Pre-Commit

[Back](../../README.md)

#### Updating dependencies

```bash
pip install -r requirements.txt
```

#### Installing linters and formatters

```bash
pre-commit install
```

#### Manual start without commit

```bash
pre-commit run --all-files
```

#### Automatically start and commit

```bash
git commit -m "message"
```


#### Commit without verification

```bash
git commit -m "message" --no-verify
```
