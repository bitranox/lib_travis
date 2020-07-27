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

.. include:: ../lib_travis/lib_travis.py
    :code: python
    :start-after: # get_branch{{{
    :end-before: # get_branch}}}


.. include:: ../lib_travis/lib_travis.py
    :code: python
    :start-after: # run_command{{{
    :end-before: # run_command}}}


.. include:: ../lib_travis/lib_travis.py
    :code: python
    :start-after: # run_commands{{{
    :end-before: # run_commands}}}
