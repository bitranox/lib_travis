# STDLIB
import os
import subprocess
import sys
from typing import List

# OWN
import lib_log_utils


def run_command(l_commands: List[str]) -> None:
    """
    runs a command and wraps it in "success" or "error" banners

    >>> run_command(['unknown', 'command'])
    Traceback (most recent call last):
        ...
    SystemExit: ...

    >>> run_command(['echo', 'test'])

    """
    lib_log_utils.setup_handler()
    command = ' '.join(l_commands)
    try:
        lib_log_utils.banner_debug('run: "{}"'.format(command))
        subprocess.run(command, shell=True, check=True)
        lib_log_utils.banner_success('success: "{}"'.format(command))
    except subprocess.CalledProcessError as exc:
        lib_log_utils.banner_error('error: "{}"\n{}'.format(command, exc))
        if hasattr(exc, 'returncode'):
            if exc.returncode is not None:
                sys.exit(exc.returncode)
        sys.exit(1)     # pragma: no cover


def get_branch() -> str:
    """
    Return the branch to work on
                        TRAVIS_BRANCH   TRAVIS_PULL_REQUEST_BRANCH  TRAVIS_TAG
    Custom Build -->    <branch>        -                           -
    Push         -->    <branch>        -                           -
    Pull Request -->    <master>        <branch>                    -               # if pr-tag is set, we should return that tag
    Tagged       -->    <tag>           -                           <tag>           # if travis tag is set, we should return "master"


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

    >>> # Teardown
    >>> if save_TRAVIS_TAG is not None: os.environ['TRAVIS_BRANCH'] = save_TRAVIS_TAG
    >>> if save_TRAVIS_PULL_REQUEST_BRANCH is not None: os.environ['TRAVIS_PULL_REQUEST_BRANCH'] = save_TRAVIS_PULL_REQUEST_BRANCH
    >>> if save_TRAVIS_BRANCH is not None: os.environ['TRAVIS_BRANCH'] = save_TRAVIS_BRANCH

    """
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
