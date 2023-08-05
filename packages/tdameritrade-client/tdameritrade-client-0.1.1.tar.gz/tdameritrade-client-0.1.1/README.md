[![pipeline status](https://gitlab.com/tdameritrade-tools/tdameritrade-client/badges/master/pipeline.svg)](https://gitlab.com/tdameritrade-tools/tdameritrade-client/commits/master) [![Documentation Status](https://readthedocs.org/projects/tdameritrade-client/badge/?version=latest)](https://tdameritrade-client.readthedocs.io/en/latest/?badge=latest)[![coverage report](https://gitlab.com/tdameritrade-tools/tdameritrade-client/badges/master/coverage.svg)](https://gitlab.com/tdameritrade-tools/tdameritrade-client/commits/master)


# TDAmeritrade Client

A tool that links to the TDA API to perform requests.

Read the [docs](https://tdameritrade-client.readthedocs.io/en/latest/?#).

## Installation:
Run `pip install tdameritrade-client` within a virtual environment

## Usage
The package has two uses as of now:
1. Run the oauth flow against a developer app.
2. Use an access token to request account positions.

To get started, use the following code snippet:

``` python
from tdameritrade_client.client import TDClient

td_client = TDClient(acct_number=<your account number>,
                     oauth_user_id=<the id registered to the TD app you would like to authenticate with>,
                     redirect_uri=<the redirect URI registered to the TD app>,
                     token_path=<optional path to an existing access token>)
td_client.run_auth()
acct_info = td_client.get_positions()
```

## Tests
This package uses poetry, which can be installed by running:
```
curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python 
```
To run the tests, first install the package by cloning the repo and running `poetry install` from the root of the
repository. Then, run `poetry run pytest tests/` from the root directory of this repository.
