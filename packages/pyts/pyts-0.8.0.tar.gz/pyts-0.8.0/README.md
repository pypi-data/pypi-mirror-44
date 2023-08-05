[![Build Status](https://travis-ci.org/johannfaouzi/pyts.svg?branch=master)](https://travis-ci.org/johannfaouzi/pyts)
[![Build Status](https://img.shields.io/appveyor/ci/johannfaouzi/pyts/master.svg)](https://ci.appveyor.com/project/johannfaouzi/pyts)
[![Build Status](https://circleci.com/gh/johannfaouzi/pyts/tree/master.svg?style=shield)](https://circleci.com/gh/johannfaouzi/pyts)
[![Documentation Status](https://readthedocs.org/projects/pyts/badge/?version=latest)](https://pyts.readthedocs.io/en/latest/?badge=latest)
[![Codecov](https://codecov.io/gh/johannfaouzi/pyts/branch/master/graph/badge.svg)](https://codecov.io/gh/johannfaouzi/pyts)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyts.svg)](https://img.shields.io/pypi/pyversions/pyts.svg)
[![PyPI version](https://badge.fury.io/py/pyts.svg)](https://badge.fury.io/py/pyts)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1244152.svg)](https://doi.org/10.5281/zenodo.1244152)

## pyts: a Python package for time series transformation and classification

pyts is a Python package for time series transformation and classification. It
aims to make time series classification easily accessible by providing
preprocessing and utility tools, and implementations of
state-of-the-art algorithms. Most of these algorithms transform time series,
thus pyts provides several tools to perform these transformations.


### Installation

#### Dependencies

pyts requires:

- Python (>= 3.5)
- NumPy (>= 1.15.4)
- SciPy (>= 1.1.0)
- Scikit-Learn (>=0.20.1)
- Numba (>0.41.0)

To run the examples Matplotlib (>=2.0.0) is required.


#### User installation

If you already have a working installation of numpy, scipy, scikit-learn and
numba, you can easily install pyts using ``pip``

    pip install pyts

You can also get the latest version of pyts by cloning the repository

    git clone https://github.com/johannfaouzi/pyts.git
    cd pyts
    pip install .


#### Testing

After installation, you can launch the test suite from outside the source
directory using pytest:

    pytest pyts


### Changelog

See the [changelog](https://pyts.readthedocs.io/en/latest/changelog.html)
for a history of notable changes to pyts.

### Development

The development of this package is in line with the one of the scikit-learn
community. Therefore, you can refer to their
[Development Guide](https://scikit-learn.org/stable/developers/). A slight
difference is the use of Numba instead of Cython for optimization.

### Documentation

The section below gives some information about the implemented algorithms in pyts.
For more information, please have a look at the
[HTML documentation available via ReadTheDocs](https://pyts.readthedocs.io/en/latest/)

### Implemented features

pyts consists of the following modules:

- `approximation`: This module provides implementations of algorithms that
approximate time series. Implemented algorithms are
[Piecewise Aggregate Approximation](https://pyts.readthedocs.io/en/latest/generated/pyts.approximation.PiecewiseAggregateApproximation.html#),
[Symbolic Aggregate approXimation](https://pyts.readthedocs.io/en/latest/generated/pyts.approximation.SymbolicAggregateApproximation.html#),
[Discrete Fourier Transform](https://pyts.readthedocs.io/en/latest/generated/pyts.approximation.DiscreteFourierTransform.html#),
[Multiple Coefficient Binning](https://pyts.readthedocs.io/en/latest/generated/pyts.approximation.MultipleCoefficientBinning.html#) and
[Symbolic Fourier Approximation](https://pyts.readthedocs.io/en/latest/generated/pyts.approximation.SymbolicFourierApproximation.html#).

- `bag_of_words`: This module consists of a class
[BagOfWords](https://pyts.readthedocs.io/en/latest/generated/pyts.bag_of_words.BagOfWords.html#)
that transforms time series into bags of words. This approach is quite common
in time series classification.

- `classification`: This module provides implementations of algorithms that
can classify time series. Implemented algorithms are
[KNeighborsClassifier](https://pyts.readthedocs.io/en/latest/generated/pyts.classification.KNeighborsClassifier.html#),
[SAXVSM](https://pyts.readthedocs.io/en/latest/generated/pyts.classification.SAXVSM.html#) and
[BOSSVS](https://pyts.readthedocs.io/en/latest/generated/pyts.classification.BOSSVS.html#).

- `decomposition`: This module provides implementations of algorithms that
decompose a time series into several time series. The only implemented algorithm
is
[Singular Spectrum Analysis](https://pyts.readthedocs.io/en/latest/generated/pyts.decomposition.SingularSpectrumAnalysis.html#).

- `image`: This module provides implementations of algorithms that transform
time series into images. Implemented algorithms are
[Recurrence Plot](https://pyts.readthedocs.io/en/latest/generated/pyts.image.RecurrencePlot.html#),
[Gramian Angular Field](https://pyts.readthedocs.io/en/latest/generated/pyts.image.GramianAngularField.html#) and
[Markov Transition Field](https://pyts.readthedocs.io/en/latest/generated/pyts.image.MarkovTransitionField.html#).

- `metrics`: This module provides implementations of metrics that are specific
to time series. Implemented metrics are
[Dynamic Time Warping](https://pyts.readthedocs.io/en/latest/generated/pyts.metrics.dtw.html#)
with several variants and the
[BOSS](https://pyts.readthedocs.io/en/latest/generated/pyts.metrics.boss.html#)
metric.

- `preprocessing`: This module provides most of the scikit-learn preprocessing
tools but applied sample-wise (i.e. to each time series independently) instead
of feature-wise, as well as an
[imputer](https://pyts.readthedocs.io/en/latest/generated/pyts.preprocessing.InterpolationImputer.html#)
of missing values using interpolation. More information is available at the
[pyts.preprocessing API documentation](https://pyts.readthedocs.io/en/latest/api.html#module-pyts.preprocessing)

- `transformation`: This module provides implementations of algorithms that
transform a data set of time series with shape `(n_samples, n_timestamps)` into
a data set with shape `(n_samples, n_features)`. Implemented algorithms are
[BOSS](https://pyts.readthedocs.io/en/latest/generated/pyts.transformation.BOSS.html#) and
[WEASEL](https://pyts.readthedocs.io/en/latest/generated/pyts.transformation.WEASEL.html#).

- `utils`: a simple module with
[utility functions](https://pyts.readthedocs.io/en/latest/api.html#module-pyts.utils).
