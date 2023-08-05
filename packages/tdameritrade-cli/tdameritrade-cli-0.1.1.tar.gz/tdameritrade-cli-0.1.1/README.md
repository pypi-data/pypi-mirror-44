[![pipeline status](https://gitlab.com/tdameritrade-tools/tdameritrade-cli/badges/master/pipeline.svg)](https://gitlab.com/tdameritrade-tools/tdameritrade-cli/commits/master) [![Documentation Status](https://readthedocs.org/projects/tdameritrade-cli/badge/?version=latest)](https://tdameritrade-cli.readthedocs.io/en/latest/?badge=latest) [![coverage report](https://gitlab.com/tdameritrade-tools/tdameritrade-cli/badges/master/coverage.svg)](https://gitlab.com/tdameritrade-tools/tdameritrade-cli/commits/master)




# TDAmeritrade CLI
A CLI that makes requests of TDA using the TDA API via the TDA client. 

Read the [docs](https://tdameritrade-cli.readthedocs.io/en/latest/?#).

## Installation:
Run `pip install tdameritrade-cli` from a virtual environment. I also suggest you add the
package's cli to your path. To do this, navigate to your virtual environment's `bin` folder
(which can be found by running `which python` from within an activated virtual environment),
and create a symbolic link.

E.g., `ln -s <PATH TO VENV BIN>/tda-cli ~/.local/bin/tda-cli`

Now you can run the tool (in a new shell) with `tda-cli`.

See `tda-cli --help` for functionality.