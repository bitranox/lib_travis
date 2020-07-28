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
