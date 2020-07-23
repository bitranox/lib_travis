Version 0.1.1a as of 2020-07-23, see changelog_

=======================================================

lib_travis
==========

|travis_build| |license| |jupyter| |pypi|

|codecov| |better_code| |cc_maintain| |cc_issues| |cc_coverage| |snyk|


.. |travis_build| image:: https://img.shields.io/travis/bitranox/lib_travis/master.svg
   :target: https://travis-ci.org/bitranox/lib_travis

.. |license| image:: https://img.shields.io/github/license/webcomics/pywine.svg
   :target: http://en.wikipedia.org/wiki/MIT_License

.. |jupyter| image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/bitranox/lib_travis/master?filepath=lib_travis.ipynb

.. for the pypi status link note the dashes, not the underscore !
.. |pypi| image:: https://img.shields.io/pypi/status/lib-travis?label=PyPI%20Package
   :target: https://badge.fury.io/py/lib_travis

.. |codecov| image:: https://img.shields.io/codecov/c/github/bitranox/lib_travis
   :target: https://codecov.io/gh/bitranox/lib_travis

.. |better_code| image:: https://bettercodehub.com/edge/badge/bitranox/lib_travis?branch=master
   :target: https://bettercodehub.com/results/bitranox/lib_travis

.. |cc_maintain| image:: https://img.shields.io/codeclimate/maintainability-percentage/bitranox/lib_travis?label=CC%20maintainability
   :target: https://codeclimate.com/github/bitranox/lib_travis/maintainability
   :alt: Maintainability

.. |cc_issues| image:: https://img.shields.io/codeclimate/issues/bitranox/lib_travis?label=CC%20issues
   :target: https://codeclimate.com/github/bitranox/lib_travis/maintainability
   :alt: Maintainability

.. |cc_coverage| image:: https://img.shields.io/codeclimate/coverage/bitranox/lib_travis?label=CC%20coverage
   :target: https://codeclimate.com/github/bitranox/lib_travis/test_coverage
   :alt: Code Coverage

.. |snyk| image:: https://img.shields.io/snyk/vulnerabilities/github/bitranox/lib_travis
   :target: https://snyk.io/test/github/bitranox/lib_travis

put your description of the project under .docs/description.rst

----

automated tests, Travis Matrix, Documentation, Badges, etc. are managed with `PizzaCutter <https://github
.com/bitranox/PizzaCutter>`_ (cookiecutter on steroids)

Python version required: 3.6.0 or newer

tested on linux "bionic" with python 3.6, 3.7, 3.8, 3.8-dev, pypy3

`100% code coverage <https://codecov.io/gh/bitranox/lib_travis>`_, codestyle checking ,mypy static type checking ,tested under `Linux, macOS, Windows <https://travis-ci.org/bitranox/lib_travis>`_, automatic daily builds and monitoring

----

- `Try it Online`_
- `Installation and Upgrade`_
- `Usage`_
- `Usage from Commandline`_
- `Requirements`_
- `Acknowledgements`_
- `Contribute`_
- `Report Issues <https://github.com/bitranox/lib_travis/blob/master/ISSUE_TEMPLATE.md>`_
- `Pull Request <https://github.com/bitranox/lib_travis/blob/master/PULL_REQUEST_TEMPLATE.md>`_
- `Code of Conduct <https://github.com/bitranox/lib_travis/blob/master/CODE_OF_CONDUCT.md>`_
- `License`_
- `Changelog`_

----

Try it Online
-------------

You might try it right away in Jupyter Notebook by using the "launch binder" badge, or click `here <https://mybinder.org/v2/gh/{{rst_include.
repository_slug}}/master?filepath=lib_travis.ipynb>`_

Installation and Upgrade
------------------------

- Before You start, its highly recommended to update pip and setup tools:


.. code-block:: bash

    python -m pip --upgrade pip
    python -m pip --upgrade setuptools
    python -m pip --upgrade wheel

- to install the latest release from PyPi via pip (recommended):

.. code-block:: bash

    # install latest release from PyPi
    python -m pip install --upgrade lib_travis

    # test latest release from PyPi without installing (can be skipped)
    python -m pip install lib_travis --install-option test

- to install the latest development version from github via pip:


.. code-block:: bash

    # normal install
    python -m pip install --upgrade git+https://github.com/bitranox/lib_travis.git

    # to test without installing (can be skipped)
    python -m pip install git+https://github.com/bitranox/lib_travis.git --install-option test

    # to install and upgrade all dependencies regardless of version number
    python -m pip install --upgrade git+https://github.com/bitranox/lib_travis.git --upgrade-strategy eager


- include it into Your requirements.txt:

.. code-block:: bash

    # Insert following line in Your requirements.txt:
    # for the latest Release on pypi:
    lib_travis

    # for the latest development version :
    lib_travis @ git+https://github.com/bitranox/lib_travis.git

    # to install and upgrade all modules mentioned in requirements.txt:
    python -m pip install --upgrade -r /<path>/requirements.txt



- to install the latest development version from source code:

.. code-block:: bash

    # cd ~
    $ git clone https://github.com/bitranox/lib_travis.git
    $ cd lib_travis

    # to test without installing (can be skipped)
    python setup.py test

    # normal install
    python setup.py install

- via makefile:
  makefiles are a very convenient way to install. Here we can do much more,
  like installing virtual environments, clean caches and so on.

.. code-block:: shell

    # from Your shell's homedirectory:
    $ git clone https://github.com/bitranox/lib_travis.git
    $ cd lib_travis

    # to run the tests:
    $ make test

    # to install the package
    $ make install

    # to clean the package
    $ make clean

    # uninstall the package
    $ make uninstall

Usage
-----------

.. code-block::

    import the module and check the code - its easy and documented there, including doctest examples.
    in case of any questions the usage section might be expanded at a later time

Usage from Commandline
------------------------

.. code-block:: bash

   Usage: lib_travis [OPTIONS] COMMAND [ARGS]...

     travis related utilities

   Options:
     --version                     Show the version and exit.
     --traceback / --no-traceback  return traceback information on cli
     -h, --help                    Show this message and exit.

   Commands:
     info  get program informations

Requirements
------------
following modules will be automatically installed :

.. code-block:: bash

    ## Project Requirements
    click

Acknowledgements
----------------

- special thanks to "uncle bob" Robert C. Martin, especially for his books on "clean code" and "clean architecture"

Contribute
----------

I would love for you to fork and send me pull request for this project.
- `please Contribute <https://github.com/bitranox/lib_travis/blob/master/CONTRIBUTING.md>`_

License
-------

This software is licensed under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_

---

Changelog
=========

- new MAJOR version for incompatible API changes,
- new MINOR version for added functionality in a backwards compatible manner
- new PATCH version for backwards compatible bug fixes

0.1.1a
-------
2020-07-23: initial release
    - setup

