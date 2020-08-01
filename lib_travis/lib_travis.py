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


# run{{{
def run(description: str, command: str, retry: int = 3, sleep: int = 30, quote: bool = False, banner: bool = True, show_command: bool = True) -> None:
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
    show_command
        if the command is shown - take care not to reveal secrets here !


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
    # run}}}

    command = command.strip()

    if quote:
        command = shlex.quote(command)

    lib_log_utils.setup_handler()

    if show_command:
        command_description = command
    else:
        command_description = '***secret***'

    lib_log_utils.banner_success("Action: {description}\nCommand: {command}".format(description=description, command=command_description), banner=banner)
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
                    sleep=sleep, description=description, command=command_description), banner=False)
                time.sleep(sleep)
            else:
                if show_command:
                    exc_message = str(exc)
                else:
                    exc_message = 'Command ***secret*** returned non-zero exit status'
                lib_log_utils.banner_error("Error: {description}\nCommand: {command}\n{exc}".format(
                    description=description, command=command_description, exc=exc_message), banner=True)
                if hasattr(exc, 'returncode'):
                    if exc.returncode is not None:  # type: ignore
                        sys.exit(exc.returncode)    # type: ignore
                sys.exit(1)     # pragma: no cover
        finally:
            cli_exit_tools.flush_streams()


# run_x{{{
def run_x(description: str, commands: List[str], retry: int = 3, sleep: int = 30, split: bool = True, banner: bool = False, show_command: bool = True) -> None:
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
    show_command
        if the command is shown - take care not to reveal secrets here !


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
    # run_x}}}

    if split:
        splitted_commands: List[str] = list()
        for command in commands:
            sp_commands = shlex.split(command)
            splitted_commands = splitted_commands + sp_commands
        commands = splitted_commands

    lib_log_utils.setup_handler()

    if show_command:
        command_description = ' '.join(commands)
    else:
        command_description = '***secret***'

    lib_log_utils.banner_success("Action: {description}\nCommand: {command}".format(description=description, command=command_description), banner=banner)
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
                    sleep=sleep, description=description, command=command_description), banner=False)
                time.sleep(sleep)
            else:
                if show_command:
                    exc_message = str(exc)
                else:
                    exc_message = 'Command ***secret*** returned non-zero exit status'
                lib_log_utils.banner_error("Error: {description}\nCommand: {command}\n{exc}".format(
                    description=description, command=command_description, exc=exc_message), banner=True)
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


# install{{{
def install(dry_run: bool = True) -> None:
    """
    upgrades pip, setuptools, wheel and pytest-pycodestyle


    Parameter
    ---------
    cPIP
        from environment, the command to launch pip, like "python -m pip"


    Examples
    --------
    >>> install()

    """
    # install}}}
    if dry_run:
        return
    pip_prefix = get_pip_prefix()
    run(description='install pip', command=' '.join([pip_prefix, 'install --upgrade pip']))
    run(description='install setuptools', command=' '.join([pip_prefix, 'install --upgrade setuptools']))
    run(description='install readme renderer', command=' '.join([pip_prefix, 'install --upgrade readme_renderer']))
    run(description='install twine', command=' '.join([pip_prefix, 'install --upgrade twine']))
    run(description='install wheel', command=' '.join([pip_prefix, 'install --upgrade wheel']))
    run(description='install pycodestyle', command=' '.join([pip_prefix, 'install --upgrade pycodestyle']))
    run(description='install pytest-pycodestyle', command=' '.join([pip_prefix, 'install --upgrade "pytest-pycodestyle; python_version >= \\"3.5\\""']))


