from pathlib import Path

import click

from . import service


@click.command()
@click.version_option()
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument(
    "arc_export_path",
    type=click.Path(
        file_okay=False, dir_okay=True, allow_dash=True, exists=True
    ),
    help="Path to the directory containing the Arc export files.",
)
def cli(db_path: Path, arc_export_path: Path):
    """
    Save data from Arc's export to a SQLite database.
    """
