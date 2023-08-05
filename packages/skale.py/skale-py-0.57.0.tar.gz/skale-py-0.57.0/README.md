# skale-py

Skale client tools.  
Python implementation which is used in the skale-node and other components.


### Development

##### Format your code before commit

```bash
cd skale
yapf -ir .
```



##### Install local version (with hot reload)

```
pip install -e .
```

### Build and publish library

```bash
bash build_and_publish.sh major/minor/patch
```

#### If you're using .env file

```bash
 export $(cat .env | xargs) && bash build_and_publish.sh major/minor/patch
``` 

### Versioning

The version format for this repo is `{major}.{minor}.{patch}` for stable, and `{major}.{minor}.{patch}-{stage}.{devnum}` for unstable (stage can be `alpha` or `beta`).

For more details see: https://semver.org/


##### Fix for scrypt error
https://github.com/ethereum/web3.py/issues/751