# script{{{
def script(dry_run: bool = True) -> None:
    """
    travis jobs to run in travis.yml section "script":
    - run setup.py test
    - run pip with install option test
    - run pip standard install
    - test the CLI Registration
    - install the test requirements
    - install codecov
    - install pytest-codecov
    - run pytest coverage
    - run mypy strict
        - if MYPY_STRICT="True"
    - rebuild the rst files (resolve rst file includes)
        - needs RST_INCLUDE_SOURCE, RST_INCLUDE_TARGET set and BUILD_DOCS="True"
    - check if deployment would succeed, if setup.py exists and not a tagged build

    Parameter
    ---------
    cPREFIX
        from environment, the command prefix like 'wine' or ''
    cPIP
        from environment, the command to launch pip, like "python -m pip"
    cPYTHON
        from environment, the command to launch python, like 'python' or 'python3' on MacOS
    CLI_COMMAND
        from environment, must be set in travis - the CLI command to test with option --version
    MYPY_STRICT
        from environment, if pytest with mypy --strict should run
    PACKAGE_NAME
        from environment, the package name to pass to mypy
    BUILD_DOCS
        from environment, if rst file should be rebuilt
    RST_INCLUDE_SOURCE
        from environment, the rst template with rst includes to resolve
    RST_INCLUDE_TARGET
        from environment, the rst target file
    DEPLOY_WHEEL
        from environment, if a wheel should be generated
        only if setup.py exists and on non-tagged builds (there we deploy for real)
    dry_run
        if set, this returns immediately - for CLI tests


    Examples
    --------
    >>> script()

    """
    # script}}}
    if dry_run:
        return
    lib_log_utils.setup_handler()
    cli_command = os.getenv('CLI_COMMAND', '')
    command_prefix = get_command_prefix()
    pip_prefix = get_pip_prefix()
    python_prefix = get_python_prefix()
    repository = get_repository()
    package_name = os.getenv('PACKAGE_NAME', '')
    run(description='setup.py test', command=' '.join([python_prefix, './setup.py test']))
    run(description='pip install, option test', command=' '.join([pip_prefix, 'install', repository, '--install-option test']))
    run(description='pip standard install', command=' '.join([pip_prefix, 'install', repository]))
    run(description='check CLI command', command=' '.join([command_prefix, cli_command, '--version']))
    run(description='install test requirements', command=' '.join([pip_prefix, 'install --upgrade -r ./requirements_test.txt']))
    run(description='install codecov', command=' '.join([pip_prefix, 'install --upgrade codecov']))
    run(description='install pytest-cov', command=' '.join([pip_prefix, 'install --upgrade pytest-cov']))
    run(description='run pytest, coverage only', command=' '.join([python_prefix, '-m pytest --cov={package_name}'.format(package_name=package_name)]))

    if do_mypy_strict_check():

        run(description='run mypy strict', command=' '.join([python_prefix, '-m mypy -p', package_name, '--strict --no-warn-unused-ignores',
                                                             '--implicit-reexport --follow-imports=silent']))
    else:
        lib_log_utils.banner_notice("mypy typecheck --strict disabled on this build")

    if do_build_docs():
        rst_include_source = os.getenv('RST_INCLUDE_SOURCE', '')
        rst_include_target = os.getenv('RST_INCLUDE_TARGET', '')
        rst_include_source_name = pathlib.Path(rst_include_source).name
        rst_include_target_name = pathlib.Path(rst_include_target).name
        run(description=' '.join(['rst rebuild', rst_include_target_name, 'from', rst_include_source_name]),
            command=' '.join([command_prefix, 'rst_include include', rst_include_source, rst_include_target]))
    else:
        lib_log_utils.banner_notice("rebuild doc file is disabled on this build")

    if do_deploy_sdist() or do_build_test():
        run(description='create source distribution', command=' '.join([python_prefix, 'setup.py sdist']))
    else:
        lib_log_utils.banner_notice("create source distribution is disabled on this build")

    if do_deploy_wheel() or do_build_test():
        run(description='create binary distribution (wheel)', command=' '.join([python_prefix, 'setup.py bdist_wheel']))
        # run(description='create binary distribution (wheel)', command=' '.join([python_prefix, '-m cibuildwheel --output-dir dist']))
    else:
        lib_log_utils.banner_notice("create wheel distribution is disabled on this build")

    if do_deploy_sdist() or do_deploy_wheel() or do_build_test():
        run(description='check distributions', command=' '.join([command_prefix, 'twine check dist/*']))


# after_success{{{
def after_success(dry_run: bool = True) -> None:
    """
    travis jobs to run in travis.yml section "after_success":
        - coverage report
        - codecov
        - codeclimate report upload


    Parameter
    ---------
    cPREFIX
        from environment, the command prefix like 'wine' or ''
    cPIP
        from environment, the command to launch pip, like "python -m pip"
    CC_TEST_REPORTER_ID
        from environment, must be set in travis
    TRAVIS_TEST_RESULT
        from environment, this is set by TRAVIS automatically
    dry_run
        if set, this returns immediately - for CLI tests


    Examples
    --------
    >>> after_success()

    """
    # after_success}}}

    if dry_run:
        return
    command_prefix = get_command_prefix()
    pip_prefix = get_pip_prefix()

    run(description='coverage report', command=' '.join([command_prefix, 'coverage report']))
    run(description='codecov', command=' '.join([command_prefix, 'codecov']))

    if os.getenv('CC_TEST_REPORTER_ID'):
        if os_is_windows():
            os.environ['CODECLIMATE_REPO_TOKEN'] = os.getenv('CC_TEST_REPORTER_ID', '')
            run(description='install codeclimate-test-reporter', command=' '.join([pip_prefix, 'install codeclimate-test-reporter']))
            run(description='report to codeclimate', command=' '.join([command_prefix, 'codeclimate-test-reporter']))
        else:
            run(description='download test reporter',
                command='curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter')
            run(description='test reporter set permissions', banner=False, command='chmod +x ./cc-test-reporter')
            travis_test_result = os.getenv('TRAVIS_TEST_RESULT', '')
            run(description='report to codeclimate', command=' '.join(['./cc-test-reporter after-build --exit-code', travis_test_result]))
    else:
        lib_log_utils.banner_notice("Code Climate Coverage is disabled, no CC_TEST_REPORTER_ID")


