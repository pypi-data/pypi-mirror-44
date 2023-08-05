# Spines

**Backbones for parameterized models.**

[![PyPI Version](https://img.shields.io/badge/pypi-v0.0.2-blue.svg)](https://pypi.org/project/spines/)
[![Documentation Status](https://readthedocs.org/projects/spines/badge/?version=latest)](https://spines.readthedocs.io/en/latest/?badge=latest)

![Spines Logo](https://github.com/douglasdaly/spines/blob/master/docs/_static/images/spines_logo_256.png "Spines Logo")


## About

Spines was built to provide a skeleton for Model classes: a common interface 
for users to build models around (with some tools and utilities which take
advantage of having the commonalities).  It's similar, in structure, to some
of scikit-learn's underlying Estimator classes - but with a unified set of
functions for all models, namely:

- Build
- Fit
- Transform

The transform method is the only one that's required, though the other two are 
likely useful most of the time.  Spines is **absolutely not** a replacement for 
scikit-learn (or any other data/machine-learning library) it's simply a useful 
framework for building your own models (leveraging *any* library) in a 
standardized and convenient way.


## Documentation

The latest documentation is hosted at [https://spines.reathedocs.io/](https://spines.readthedocs.io/ "Spines ReadTheDocs").


## Installing

To install spines use your package manager of choice, an example using `pipenv`
would be:

```bash
$ pipenv install spines
```


## License

This project is licensed under the MIT License, for more information see the 
[LICENSE](./LICENSE) file.
