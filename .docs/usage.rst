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

- run_x, usually used internally

.. include:: ../lib_travis/lib_travis.py
    :code: python
    :start-after: # run_x{{{
    :end-before: # run_x}}}

- travis.py example

.. include:: ../.travis.yml
    :code: yaml

