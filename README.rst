Version 1.0.2 as of 2020-07-29, see changelog_

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

`100% code coverage <https://codecov.io/gh/bitranox/lib_travis>`_, codestyle checking ,mypy static type checking ,tested under `Linux, macOS <https://travis-ci.org/bitranox/lib_travis>`_, automatic daily builds and monitoring

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

.. code-block:: text

   Usage: lib_travis [OPTIONS] COMMAND [ARGS]...

     travis related utilities

   Options:
     --version                     Show the version and exit.
     --traceback / --no-traceback  return traceback information on cli
     -h, --help                    Show this message and exit.

   Commands:
     install
        updates pip, setuptools, wheel, pytest-pycodestyle
        --dry-run

     script
        updates pip, setuptools, wheel, pytest-pycodestyle
        --dry-run

     after_success
        coverage reports
        --dry-run

     deploy
        deploy on pypi
        --dry-run

     get_branch
        get the branch to work on

     info
        get program informations

     run [Options] <description> <command>
        run string command wrapped in run/success/error banners
        -r --retry              retry n times, default = 3
        -s --sleep              sleep when retry, default = 30 seconds
        --quote --plain         use shlex auto quote, default = False
        --banner --no-banner    wrap in banners, default = True

     run_x [Options] -- <description> <command1> <command2> ...
        run commands wrapped in run/success/error banners
        -r --retry              retry n times, default = 3
        -s --sleep              sleep when retry, default = 30 seconds
        --split --no-split      if to split arguments with shlex, default = False
        --banner --no-banner    wrap in banners, default = True



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
    # commands can be splitted again with shlex - in case there are multiple commands in an argument
    $> lib_travis run_x --retry=3 --sleep=30 -- "description" command -some -options

    # in that case "echo test" will be splitted into ['echo', 'test']
    $> EXAMPLE="echo test"
    $> lib_travis run_x --retry=3 --sleep=30 --split -- ${EXAMPLE}


- get the branch to work on from travis environment variables

.. code-block:: bash

    $> BRANCH=$(lib_travis get_branch)

python methods:

- install, jobs to do in the Travis "install" section

.. code-block:: python

    def install(dry_run: bool = True) -> None:
        """
        upgrades pip, setuptools, wheel and pytest-pycodestyle


        Parameter
        ---------
        cPIP
            from environment, the command to launch pip, like "python -m pip"


        Examples
        --------
        >>> install()

        """

- script, jobs to do in the Travis "script" section

.. code-block:: python

    def script(dry_run: bool = True) -> None:
        """
        travis jobs to run in travis.yml section "script":
        - run setup.py test
        - run pip with install option test
        - run pip standard install
        - test the CLI Registration
        - install the test requirements
        - install codecov
        - install pytest-codecov
        - run pytest coverage
        - run mypy strict
            - if MYPY_STRICT="True"
        - rebuild the rst files (resolve rst file includes)
            - needs RST_INCLUDE_SOURCE, RST_INCLUDE_TARGET set and BUILD_DOCS="True"
        - check if deployment would succeed
            - needs CHECK_DEPLOYMENT="True", setup.py exists and not a tagged build)


        Parameter
        ---------
        cPREFIX
            from environment, the command prefix like 'wine' or ''
        cPIP
            from environment, the command to launch pip, like "python -m pip"
        cPYTHON
            from environment, the command to launch python, like 'python' or 'python3' on MacOS
        CLI_COMMAND
            from environment, must be set in travis - the CLI command to test with option --version
        MYPY_STRICT
            from environment, if pytest with mypy --strict should run
        BUILD_DOCS
            from environment, if rst file should be rebuilt
        RST_INCLUDE_SOURCE
            from environment, the rst template with rst includes to resolve
        RST_INCLUDE_TARGET
            from environment, the rst target file
        DEPLOY_CHECK
            from environment, if deployment to pypi should be tested
            only if setup.py exists and on non-tagged builds (there we deploy for real)
        dry_run
            if set, this returns immediately - for CLI tests


        Examples
        --------
        >>> script()

        """

- after_success, jobs to do in the Travis "after_success" section

