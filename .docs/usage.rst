usage commandline:

.. code-block:: bash

    # to be used in travis.yml
    # run a command, wrap it in colored banners, retry 3 times, sleep 30 seconds when retry
    $> lib_travis run "description" "command -some -options" --retry=3 --sleep=30

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
