# Squidward

After working with gaussian processes (GPs) to build out robust reinforcement learning models in production for most of my early career as a machine learning engineer (MLE), I became frustrated with the packages available for building GPs. They often focus using the latest in optimization tools and are far from the elegant, efficient, and simple design that I believe a GP package should embody.

This is my attempt to create the product that I would want to use. Something simple and flexible that gives knowledgable data scientists the tools they need to do the research or production machine learning work that they need.

I'm open to all feedback, commentary, and suggestions as long as they are constructive and polite.

### Authors

**James Montgomery** - *Initial work* - [jamesmontgomery.us](http://jamesmontgomery.us)

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing

This is a step by step guide to installing squidward for your local environment.

I recommend installing squidward in a virtual environment for organized dependency control. Personally, I prefer conda environments. First, let's create and open our environment.

```
conda create --name squidward_env python=3.6
source activate squidward_env
```

MKL backend for numpy can help increase performance of this code. Anaconda now comes with mkl by default. To make use of mkl simply set up your virtual environment with anaconda like below.

```
conda create --name squidward_env python=3.6 anaconda
source activate squidward_env
```

To install the latest stable version, simply [pip install from pypi](https://pypi.org/project/squidward/)!

```
pip install squidward
```

However, if you want the latest version git clone this repository to your local environment instead.

```
git clone https://github.com/looyclark/squidward.git
```

Change directory (cd) into the root of the squidward repository. Updates staged for the next stable release will be in the `master` branch and experimental updates will be in the `dev_branch` branch of this repo.

```
cd ./squidward
```

Install squidward using pip from the setup file.

```
pip install .
```

### Basic Examples

I've included basic examples of how to use squidward to get new users started building gaussian process models with this package.

* [Simple Regression](https://github.com/looyclark/squidward/blob/master/docs/examples/Simple_Regression.ipynb)
* [Simple Classification](https://github.com/looyclark/squidward/blob/master/docs/examples/Simple_Classification.ipynb)

## Testing

Testing is an important part of creating maintainable, production grade code.

### Running the unit tests

To run the unit tests cd to `squidward/squidward` so that `/tests` is a subdirectory.

```
cd ./squidward/tests
```

Use `nosetests` to run all unit tests for squidward. If you installed squidward in a virtual environment, please run the tests in that same environment.

```
source activate squidward_env
nosetests
```

You can also run the tests with coverage to see what code within the package is called in the tests.

```
nosetests --with-coverage --cover-package=squidward
```

### Running the style tests

I attempt to adhere to the [pep8](https://www.python.org/dev/peps/pep-0008/) style guide for the squidward project. To run the style tests cd to the root directory of the repository `squidward/` so that `/squidward` is a subdirectory. Use `pylint squidward` to run all style tests for squidward.

```
cd ./squidward
pylint squidward
```

Some of the naming conventions I've chosen intentionally do not adhere to pep8 in order to better resemble mathematical conventions. For example, I often borrow the matrix naming conventions of Rassmussen such as `K` and `K_ss`. You can run `pylint --disable=invalid-name` if you would like to ignore the resulting pylint warnings.

```
pylint squidward --disable=invalid-name --ignore=gp_viz
```

## Acknowledgments

* A big thanks to Keegan Hines and Josh Touyz who introduced me to Gaussian Processes
* Many of the methods/implementations in this package are based off of [Gaussian Processes for Machine Learning](http://www.gaussianprocess.org/gpml/) chapters 2 and 3.
* Many of the native kernels supported by squidward are largely drawn from the [kernel cookbook](https://www.cs.toronto.edu/~duvenaud/cookbook/) by David Duvenaud.

## Alternative Gaussian Process Packages

This is hardly the only gaussian process package out there. Here are a few alternatives in case you dislike this package.

* [GPyTorch](https://gpytorch.ai/)
* [GPy](https://gpy.readthedocs.io/en/deploy/)
* [GPFlow](https://gpflow.readthedocs.io/en/develop/)
* [Sklearn](https://scikit-learn.org/stable/modules/gaussian_process.html)
* [George](https://george.readthedocs.io/en/latest/tutorials/first/)
* [Pymc3](https://docs.pymc.io/api/gp.html)
* [Stan](https://betanalpha.github.io/assets/case_studies/gp_part1/part1.html)
