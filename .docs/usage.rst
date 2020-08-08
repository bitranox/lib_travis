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


- run a command passed as string

.. code-block:: bash

    # to be used in travis.yml
    # run a command passed as string, wrap it in colored banners, retry 3 times, sleep 30 seconds when retry
    $> lib_travis run "description" "command -some -options" --retry=3 --sleep=30


- get the branch to work on from travis environment variables

.. code-block:: bash

    $> BRANCH=$(lib_travis get_branch)

python methods:

- install, jobs to do in the Travis "install" section

.. include:: ../lib_travis/lib_travis.py
    :code: python
    :start-after: # install{{{
    :end-before: # install}}}

- script, jobs to do in the Travis "script" section

.. include:: ../lib_travis/lib_travis.py
    :code: python
    :start-after: # script{{{
    :end-before: # script}}}

- after_success, jobs to do in the Travis "after_success" section

.. include:: ../lib_travis/lib_travis.py
    :code: python
    :start-after: # after_success{{{
    :end-before: # after_success}}}

- deploy, deploy to pypi in the Travis "after_success" section

.. include:: ../lib_travis/lib_travis.py
    :code: python
    :start-after: # deploy{{{
    :end-before: # deploy}}}

- get_branch, determine the branch to work on from Travis environment

.. include:: ../lib_travis/lib_travis.py
    :code: python
    :start-after: # get_branch{{{
    :end-before: # get_branch}}}


- run, usually used internally


.. include:: ../lib_travis/lib_travis.py
    :code: python
    :start-after: # run{{{
    :end-before: # run}}}

- travis.py example

.. include:: ../.travis.yml
    :code: yaml

