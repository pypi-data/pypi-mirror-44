# IBM Bluepages Python SDK

## Installation

To install, use `pip`:

```bash
pip install --upgrade ibmBluepages
```

## Usage

```python
from ibmBluepages import ibmBluepages

ibmBluepages = ibmBluepages()
personInfo = ibmBluepages.getPersonInfoByIntranetID("intrenetID")
print(personInfo)
```

## Python Version

Tested on: Python from 3.5.

## License

This library is licensed under the [Apache 2.0 license][license].



[license]: http://www.apache.org/licenses/LICENSE-2.0
