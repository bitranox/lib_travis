Changelog
=========

- new MAJOR version for incompatible API changes,
- new MINOR version for added functionality in a backwards compatible manner
- new PATCH version for backwards compatible bug fixes


v2.0.6
---------
2020-08-01: fix cibuildwheel

v1.0.9
---------
2020-07-29: fix pypi deploy

v1.0.6
---------
2020-07-29: feature release
    - preserve Travis Tag

v1.0.5
---------
2020-07-29: feature release
    - pass correct package name to mypy and codecov

v1.0.4
---------
2020-07-29: feature release
    - use the new pizzacutter template
    - use cli_exit_tools

v1.0.3
---------
2020-07-29: feature release
    - fix code coverage test report

v1.0.2
---------
2020-07-29: feature release
    - do not reveal secrets in error messages

v1.0.1
---------
2020-07-29: feature release
    - documentation updates

v1.0.0
---------
2020-07-29: Release 1.0.0 fully functional

v0.4.9
---------
2020-07-27: feature release
    - add command script
    - add command after_success
    - add command deploy

v0.4.8
---------
2020-07-27: debug

v0.4.7
---------
2020-07-27: debug

v0.4.6
---------
2020-07-27: debug

v0.4.5
---------
2020-07-27: feature release
    - add command run_tests

v0.4.3
---------
2020-07-27: feature release
    - set default to --no-split on run_x
    - add command upgrade_setup_related

v0.4.2
---------
2020-07-27: feature release
    - change colors
    - catch all in run exceptions (OS Error)

v0.4.1
---------
2020-07-27: feature release
    - use cli_exit_tools
    - adding banner parameter to "run" commands

v0.4.0
---------
2020-07-23: feature release
    - rename commands

v0.3.1
---------
2020-07-23: feature release
    - add splitting of commands

v0.3.0
---------
2020-07-23: feature release
    - add second run method
    - add automatic quoting for commands passed as string

v0.2.1
---------
2020-07-23: patch release
    - flush streams on exit

v0.2.0
---------
2020-07-23: feature release
    - change arguments
    - add options for retry and sleep on run command

v0.1.3
---------
2020-07-23: patch release
    - correct doctests

v0.1.2
---------
2020-07-23: patch release
    - ignore unused options on cli run command
    - added description argument to run command

v0.1.1
---------
2020-07-23: initial release
    - setup
    - log utils
    - run wrapper
    - get the branch to work on