# deploy{{{
def deploy(dry_run: bool = True) -> None:
    """
    uploads sdist and wheels to pypi on success


    Parameter
    ---------
    cPREFIX
        from environment, the command prefix like 'wine' or ''
    PYPI_PASSWORD
        from environment, passed as secure, encrypted variable to environment
    TRAVIS_TAG
        from environment, needs to be set
    DEPLOY_SDIST, DEPLOY_WHEEL
        from environment, one of it needs to be true
    dry_run
        if set, this returns immediately - for CLI tests


    Examples
    --------
    >>> deploy()

    """
    # deploy}}}

    if dry_run:
        return

    command_prefix = get_command_prefix()
    github_username = get_github_username()
    pypi_password = os.getenv('PYPI_PASSWORD', '')

    if do_deploy():
        run(description='upload to pypi', command=' '.join([command_prefix, 'twine upload --repository-url https://upload.pypi.org/legacy/ -u',
                                                            github_username, '-p', pypi_password, 'dist/*']), show_command=False)
    else:
        lib_log_utils.banner_notice("pypi deploy is disabled on this build")


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
    c_parts.append(get_branch())
    repository = ''.join(c_parts)
    return repository


def get_github_username() -> str:
    """
    get the github username like 'bitranox'

    >>> discard = get_github_username()

    """
    repo_slug = os.getenv('TRAVIS_REPO_SLUG', '')
    github_username = repo_slug.split('/')[0]
    return github_username


def do_mypy_strict_check() -> bool:
    """ if mypy check should run """
    if os.getenv('MYPY_STRICT', '').lower() == 'true':
        return True
    else:
        return False


def do_build_docs() -> bool:
    """ if README.rst should be rebuilt """
    if os.getenv('BUILD_DOCS', '').lower() != 'true':
        return False

    if not os.getenv('RST_INCLUDE_SOURCE'):
        return False

    if not os.getenv('RST_INCLUDE_TARGET'):
        return False
    else:
        return True


def do_deploy_sdist() -> bool:
    if os.getenv('DEPLOY_SDIST', '').lower() == 'true':
        return True
    else:
        return False


def do_deploy_wheel() -> bool:
    if os.getenv('DEPLOY_WHEEL', '').lower() == 'true':
        return True
    else:
        return False


def do_build_test() -> bool:
    if os.getenv('BUILD_TEST', '').lower() == 'true':
        return True
    else:
        return False


def do_check_deployment() -> bool:
    """ if we should check if deployment would work on pypi
        we only check when :
            - setup.py is existing
            - there is no Travis_TAG (then it will be deployed anyway
            - and CHECK_DEPLOYMENT = True
    """
    path_setup_file = pathlib.Path('./setup.py')

    if not path_setup_file.is_file():
        return False
    if os.getenv('TRAVIS_TAG'):
        return False
    if os.getenv('DEPLOY_CHECK', '').lower() == 'true':
        return True
    else:
        return False


def on_travis() -> bool:
    """
    if we run on travis
    """
    if 'TRAVIS' in os.environ:
        return True
    else:
        return False


def os_is_windows() -> bool:
    if os.getenv('TRAVIS_OS_NAME', '').lower() == 'windows':
        return True
    else:
        return False


def do_deploy() -> bool:
    """
    if we should deploy
        - when $deploy_on_pypi = True
        - when TRAVIS_TAG != ''
    """
    if not os.getenv('TRAVIS_TAG'):
        return False
    if do_deploy_sdist() or do_deploy_wheel():
        return True
    else:
        return False


if __name__ == '__main__':
    print(b'this is a library only, the executable is named "lib_travis_cli.py"', file=sys.stderr)
