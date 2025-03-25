# Pre-Commit + Cz

[Back](../../README.md )

## Using Pre-Commit + Cz

```bash
git add .
cz commit
```

## Using a Dry Pre-Commit

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

#### Automatic start and commit

```bash
git commit -m "message"
```


#### Commit without verification

```bash
git commit -m "message" --no-verify
```
