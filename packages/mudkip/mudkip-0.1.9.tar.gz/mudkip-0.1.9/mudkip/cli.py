import sys
import time
from os import path
from functools import wraps
from contextlib import contextmanager
from traceback import format_exc

import click

from . import __version__
from .application import Mudkip
from .config import Config
from .errors import MudkipError
from .preset import Preset


DIRECTORY = click.Path(file_okay=False)


@contextmanager
def exception_handler(exit=False):
    try:
        yield
    except Exception as exc:
        error = exc.args[0] if isinstance(exc, MudkipError) else format_exc()
        click.secho(error, fg="red", bold=True)

        if exit:
            sys.exit(1)


def print_version(ctx, _param, value):
    if not value or ctx.resilient_parsing:
        return
    click.secho(f"Mudkip v{__version__}", fg="blue")
    ctx.exit()


@click.group()
@click.option(
    "--version",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=print_version,
    help="Show the version and exit.",
)
def mudkip():
    """A friendly Sphinx wrapper."""


def with_application(command):
    @click.option(
        "--preset",
        type=click.Choice(list(Preset.registry)),
        help="Documentation preset.",
    )
    @click.option("--source-dir", type=DIRECTORY, help="The source directory.")
    @click.option("--output-dir", type=DIRECTORY, help="The output directory.")
    @click.option("--verbose", is_flag=True, help="Show Sphinx output.")
    @wraps(command)
    def wrapper(preset, source_dir, output_dir, verbose, *args, **kwargs):
        params = dict(
            preset=preset, source_dir=source_dir, output_dir=output_dir, verbose=verbose
        )
        for key, value in tuple(params.items()):
            if not value:
                del params[key]
        return command(*args, application=Mudkip(**params), **kwargs)

    return wrapper


@mudkip.command()
@click.option("--title", help="Documentation title.")
@with_application
def init(application, title):
    """Initialize documentation."""
    padding = "\n" * application.config.verbose

    click.secho(
        f'{padding}Initializing "{application.config.source_dir}"...', fg="blue"
    )

    with exception_handler(exit=True):
        application.init(title)

    click.secho("\nDone.", fg="yellow")


@mudkip.command()
@click.option("--check", is_flag=True, help="Check documentation.")
@click.option(
    "--skip-broken-links",
    is_flag=True,
    help="Do not check external links for integrity.",
)
@with_application
def build(application, check, skip_broken_links):
    """Build documentation."""
    padding = "\n" * application.config.verbose

    action = "Building and checking" if check else "Building"
    click.secho(
        f'{padding}{action} "{application.config.source_dir}"...{padding}', fg="blue"
    )

    with exception_handler(exit=True):
        application.build(check=check, skip_broken_links=skip_broken_links)

    message = "All good" if check else "Done"
    click.secho(f"\n{message}.", fg="yellow")


@mudkip.command()
@click.option("-n", "--notebook", is_flag=True, help="Open the Jupyter notebook.")
@click.option("--host", help="Development server host.", default="127.0.0.1")
@click.option("--port", help="Development server port.", default=5500)
@with_application
def develop(application, notebook, host, port):
    """Start development server."""
    padding = "\n" * application.config.verbose

    click.secho(
        f'{padding}Watching "{application.config.source_dir}"...{padding}', fg="blue"
    )

    @contextmanager
    def build_manager(event_batch=None):
        if event_batch is None:
            if application.config.dev_server:
                click.secho(
                    f"{padding}Server running on http://{host}:{port}", fg="blue"
                )
            with exception_handler():
                yield
            return

        now = time.strftime("%H:%M:%S")
        click.secho(f"{padding}{now}", fg="black", bold=True, nl=False)

        events = event_batch.all_events

        if len(events) == 1:
            event = events[0]
            filename = path.basename(event.src_path)
            click.echo(f" {event.event_type} {filename}{padding}")
        else:
            click.echo(f" {len(events)} changes{padding}")

        with exception_handler():
            yield

    try:
        application.develop(notebook, host, port, build_manager)
    except KeyboardInterrupt:
        click.secho("\nExit.", fg="yellow")


@mudkip.command()
@with_application
def test(application):
    """Test documentation."""
    padding = "\n" * application.config.verbose

    click.secho(
        f'{padding}Testing "{application.config.source_dir}"...{padding}', fg="blue"
    )

    with exception_handler(exit=True):
        passed, summary = application.test()

    if not application.config.verbose:
        click.echo("\n" + summary)

    if passed:
        click.secho("\nPassed.", fg="yellow")
    else:
        click.secho("\nFailed.", fg="red", bold=True)
        sys.exit(1)


@mudkip.command()
@with_application
def clean(application):
    """Remove output directory."""
    padding = "\n" * application.config.verbose

    click.secho(f'{padding}Removing "{application.config.output_dir}"...', fg="blue")

    with exception_handler(exit=True):
        application.clean()

    click.secho("\nDone.", fg="yellow")


def main():
    mudkip(prog_name="mudkip")
