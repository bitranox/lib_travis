Version 0.4.3 as of 2020-07-28, see changelog_

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

small utils for travis:
 - print colored banners
 - wrap commands into run/success/error banners, with automatic retry
 - resolve the branch to test, based on the travis environment variables

----

automated tests, Travis Matrix, Documentation, Badges, etc. are managed with `PizzaCutter <https://github
.com/bitranox/PizzaCutter>`_ (cookiecutter on steroids)

Python version required: 3.6.0 or newer

tested on linux "bionic" with python 3.6, 3.7, 3.8, 3.8-dev, pypy3

`100% code coverage <https://codecov.io/gh/bitranox/lib_travis>`_, codestyle checking ,mypy static type checking ,tested under `Linux, macOS, Windows <https://travis-ci.org/bitranox/lib_travis>`_, automatic daily builds and monitoring

----

- `Try it Online`_
- `Usage`_
- `Usage from Commandline`_
- `Installation and Upgrade`_
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

Usage
-----------

usage commandline:


- run a command passed as string

.. code-block:: bash

    # to be used in travis.yml
    # run a command passed as string, wrap it in colored banners, retry 3 times, sleep 30 seconds when retry
    $> lib_travis run "description" "command -some -options" --retry=3 --sleep=30


- run a command passed as a list of arguments

.. code-block:: bash

    # You need to pass '--' after the options for lib_travis run_x command,
    # then all following strings are considered as arguments to run a command,
    # and are not parsed as options for the run_x command itself.
    # that means, all options need to be stated before the '--' marker.
    # commands are splitted again with shlex - in case there are multiple commands in an argument
    $> lib_travis run_x --retry=3 --sleep=30 -- "description" command -some -options

    # in that case "echo test" will be splitted into ['echo', 'test']
    $> EXAMPLE="echo test"
    $> lib_travis run_x --retry=3 --sleep=30 -- ${EXAMPLE}


- get the branch to work on from travis environment variables

.. code-block:: bash

    $> BRANCH=$(lib_travis get_branch)

python methods:

.. code-block:: python

    def get_branch() -> str:
        """
        Return the branch to work on


        Parameter
        ---------
        TRAVIS_BRANCH
            from environment
        TRAVIS_PULL_REQUEST_BRANCH
            from environment
        TRAVIS_TAG
            from environment

        Result
        ---------
        the branch


        Exceptions
        ------------
        none


        ============  =============  ==========================  ==========  =======================================================
        Build         TRAVIS_BRANCH  TRAVIS_PULL_REQUEST_BRANCH  TRAVIS_TAG  Notice
        ============  =============  ==========================  ==========  =======================================================
        Custom Build  <branch>       ---                         ---         return <branch> from TRAVIS_BRANCH
        Push          <branch>       ---                         ---         return <branch> from TRAVIS_BRANCH
        Pull Request  <master>       <branch>                    ---         return <branch> from TRAVIS_PULL_REQUEST_BRANCH
        Tagged        <tag>          ---                         <tag>       return 'master'
        ============  =============  ==========================  ==========  =======================================================

        TRAVIS_BRANCH:
            for push builds, or builds not triggered by a pull request, this is the name of the branch.
            for builds triggered by a pull request this is the name of the branch targeted by the pull request.
            for builds triggered by a tag, this is the same as the name of the tag (TRAVIS_TAG).
            Note that for tags, git does not store the branch from which a commit was tagged. (so we use always master in that case)

        TRAVIS_PULL_REQUEST_BRANCH:
            if the current job is a pull request, the name of the branch from which the PR originated.
            if the current job is a push build, this variable is empty ("").

        TRAVIS_TAG:
            If the current build is for a git tag, this variable is set to the tag’s name, otherwise it is empty ("").


        Examples
        --------

        >>> # Setup
        >>> save_TRAVIS_TAG = os.environ.pop('TRAVIS_TAG', None)
        >>> save_TRAVIS_PULL_REQUEST_BRANCH = os.environ.pop('TRAVIS_PULL_REQUEST_BRANCH', None)
        >>> save_TRAVIS_BRANCH = os.environ.pop('TRAVIS_BRANCH', None)

        >>> # Test Tagged Commit
        >>> os.environ['TRAVIS_TAG'] = 'test_tag'
        >>> assert get_branch() == 'master'
        >>> discard = os.environ.pop('TRAVIS_TAG', None)

        >>> # Test Pull request
        >>> os.environ['TRAVIS_PULL_REQUEST_BRANCH'] = 'test_pr'
        >>> assert get_branch() == 'test_pr'
        >>> discard = os.environ.pop('TRAVIS_PULL_REQUEST_BRANCH', None)

        >>> # Test Push or Custom Build
        >>> os.environ['TRAVIS_BRANCH'] = 'test_branch'
        >>> assert get_branch() == 'test_branch'
        >>> discard = os.environ.pop('TRAVIS_BRANCH', None)

        >>> # Test unknown
        >>> assert get_branch() == 'master'

        >>> # Teardown
        >>> if save_TRAVIS_TAG is not None: os.environ['TRAVIS_BRANCH'] = save_TRAVIS_TAG
        >>> if save_TRAVIS_PULL_REQUEST_BRANCH is not None: os.environ['TRAVIS_PULL_REQUEST_BRANCH'] = save_TRAVIS_PULL_REQUEST_BRANCH
        >>> if save_TRAVIS_BRANCH is not None: os.environ['TRAVIS_BRANCH'] = save_TRAVIS_BRANCH

        """