.. code-block:: python

    def after_success(dry_run: bool = True) -> None:
        """
        travis jobs to run in travis.yml section "after_success":
            - coverage report
            - codecov
            - codeclimate report upload


        Parameter
        ---------
        cPREFIX
            from environment, the command prefix like 'wine' or ''
        cPIP
            from environment, the command to launch pip, like "python -m pip"
        CC_TEST_REPORTER_ID
            from environment, must be set in travis
        TRAVIS_TEST_RESULT
            from environment, this is set by TRAVIS automatically
        dry_run
            if set, this returns immediately - for CLI tests


        Examples
        --------
        >>> after_success()

        """

- deploy, deploy to pypi in the Travis "after_success" section

.. code-block:: python

    def deploy(dry_run: bool = True) -> None:
        """
            travis jobs to run in travis.yml section "script":
        - run setup.py test
        - run pip with install option test
        - run pip standard install
        - test the CLI Registration
        - install the test requirements
        - install codecov
        - install pytest-codecov
        - run pytest coverage
        - run mypy strict
            - if MYPY_STRICT="True"
        - rebuild the rst files (resolve rst file includes)
            - needs RST_INCLUDE_SOURCE, RST_INCLUDE_TARGET set and BUILD_DOCS="True"
        - check if deployment would succeed
            - needs CHECK_DEPLOYMENT="True", setup.py exists and not a tagged build)


        Parameter
        ---------
        cPREFIX
            from environment, the command prefix like 'wine' or ''
        cPIP
            from environment, the command to launch pip, like "python -m pip"
        cPYTHON
            from environment, the command to launch python, like 'python' or 'python3' on MacOS
        PYPI_PASSWORD
            from environment, passed as secure, encrypted variable to environment
        DEPLOY
            from environment, needs to be "True"
        dry_run
            if set, this returns immediately - for CLI tests


        Examples
        --------
        >>> deploy()

        """

- get_branch, determine the branch to work on from Travis environment

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

- run, usually used internally

.. code-block:: python

    def run(description: str, command: str, retry: int = 3, sleep: int = 30, quote: bool = False, banner: bool = True, show_command: bool = True) -> None:
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
        show_command
            if the command is shown - take care not to reveal secrets here !


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

- run_x, usually used internally

.. code-block:: python

    def run_x(description: str, commands: List[str], retry: int = 3, sleep: int = 30, split: bool = True, banner: bool = False, show_command: bool = True) -> None:
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
        show_command
            if the command is shown - take care not to reveal secrets here !


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

- travis.py example

