# mod-ngarn 

[![CircleCI](https://circleci.com/gh/Proteus-tech/mod-ngarn.svg?style=svg)](https://circleci.com/gh/Proteus-tech/mod-ngarn) [![PyPI version](https://badge.fury.io/py/mod_ngarn.svg)](https://badge.fury.io/py/mod_ngarn)

## Usage
```
Usage: mod-ngarn [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create-table     Create mod-ngarn queue table
  run              Run mod-ngarn job
  wait-for-notify  Wait and listening for NOTIFY
```

## Installation
```
pip install mod-ngarn
```

## Run modngarn
```
Usage: mod-ngarn run [OPTIONS]

Options:
  --queue-table TEXT  Queue table name (Default: os.getenv("DBTABLE",
                      "public.modngarn_job"))
  --limit INTEGER     Limit jobs (Default: 300)
  --max-delay FLOAT   Max delay for failed jobs (seconds) (Default: None)
  --help              Show this message and exit.

Returns:
  Exit code 0   Success run all <--limit> job
  Exit code 3   Success run but has job less than <--limit> 
```

## Create modngarn job queue table
```
Usage: mod-ngarn create-table [OPTIONS]

Options:
  --queue-table TEXT  Queue table name (Default: os.getenv("DBTABLE",
                      "public.modngarn_job"))
  --help              Show this message and exit.
```

## Wait for notify
```
Usage: mod-ngarn wait-for-notify [OPTIONS]

  Wait and listening for NOTIFY

Options:
  --queue-table TEXT  Queue table name (Default: os.getenv("DBTABLE",
                      "public.modngarn_job"))
  --help              Show this message and exit.
```
## Dev
### Required
- pipenv (https://github.com/pypa/pipenv)
- running PostgreSQL (`psql` should work)
- python 3.7

#### Setup
```
pipenv install --python 3.7
pipenv shell
```

#### Runtests
```
./runtests.sh
```

#### Publish to PyPi
```
flit publish
```
