[![Build Status](https://travis-ci.org/kmedian/jupytertweak.svg?branch=master)](https://travis-ci.org/kmedian/jupytertweak)
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/kmedian/jupytertweak/master?urlpath=lab)

# jupytertweak


## Table of Contents
* [Installation](#installation)
* [Usage](#usage)
* [Commands](#commands)
* [Support](#support)
* [Contributing](#contributing)


## Installation
The `jupytertweak` [git repo](http://github.com/kmedian/jupytertweak) is available as [PyPi package](https://pypi.org/project/jupytertweak)

```
pip install jupytertweak
```


## Usage
Check the [examples](http://github.com/kmedian/jupytertweak/examples) folder for notebooks.


## Commands
* Check syntax: `flake8 --ignore=F401`
* Remove `.pyc` files: `find . -type f -name "*.pyc" | xargs rm`
* Remove `__pycache__` folders: `find . -type d -name "__pycache__" | xargs rm -rf`
* Upload to PyPi: `python setup.py sdist upload -r pypi`
* Upload to PyPi with twine: `python setup.py sdist && twine upload -r pypi dist/*`


## Support
Please [open an issue](https://github.com/kmedian/jupytertweak/issues/new) for support.


## Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/kmedian/jupytertweak/compare/).
