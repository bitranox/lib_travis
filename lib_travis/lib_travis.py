# STDLIB
import os
import subprocess
import sys
import time
from typing import List

# OWN
import lib_log_utils


# run_command{{{
def run_command(description: str, command: str, retry: int = 3, sleep: int = 30) -> None:
    """
    runs and retries a command and wraps it in "success" or "error" banners


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


    Result
    ---------
    none


    Exceptions
    ------------
    none


    Examples
    ------------

    >>> run_command('test', "unknown command", sleep=0)
    Traceback (most recent call last):
        ...
    SystemExit: ...

    >>> run_command('test', "echo test")

    """
    # run_command}}}

    lib_log_utils.setup_handler()
    lib_log_utils.banner_debug("{description}\n{command}".format(description=description, command=command))
    tries = retry
    while True:
        try:
            subprocess.run(command, shell=True, check=True)
            lib_log_utils.banner_success("success : {description}\n{command}".format(description=description, command=command))
            break
        except subprocess.CalledProcessError as exc:
            tries = tries - 1
            # try 3 times, because sometimes connection or other errors on travis
            if tries:
                lib_log_utils.banner_notice("retry in {sleep} seconds: {description}\n{command}".format(
                    sleep=sleep, description=description, command=command))
                time.sleep(sleep)
            else:
                lib_log_utils.banner_error("error: {description}\n{command}\n{exc}".format(description=description, command=command, exc=exc))
                if hasattr(exc, 'returncode'):
                    if exc.returncode is not None:
                        sys.exit(exc.returncode)
                sys.exit(1)     # pragma: no cover


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


if __name__ == '__main__':
    print(b'this is a library only, the executable is named "lib_travis_cli.py"', file=sys.stderr)
