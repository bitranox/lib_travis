usage commandline:

.. code-block:: bash

    # run a command passed as a list of strings
    # You need to pass '--' after the options, then all following strings are considered as arguments,
    # otherwise options would cause an error
    # stat means, all options need to be stated before the '--' marker
    $> lib_travis run --retry=3 --sleep=30 -- "description" command -some -options

    # to be used in travis.yml
    # run a command passed as string, wrap it in colored banners, retry 3 times, sleep 30 seconds when retry
    $> lib_travis run_s "description" "command -some -options" --retry=3 --sleep=30

    # get the branch to work on from travis environment variables
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
