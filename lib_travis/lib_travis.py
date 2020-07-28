# STDLIB
import os
import shlex
import subprocess
import sys
import time
from typing import List

# OWN
import lib_log_utils
import cli_exit_tools


# run_command{{{
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
    # run_command}}}

    command = command.strip()
    # test
    command = command.replace('.git', '.git@{BRANCH}'.format(BRANCH=get_branch()))

    if quote:
        command = shlex.quote(command)

    lib_log_utils.setup_handler()
    lib_log_utils.banner_success("Action: {description}\nCommand: {command}".format(description=description, command=command), banner=banner)
    tries = retry
    while True:
        try:
            subprocess.run(command, shell=True, check=True)
            lib_log_utils.banner_success("Success: {description}".format(description=description), banner=False)
            break
        except Exception as exc:
            tries = tries - 1
            # try 3 times, because sometimes connection or other errors on travis
            if tries:
                lib_log_utils.banner_notice("Retry in {sleep} seconds: {description}\nCommand: {command}".format(
                    sleep=sleep, description=description, command=command), banner=False)
                time.sleep(sleep)
            else:
                lib_log_utils.banner_error("Error: {description}\nCommand: {command}\n{exc}".format(description=description, command=command, exc=exc),
                                           banner=True)
                if hasattr(exc, 'returncode'):
                    if exc.returncode is not None:  # type: ignore
                        sys.exit(exc.returncode)    # type: ignore
                sys.exit(1)     # pragma: no cover
        finally:
            cli_exit_tools.flush_streams()


# run_commands{{{
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
    # run_commands}}}

    if split:
        splitted_commands: List[str] = list()
        for command in commands:
            sp_commands = shlex.split(command)
            splitted_commands = splitted_commands + sp_commands
        commands = splitted_commands

    str_command = ' '.join(commands)
    lib_log_utils.setup_handler()
    lib_log_utils.banner_success("Action: {description}\nCommand: {command}".format(description=description, command=str_command), banner=banner)
    tries = retry
    while True:
        try:
            subprocess.run(commands, shell=True, check=True)
            lib_log_utils.banner_success("Success : {description}".format(description=description), banner=False)
            break
        except Exception as exc:
            tries = tries - 1
            # try 3 times, because sometimes connection or other errors on travis
            if tries:
                lib_log_utils.banner_notice("Retry in {sleep} seconds: {description}\nCommand: {command}".format(
                    sleep=sleep, description=description, command=str_command), banner=False)
                time.sleep(sleep)
            else:
                lib_log_utils.banner_error("Error: {description}\nCommand: {command}\n{exc}".format(description=description, command=str_command, exc=exc),
                                           banner=True)
                if hasattr(exc, 'returncode'):
                    if exc.returncode is not None:      # type: ignore
                        sys.exit(exc.returncode)        # type: ignore
                sys.exit(1)     # pragma: no cover
        finally:
            cli_exit_tools.flush_streams()


# get_branch{{{
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
    # get_branch}}}

    if 'TRAVIS_TAG' in os.environ and os.environ['TRAVIS_TAG']:
        branch = 'master'
    elif 'TRAVIS_PULL_REQUEST_BRANCH' in os.environ and os.environ['TRAVIS_PULL_REQUEST_BRANCH']:
        branch = os.environ['TRAVIS_PULL_REQUEST_BRANCH']
    elif 'TRAVIS_BRANCH' in os.environ and os.environ['TRAVIS_BRANCH']:
        branch = os.environ['TRAVIS_BRANCH']
    else:
        branch = 'master'
    return branch


def upgrade_setup_related():
    """
    upgrades pip, setuptools, wheel and pytest-pycodestyle

    >>> if 'TRAVIS' in os.environ:
    ...    upgrade_setup_related()

    """
    run(description='upgrade pip', command='${cPREFIX} ${cPIP} install --upgrade pip')
    run(description='upgrade setuptools', command='${cPREFIX} ${cPIP} install --upgrade setuptools')
    run(description='upgrade wheel', command='${cPREFIX} ${cPIP} install --upgrade wheel')
    run(description='upgrading pytest-pycodestyle', command='${cPREFIX} ${cPIP} install --upgrade "pytest-pycodestyle; python_version >= \\"3.5\\""')


if __name__ == '__main__':
    print(b'this is a library only, the executable is named "lib_travis_cli.py"', file=sys.stderr)
