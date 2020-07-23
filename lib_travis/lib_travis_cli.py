# STDLIB
import sys
from typing import List, Optional

# EXT
import click

# CONSTANTS
CLICK_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
CLICK_CONTEXT_SETTINGS_RUN = dict(help_option_names=['-h', '--help'], ignore_unknown_options=True)

try:
    from . import __init__conf__
    from . import cli_exit_tools
    from . import lib_travis
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    # imports for doctest
    import __init__conf__                   # type: ignore  # pragma: no cover
    import cli_exit_tools                   # type: ignore  # pragma: no cover
    import lib_travis      # type: ignore  # pragma: no cover


def info() -> None:
    """
    >>> info()
    Info for ...

    """
    __init__conf__.print_info()


@click.group(help=__init__conf__.title, context_settings=CLICK_CONTEXT_SETTINGS)
@click.version_option(version=__init__conf__.version,
                      prog_name=__init__conf__.shell_command,
                      message='{} version %(version)s'.format(__init__conf__.shell_command))
@click.option('--traceback/--no-traceback', is_flag=True, type=bool, default=None, help='return traceback information on cli')
def cli_main(traceback: Optional[bool] = None) -> None:
    if traceback is not None:
        cli_exit_tools.config.traceback = traceback


@cli_main.command('info', context_settings=CLICK_CONTEXT_SETTINGS)
def cli_info() -> None:
    """ get program informations """
    info()


@cli_main.command('get_branch', context_settings=CLICK_CONTEXT_SETTINGS)
def cli_get_branch() -> None:
    """ get the branch to work on """
    response = lib_travis.get_branch()
    print(response)


@cli_main.command('run', context_settings=CLICK_CONTEXT_SETTINGS_RUN)
@click.argument('description')
@click.argument('commands', nargs=-1)
def cli_run(description: str, commands: List[str]) -> None:
    """ run commands and wrap them in run/success/error banners """
    lib_travis.run_command(description, commands)


# entry point if main
if __name__ == '__main__':
    try:
        cli_main()
    except Exception as exc:
        cli_exit_tools.print_exception_message()
        sys.exit(cli_exit_tools.get_system_exit_code(exc))