.. code-block:: python

    def run(description: str, command: str, retry: int = 3, sleep: int = 30, quote: bool = False, banner: bool = True) -> None:
        """
        runs and retries a command passed as string and wrap it in "success" or "error" banners


        Parameter
        ---------
        description
            description of the action, shown in the banner
        command
            the command to launch
        retry
            retry the command n times, default = 3
        sleep
            sleep for n seconds between the commands, default = 30
        quote
            use shlex.quote for automatic quoting of shell commands, default=False
        banner
            if to use banner for run/success or just colored lines.
            Errors will be always shown as banner


        Result
        ---------
        none


        Exceptions
        ------------
        none


        Examples
        ------------


        >>> run('test', "unknown command", sleep=0)
        Traceback (most recent call last):
            ...
        SystemExit: ...

        >>> run('test', "echo test")

        """

.. code-block:: python

    def run_x(description: str, commands: List[str], retry: int = 3, sleep: int = 30, split: bool = True, banner: bool = False) -> None:
        """
        runs and retries a command passed as list of strings and wrap it in "success" or "error" banners


        Parameter
        ---------
        description
            description of the action, shown in the banner
        commands
            the commands to launch
        retry
            retry the command n times, default = 3
        sleep
            sleep for n seconds between the commands, default = 30
        split
            split the commands again with shlex - default = False
            this we need because some commands passed are an array of commands themself
        banner
            if to use banner for run/success or just colored lines.
            Errors will be always shown as banner


        Result
        ---------
        none


        Exceptions
        ------------
        none


        Examples
        ------------


        >>> run_x('test', ['unknown', 'command'], sleep=0)
        Traceback (most recent call last):
            ...
        SystemExit: ...

        >>> run_x('test', ['echo', 'test'])

        >>> run_x('test', ['echo test'])

        """

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
     get_branch             get the branch to work on
     info                   get program informations
     run                    run string command wrapped in run/success/error...
     run_x                  run commands wrapped in run/success/error banners
     upgrade_setup_related  updates pip, setuptools, wheel, pytest-pycodestyle

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

Requirements
------------
following modules will be automatically installed :

.. code-block:: bash

    ## Project Requirements
    click
    cli_exit_tools @ git+https://github.com/bitranox/cli_exit_tools.git
    lib_log_utils @ git+https://github.com/bitranox/lib_log_utils.git
    rst_include @ git+https://github.com/bitranox/rst_include.git

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

0.4.3
-------
2020-07-27: development
    - set default to --no-split on run_x
    - add command upgrade_setup_related

0.4.2
-------
2020-07-27: feature release
    - change colors
    - catch all in run exceptions (OS Error)

0.4.1
-------
2020-07-27: feature release
    - use cli_exit_tools
    - adding banner parameter to "run" commands

0.4.0
-------
2020-07-23: feature release
    - rename commands

0.3.1
-------
2020-07-23: feature release
    - add splitting of commands

0.3.0
-------
2020-07-23: feature release
    - add second run method
    - add automatic quoting for commands passed as string

0.2.1
-------
2020-07-23: patch release
    - flush streams on exit

0.2.0
-------
2020-07-23: feature release
    - change arguments
    - add options for retry and sleep on run command

0.1.3
-------
2020-07-23: patch release
    - correct doctests

0.1.2
-------
2020-07-23: patch release
    - ignore unused options on cli run command
    - added description argument to run command

0.1.1
-------
2020-07-23: initial release
    - setup
    - log utils
    - run wrapper
    - get the branch to work on

