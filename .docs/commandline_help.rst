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
     run_tests              updates pip, setuptools, wheel, pytest-pycodestyle
     run_x                  run commands wrapped in run/success/error banners
     upgrade_setup_related  updates pip, setuptools, wheel, pytest-pycodestyle
