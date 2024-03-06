## uas_utils package
This package contains the uas to bufr conversion tools that are distributed as part of this repo, but also utilized by
[WMO UASDC Data pipeline](https://github.com/synoptic/uasdc-pipeline/tree/main). In order to avoid code duplication, the 
uas_utils package is used as a dependency in the uasdc-pipeline.

### Installation
To install the uas_utils package, you can use the following command:
```bash
pip install git+ssh://git@github.com/synoptic/wmo-uasdc.git@package-it#egg=wmo-uasdc
```
For development work, you can install the package in editable mode:
```bash
pip install -e git+ssh://github.com/synoptic/wmo-uasdc.git@package-it#egg=wmo-uasdc -I
```

### Usage
Once the package is installed, you can use the uas_utils package in your code as follows:
```python
from uas_utils import uas2bufr
```
The `uas2bufr` module contains the functions to convert UAS data to BUFR format.