.. code-block:: yaml

    language: python
    group: travis_latest
    dist: bionic
    sudo: true

    env:
        global:
            - cPREFIX=""				# prefix before commands - used for wine, there the prefix is "wine"
            - cPYTHON="python"			# command to launch python interpreter (its different on macOs, there we need python3)
            - cPIP="python -m pip"   	# command to launch pip (its different on macOs, there we need pip3)
            - WINEDEBUG=fixme-all       # switch off wine fix me messages
            - secure: "PmyawDvf+hN5ACdHD0n3RjwfYmrh801cfcRGy9tyXvjnUWyrpseCQc1/Is3SX4Ju29zcWFS6P34uolGJ/4vPfrWS2vpIVXJuHa3tYPuQe0wKq1Ke9MmohjeM/4IRYWzyIQozjo1fy3RAk4hMzMK9mf9WDIcGNbi2jrxALJwG0HKeHberF+irjxfnV5/n/pz9mO9QPc+qc0b2cdFakNsth51XoxGkT1YdGbI6wjtPcsRX4JAKCF4K/gIAfXrAadNV+j9ttqQlq3qk5CrRKK5NyjnxMJwenCYd+GzEK7oFWwKOdJfoGQFpjZ0pV7bw8Xs6w0neZKq973GRvBvPhFBprF13dGeg1EOPlggzi9EAhLTgvCyfQGWkEEVCry8luNP56VSAzBGbMahN1KLZ/9FN1ZdZFF87E8Vg/jWiCHR7IM6DaETY5283NSnhB29rBmogoCxsC9l8FCY+OhYwnpKUl13LBi+XeqBry+hn5Y+sVGhYxwJsd8eY7+zjodVedtHCqO8mfOR6xAGh/stRAojOmP1o1DcB7CvmUDIO8vhDkrhwa5dUWZwOg6AeABmLlHn8KtyePqQ65RzkDYqoiphCG8EeVZWzEsuht8YORIi3ea4ZfcTDyKX9zxE6VI/wIBJeUPy0Pwbzb2m7k1DoMeecSaMHjHBrHWMErhbswwb1TTw="  # CC_TEST_REPORTER_ID.secret
            - secure: "MrMbBlF5fVSWXV7KkvcC52S7Pm2jTkJlMTYzIXJux9wGHulA6ujYfs5doNVcuejRIOe0+91ruH8ENLOw1mITmli/bfHz5gLgUCQONjMxbhr3KI1E8xzUasRroQ8rSHKeFeXStRJglRwQJ+eqNsaX25F9YdwqR89v6lYjk+g4R8BkyoJROwkfPs4p3PRO+826q//nELtWUUQOUvRxqLWEC99JMOUEssHelAjaedf9eKKfGf9t2yoANIOYMQxdAbSn3HxYr7CBf0+53Z5bkAxRKq1cAsrISa4VDHyJAabfycvCBW8EBjdvvbS/20octdKxnqf4NUd97B2PDEzXSgZ4IRB8LtTda9xgdhUUx+e23mWNdpsXwpIM13A0ql5e2pWvnjxfMSNNctc5GN/+0DM+a9RWsmfYxQa8P9iZKtsCl4uiYzjHALVXakAcoaTamx0eH+g0JIAgUvhNXwL10w+24mqioleDNYQuuWRibgWTN0qKlt2+7VXd+J03TmIA7mPamNlil1oOyLPM03qgXXWbpZ2hjlHeEIcw6qSPqIUXPXXVoRnxvbRZWWDFji7H2sVd2fpUWe9lUMyu+fHj5i1PeOEoXrLcRi0BnOLzZWHl/GM6h0eh/0SwjgoY/SzUOAYtd3YhHsLNSMp4wIclHtcFkmi0pOoZ2ARtTvV0kRK0vJ8="  # pypi_password.secret


    addons:
        apt:
            packages:
                - xvfb      # install xvfb virtual framebuffer - this we need for WINE
                - winbind   # needed for WINE

    services:   			# start services
      - xvfb    			# is needed for WINE on headless installation


    matrix:
        include:


        - os: linux
          language: python
          python: "3.6"
          before_install:
              - export mypy_strict_typecheck="True"
              - export build_docs="False"
              - export deploy_on_pypi="False"


        - os: linux
          language: python
          python: "3.7"
          before_install:
              - export mypy_strict_typecheck="True"
              - export build_docs="False"
              - export deploy_on_pypi="False"


        - os: linux
          language: python
          python: "3.8"
          before_install:
              - export mypy_strict_typecheck="True"
              - export build_docs="True"
              - export deploy_on_pypi="True"


        - os: linux
          language: python
          python: "3.8-dev"
          before_install:
              - export mypy_strict_typecheck="True"
              - export build_docs="False"
              - export deploy_on_pypi="False"


        - os: linux
          language: python
          python: "pypy3"
          before_install:
              - export mypy_strict_typecheck="False"
              - export build_docs="False"
              - export deploy_on_pypi="False"


        - os: osx
          language: sh
          name: "macOS 10.15.4"
          python: "3.8"
          osx_image: xcode11.5
          env:
            # on osx pip and python points to python 2.7 - therefore we have to use pip3 and python3 here
            - cPREFIX=""				# prefix before commands - used for wine, there the prefix is "wine"
            - cPYTHON="python3"			# command to launch python interpreter (its different on macOs, there we need python3)
            - cPIP="python3 -m pip"   	# command to launch pip (its different on macOs, there we need pip3)


    install:
        # install lib_bash_wine - this installs also lib_bash
        - $(command -v sudo 2>/dev/null) git clone https://github.com/bitranox/lib_bash_wine.git /usr/local/lib_bash_wine
        - $(command -v sudo 2>/dev/null) chmod -R 0755 /usr/local/lib_bash_wine
        - $(command -v sudo 2>/dev/null) chmod -R +x /usr/local/lib_bash_wine/*.sh
        - $(command -v sudo 2>/dev/null) /usr/local/lib_bash_wine/install_or_update.sh
        - export lib_bash_color="/usr/local/lib_bash/lib_color.sh"
        - export lib_bash_banner="/usr/local/lib_bash/lib_helpers.sh banner"
        - export lib_bash_banner_warning="/usr/local/lib_bash/lib_helpers.sh banner_warning"
        - export lib_bash_wine="/usr/local/lib_bash_wine"
        - ${lib_bash_banner} "upgrading pip"; ${cPREFIX} ${cPIP} install --upgrade pip
        - ${lib_bash_banner} "upgrading setuptools"; ${cPREFIX} ${cPIP} install --upgrade setuptools
        - ${lib_bash_banner} "upgrading wheel"; ${cPREFIX} ${cPIP} install --upgrade wheel
        - ${lib_bash_banner} "upgrading pytest-pycodestyle"; ${cPREFIX} ${cPIP} install --upgrade "pytest-pycodestyle; python_version >= \"3.5\""
        - ${lib_bash_banner} "installing lib_log_utils"; ${cPREFIX} ${cPIP} install git+https://github.com/bitranox/lib_log_utils.git
        - if [[ ${build_docs} == "True" ]]; then
              ${lib_bash_banner} "installing rst_include"; ${cPREFIX} ${cPIP} install git+https://github.com/bitranox/rst_include.git;
          fi

        - if [[ ${cPREFIX} == "wine" ]]; then ${lib_bash_wine}/001_000_install_wine.sh ; fi
        - if [[ ${cPREFIX} == "wine" ]]; then ${lib_bash_wine}/002_000_install_wine_machine.sh ; fi
        - if [[ ${wine_python_version} == "python3" ]]; then ${lib_bash_wine}/003_000_install_wine_python3_preinstalled.sh ; fi
        - if [[ ${cPREFIX} == "wine" ]]; then ${lib_bash_wine}/004_000_install_wine_git_portable.sh ; fi
        - if [[ ${cPREFIX} == "wine" ]]; then ${lib_bash_wine}/005_000_install_wine_powershell_core.sh ; fi

    script:

        # setup.py test
        - COMMAND="${cPREFIX} ${cPYTHON} ./setup.py test"
        - ${lib_bash_banner} "running '${COMMAND}'"
        - if ${COMMAND}; then ${lib_bash_banner} "'${COMMAND}' - OK"; else ${lib_bash_banner_warning} "'${COMMAND}' - FAILED" && exit 1; fi

        # pip install git+https://github.com/bitranox/lib_travis.git --install-option test
        - COMMAND="${cPREFIX} ${cPIP} install git+https://github.com/bitranox/lib_travis.git --install-option test"
        - ${lib_bash_banner} "running '${COMMAND}'"
        - if ${COMMAND}; then ${lib_bash_banner} "'${COMMAND}' - OK"; else ${lib_bash_banner_warning} "'${COMMAND}' - FAILED" && exit 1; fi

        # pip install git+https://github.com/bitranox/lib_travis.git
        - COMMAND="${cPREFIX} ${cPIP} install git+https://github.com/bitranox/lib_travis.git"
        - ${lib_bash_banner} "running '${COMMAND}'"
        - if ${COMMAND}; then ${lib_bash_banner} "'${COMMAND}' - OK"; else ${lib_bash_banner_warning} "'${COMMAND}' - FAILED" && exit 1; fi

        # commandline registration check
        - COMMAND="${cPREFIX} lib_travis --version"
        - ${lib_bash_banner} "running '${COMMAND}' (check commandline registration)"
        - if ${COMMAND}; then ${lib_bash_banner} "'${COMMAND}' - OK"; else ${lib_bash_banner_warning} "'${COMMAND}' - FAILED" && exit 1; fi

        # pytest codecov only
        - COMMAND="${cPREFIX} ${cPYTHON} -m pytest --cov=lib_travis"
        - ${lib_bash_banner} "running '${COMMAND}' - (coverage only)"
        - ${cPREFIX} ${cPIP} install --upgrade -r ./requirements_test.txt > /dev/null 2>&1
        - ${cPREFIX} ${cPIP} install --upgrade codecov > /dev/null 2>&1
        - ${cPREFIX} ${cPIP} install --upgrade pytest-cov > /dev/null 2>&1
        - if ${COMMAND}; then ${lib_bash_banner} "'${COMMAND}' - OK"; else ${lib_bash_banner_warning} "'${COMMAND}' - FAILED" && exit 1; fi

        # mypy typecheck strict
        - if [[ ${mypy_strict_typecheck} == "True" ]]; then
              COMMAND="${cPREFIX} ${cPYTHON} -m mypy -p lib_travis --strict --no-warn-unused-ignores --implicit-reexport --follow-imports=silent";
              ${lib_bash_banner} "running '${COMMAND}'";
              if ${COMMAND}; then ${lib_bash_banner} "'${COMMAND}' - OK"; else ${lib_bash_banner_warning} "'${COMMAND}' - FAILED" && exit 1; fi
          else
              ${lib_bash_banner_warning} "mypy typecheck --strict disabled on this build";
          fi

        # Bild Docs
        - if [[ "${build_docs}" == "True" ]]; then
              COMMAND="${cPREFIX}" rst_include include "./.docs/README_template.rst" "./README.rst";
              ${lib_bash_banner} "running '${COMMAND}' - rebuild README.rst";
              if ${COMMAND}; then ${lib_bash_banner} "'${COMMAND}' - OK"; else ${lib_bash_banner_warning} "'${COMMAND}' - FAILED" && exit 1; fi
          else
              ${lib_bash_banner_warning} "rebuild README.rst disabled on this build" ;
          fi

        # Check if Deployment would work on non-tagged builds
        - if [[ -f setup.py ]] && [[ -z ${TRAVIS_TAG} ]] && [[ ${build_docs} == "True" ]]; then
              ${lib_bash_banner} "Testing PyPi Deployment";
              ${cPREFIX} ${cPIP} install readme_renderer > /dev/null 2>&1;
              ${cPREFIX} ${cPIP} install --upgrade twine > /dev/null 2>&1;
              ${cPREFIX} ${cPIP} install wheel > /dev/null 2>&1;
              ${cPREFIX} ${cPYTHON} setup.py sdist bdist_wheel || ${lib_bash_banner_warning} "Building Wheels failed" 1>&2;
              if ${cPREFIX} twine check dist/*; then
                  ${lib_bash_banner} "PyPi Deployment would be OK";
              else
                  ${lib_bash_banner_warning} "PyPi Deployment would fail";
                  exit 1;
              fi
          else
              ${lib_bash_banner_warning} "Check PyPi Deployment disabled on this build" ;
          fi

    after_success:
        - ${cPREFIX} coverage report
        - ${cPREFIX} codecov
        # codeclimate coverage upload - TODO: check function on wine
        - if [ "${TRAVIS_OS_NAME}" == 'windows' ]; then
              CODECLIMATE_REPO_TOKEN="${CC_TEST_REPORTER_ID}";
              ${cPREFIX} ${cPIP} install codeclimate-test-reporter;
              ${cPREFIX} codeclimate-test-reporter;
          else
              curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter;
              chmod +x ./cc-test-reporter;
              ./cc-test-reporter after-build --exit-code $TRAVIS_TEST_RESULT;
          fi

        # This works for sure - the Travis deploy is somehow buggy.
        # create the secret :
        # pypi_password
        # to create the secret :
        # cd /<repository>
        # sudo travis encrypt -r <github_account>/<repository> pypi_password=*****
        # copy and paste the encrypted password in the PizzaCutter Config File
        - if [[ ${deploy_on_pypi} == "True" ]] && [[ -n ${TRAVIS_TAG} ]]; then
              ${lib_bash_banner} "Deploy on PyPi";
              export travis_deploy="True";
              ${cPREFIX} ${cPIP} install readme_renderer;
              ${cPREFIX} ${cPIP} install --upgrade twine;
              ${cPREFIX} ${cPIP} install wheel;
              ${cPREFIX} ${cPYTHON} setup.py sdist bdist_wheel;
              ${cPREFIX} twine check dist/*;
              ${cPREFIX} twine upload --repository-url https://upload.pypi.org/legacy/ -u bitranox -p ${pypi_password} dist/*;
          fi

    notifications:
      email:
        recipients:
            - bitranox@gmail.com
        on_success: never # default: change
        on_failure: always # default: always

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
     after_success  coverage reports
     deploy         deploy on pypi
     get_branch     get the branch to work on
     info           get program informations
     install        updates pip, setuptools, wheel, pytest-pycodestyle
     run            run string command wrapped in run/success/error banners
     run_x          run commands wrapped in run/success/error banners
     script         updates pip, setuptools, wheel, pytest-pycodestyle

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


1.0.2
--------
2020-07-29: feature release
    - do not reveal secrets in error messages

1.0.1
--------
2020-07-29: feature release
    - documentation updates

1.0.0
--------
2020-07-29: Release 1.0.0 fully functional


0.4.9
-------
2020-07-27: feature release
    - add command script
    - add command after_success
    - add command deploy


0.4.8
-------
2020-07-27: debug


0.4.7
-------
2020-07-27: debug


0.4.6
-------
2020-07-27: debug


0.4.5
-------
2020-07-27: feature release
    - add command run_tests

0.4.3
-------
2020-07-27: feature release
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

