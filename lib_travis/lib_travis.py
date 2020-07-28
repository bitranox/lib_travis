# STDLIB
import os
import pathlib
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


def upgrade_setup_related(dry_run: bool) -> None:
    """
    upgrades pip, setuptools, wheel and pytest-pycodestyle

    >>> if 'TRAVIS' in os.environ:
    ...    upgrade_setup_related()

    """
    if dry_run:
        return
    pip_prefix = get_pip_prefix()
    run(description='install pip', command=' '.join([pip_prefix, 'install --upgrade pip']))
    run(description='install setuptools', command=' '.join([pip_prefix, 'install --upgrade setuptools']))
    run(description='install wheel', command=' '.join([pip_prefix, 'install --upgrade wheel']))
    run(description='install pytest-pycodestyle', command=' '.join([pip_prefix, 'install --upgrade "pytest-pycodestyle; python_version >= \\"3.5\\""']))


def run_tests(dry_run: bool) -> None:
    if dry_run:
        return
    lib_log_utils.setup_handler()
    cli_command = get_cli_command()
    command_prefix = get_command_prefix()
    pip_prefix = get_pip_prefix()
    python_prefix = get_python_prefix()
    repository = get_repository()
    repo_name = get_repo_name()
    run(description='setup.py test', command=' '.join([python_prefix, './setup.py test']))

    command = ' '.join([pip_prefix, 'install', repository, '--install-option test'])
    lib_log_utils.banner_debug('repository: {}'.format(repository))
    lib_log_utils.banner_debug('command: {}'.format(command))

    run(description='pip install, option test', command=command)
    run(description='pip standard install', command=' '.join([pip_prefix, 'install', repository]))
    run(description='check CLI command', command=' '.join([command_prefix, cli_command, '--version']))
    run(description='install test requirements', command=' '.join([pip_prefix, 'install --upgrade -r ./requirements_test.txt']))
    run(description='install codecov', command=' '.join([pip_prefix, 'install --upgrade codecov']))
    run(description='install pytest-cov', command=' '.join([pip_prefix, 'install --upgrade pytest-cov']))
    run(description='run pytest, coverage only', command=' '.join([python_prefix, '-m pytest --cov={}'.format(repo_name)]))

    if do_mypy_strict_check():
        run(description='run mypy strict', command=' '.join([python_prefix, '-m mypy -p', repo_name, '--strict --no-warn-unused-ignores',
                                                             '--implicit-reexport --follow-imports=silent']))
    else:
        lib_log_utils.banner_notice("mypy typecheck --strict disabled on this build")

    if do_build_docs():
        run(description='rebuild README.rst', command=' '.join([command_prefix, cli_command,
                                                                'rst_include include "./.docs/README_template.rst" "./README.rst"']))
    else:
        lib_log_utils.banner_notice("rebuild READE.rst is disabled on this build")

    if do_check_deployment():
        run(description='install readme renderer', command=' '.join([pip_prefix, 'install --upgrade readme_renderer']))
        run(description='install twine', command=' '.join([pip_prefix, 'install --upgrade twine']))
        run(description='install wheel', command=' '.join([pip_prefix, 'install --upgrade wheel']))
        run(description='create source distribution', command=' '.join([python_prefix, 'setup.py sdist']))
        run(description='create binary distribution (wheel)', command=' '.join([python_prefix, 'setup.py bdist_wheel']))
        run(description='check distributions', command=' '.join([command_prefix, 'twine check dist/*']))
    else:
        lib_log_utils.banner_notice("check pypy deployment is disabled on this build")


def get_pip_prefix() -> str:
    """
    get the pip_prefix including the command prefix like : 'wine python -m pip'

    >>> if 'TRAVIS' in os.environ:
    ...    discard = get_pip_prefix()

    """
    c_parts: List[str] = list()
    c_parts.append(get_command_prefix())
    if 'cPIP' in os.environ:
        c_parts.append(os.environ['cPIP'])
    command_prefix = ' '.join(c_parts).strip()
    return command_prefix


def get_python_prefix() -> str:
    """
    get the python_prefix including the command prefix like : 'wine python'

    >>> if 'TRAVIS' in os.environ:
    ...    discard = get_python_prefix()

    """
    c_parts: List[str] = list()
    c_parts.append(get_command_prefix())
    if 'cPYTHON' in os.environ:
        c_parts.append(os.environ['cPYTHON'])
    python_prefix = ' '.join(c_parts).strip()
    return python_prefix


def get_command_prefix() -> str:
    """
    get the command_prefix like : 'wine' or ''
    """

    command_prefix = ''
    if 'cPREFIX' in os.environ:
        command_prefix = os.environ['cPREFIX']
    return command_prefix


def get_repository() -> str:
    """
    get the repository including the branch to work on , like :
    'git+https://github.com/bitranox/lib_travis.git@master'

    >>> get_repository()
    'git+https://github.com/...git@...'

    """

    c_parts: List[str] = list()
    c_parts.append('git+https://github.com/')
    if 'TRAVIS_REPO_SLUG' in os.environ:
        c_parts.append(os.environ['TRAVIS_REPO_SLUG'])
    c_parts.append('.git@')
    branch = get_branch()
    lib_log_utils.banner_debug('branch: {}'.format(branch))
    c_parts.append(branch)
    repository = ''.join(c_parts)
    return repository


def get_repo_name() -> str:
    """
    get the repo name like 'lib_travis'

    >>> discard = get_repo_name()

    """
    repo_name = ''
    if 'TRAVIS_REPO_SLUG' in os.environ:
        repo_slug = os.environ['TRAVIS_REPO_SLUG']
        repo_name = repo_slug.split('/')[1]
    return repo_name


def get_cli_command() -> str:
    """
    get the registered CLI Command like 'lib_travis'
    this will be used to check commandline registration like : lib_travis --version

    """
    cli_command = ''
    if 'CLI_COMMAND' in os.environ:
        cli_command = os.environ['CLI_COMMAND']
    return cli_command


def do_mypy_strict_check() -> bool:
    """ if mypy check should run """
    if 'mypy_strict_typecheck' in os.environ and os.environ['mypy_strict_typecheck'].lower() == 'true':
        return True
    else:
        return False


def do_build_docs() -> bool:
    """ if README.rst should be rebuilt """
    if 'build_docs' in os.environ and os.environ['build_docs'].lower() == 'true':
        return True
    else:
        return False


def do_check_deployment() -> bool:
    """ if we should check if deployment would work on pypi
        we only check when :
            - setup.py is existing
            - there is no Travis_TAG (then it will be deployed anyway
            - and build_docs = True
    """
    path_setup_file = pathlib.Path('./setup.py')
    if not path_setup_file.is_file():
        return False
    if 'TRAVIS_TAG' in os.environ and os.environ['TRAVIS_TAG'] != '':
        return False
    return do_build_docs()


def on_travis() -> bool:
    """
    if we run on travis
    """
    if 'TRAVIS' in os.environ:
        return True
    else:
        return False


if __name__ == '__main__':
    print(b'this is a library only, the executable is named "lib_travis_cli.py"', file=sys.stderr)
