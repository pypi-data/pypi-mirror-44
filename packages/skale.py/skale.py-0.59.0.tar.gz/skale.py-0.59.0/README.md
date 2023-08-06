# skale.py

SKALE client tools.  
Python implementation used in skale-node and other SKALE network components.

### Installation

```bash
pip install skale
```

### Usage

Library initialization

```python
from skale import Skale, BlockchainEnv
skale = Skale(BlockchainEnv.DO)
```

Interactions with SKALE contracts

```python
active_nodes = skale.nodes_data.get_active_node_ips()
schains = skale.schains_data.get_schains_for_owner('0x...')
```


### Development

##### Install local version (with hot reload)

```
virtualenv venv
. venv/bin/activate 
pip install -e .[dev]
```

#### Build and publish library

```bash
bash build_and_publish.sh major/minor/patch
```

#### If you're using .env file

```bash
 export $(cat .env | xargs) && bash build_and_publish.sh major/minor/patch
``` 

##### Format your code before commit

Show flake8 errors on file change:

```sh
# Test flake8
WHEN_CHANGED_EVENT=file_modified when-changed -v -s -r -1 skale/ tests/ examples/ -c "clear; flake8 web3 tests ens && echo 'flake8 success' || echo 'error'"
```

Install `when-changed`:
```bash
 pip install https://github.com/joh/when-changed/archive/master.zip
```

#### Versioning

The version scheme for this repo is `{major}.{minor}.{patch}`
For more details see: https://semver.org/

#### Testing

For running full test suite you will need `skale-manager` repo cloned alongside with `skale-py` directory

Running full test suite:

```bash
bash test_runner.sh
```

Running test suite manually:

See `tests/README.md`