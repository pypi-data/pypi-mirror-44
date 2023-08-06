# libpagure

A Python library for Pagure APIs. Pagure is a light-weight git-centered forge based on pygit2, created by Pierre-Yves Chibon.


## User Guide

A more detail user guide is available [here](https://docs.pagure.org/libpagure/)

## Usage
---
* Import and Initialization:
```
>>> from libpagure import Pagure
>>> pg = Pagure()
```

* Get the API version
```
>>> pg.api_version()
'0.8'
```

* Create a new Project
```
>>> from libpagure import Pagure
>>> pg = Pagure(pagure_token="foobar")
>>> pg.new_project(name="foo", description="bar", url="http://foobar.io",
                   create_readme=True)
>>> Project "foo" created
```

This library is a Python wrapper of Pagure web APIs.
You can refer to [Pagure API](https://pagure.io/api/0/) reference.


## Contribution

Thank you for taking the time to contribute. This project relies on an active and involved community, and we really appreciate your support.

### Quickstart

    1. Look for an existing issue about the bug or feature you're interested in. If you can't find an existing issue, create a new one.

    2. Fork the repository.

    3. Fix the bug or add the feature, and then write one or more tests which show the bug is fixed or the feature works.

    4. Submit a pull request and wait for a maintainer to review it.

More detailed guidelines to help ensure your submission goes smoothly are below.

### Guidelines

#### Code Style

We follow the [PEP8](https://www.python.org/dev/peps/pep-0008/) style guide for Python. This is automatically enforced by the CI suite.

We are using [Black](https://github.com/ambv/black) to automatically format the source code. It is also checked in CI. The Black webpage contains instructions to configure your editor to run it on the files you edit.

Note : The max line length is configured to be 100.

#### Tests

The test suites can be run using [tox](http://tox.readthedocs.io/) by simply
running ``tox`` from the repository root. We aim for all code to have test coverage or
be explicitly marked as not covered using the ``# no-qa`` comment. We encourage the [Test
Driven Development Practice](http://www.extremeprogramming.org/rules/testfirst.html)

If you're not certain how to write tests, we will be happy to help you.

## Development

### Container Development environment

To build the development environment we provide a Dockerfile. You can build the container as follow:

    $ cd devel
    $ docker build -t libpagure_dev .
    $ cd ..

Once the container is built you can run the tests using the following command for Python 3.6

    $ docker run -it --rm -v `pwd`:/code:z libpagure_dev py.test-3.6 --cov libpagure

and for Python 2.7.

    $ docker run -it --rm -v `pwd`:/code:z libpagure_dev py.test-2.7 --cov libpagure

You can also run an interactive shell inside the container using:

    $ docker run -it --rm -v `pwd`:/code:z libpagure_dev

In each case `pwd` command needs to return the root path of libpagure repository. (ie where this readme is)

## Running the unit tests outside the container environment

First you need to create a virtual environment and install the dependencies needed ::

    $ python3 -m venv .venv
    $ source .venv/bin/activate
    (.venv) $ pip install -r test-requirements.txt

Then you can execute the test suite using the following command ::

    $ tox

