# walk-replace
Replace in directories and sub-directories.



## Setup

You need python 3.7+

```bash
pip install -r requirements.txt
```

## Usage

```
Usage: __main__.py [OPTIONS] CONFIG_FILE PATH

  Main module function.

Options:
  -e, --env-vars
  -s, --substitute-config-section TEXT
  -m, --substitute-mode TEXT
  -i, --include-file-match TEXT
  --help                          Show this message and exit.

```

## Config File

Config file format follows Python's [ConfigParser](https://docs.python.org/3/library/configparser.html) format, using extended interpolation.

If `--env-vars` flag is specified, a section `ENV` is added so environment variables could be referred in the config.

## Text Substitution

Following substitution modes are supported:

* `plaintext`

### Plaintext Substitution

The configuration setting `--substitute-config-section` parameter (default: `substitute`) specifies config section. This section is used to perform plaintext search and replace in files.

## Example

`myreplace.conf`

```properties
[DEFAULT]
ENV_CODE=${ENV:ENV_CODE}
WALK_SECRET=${ENV:WALK_SECRET}

[substitute]
__secret__=${WALK_SECRET}
__environment__=${ENV_CODE}

```

Interpolation keys `ENV:ENV_CODE` and `ENV:WALK_SECRET` will be replaced using values from environment.

Interpolation keys `ENV_CODE` and `WALK_SECRET` will be replaced using corresponding options from `DEFAULT` section. Before being replaced, the values of `ENV_CODE` and `WALK_SECRET` will be interpolated.

`Environment`

```
WALK_SECRET='$secret'
ENV_CODE='test'
```

`docs/my_document.txt`

```
secret is: __secret__
environment is: __environment__
```

File `docs/my_document.txt` will be processed and strings witch match options from `substitute` config section will be replaced with corresponding values.

```bash
python -m walk_replace -e myreplace.conf docs
```

Above command will process all documents in `docs` directory and perform replacement, overwriting the original content of the files. 

Replaced `docs/my_document.txt`

```
secret is: $secret
environment is: test
```



## Testing

```bash
# Install test dependencies
pip install -r requirements.test.txt
# Execute pytest test cases
pytest tests -vv --cov walk_replace --cov-report html --cov-report term
```

Optionally run `pylint`:

```bash
pylint walk_replace
```

