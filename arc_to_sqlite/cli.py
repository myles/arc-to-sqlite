from pathlib import Path
from typing import Literal

import click

from .errors import ArcToSqliteError
from . import service


@click.command()
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument(
    "arc_root_dir",
    type=click.Path(
        file_okay=False, dir_okay=True, allow_dash=True, exists=True
    ),
    required=True,
)
@click.option(
    "--export-type",
    type=click.Choice(["daily", "monthly"]),
    default="daily",
)
@click.option("--spatialite", is_flag=True, help="Enable SpatiaLite support.")
def cli(
    db_path: str,
    arc_root_dir: str,
    export_type: Literal["daily", "monthly"] = "daily",
    spatialite: bool = False,
):
    """
    Save data from Arc's export to a SQLite database.
    """
    # If spatialite is enabled, we need to ensure the SpatiaLite extension is
    # available.
    if spatialite is True and service.check_spatialite_support() is False:
        raise click.ClickException(
            "SpatiaLite support is not available. Please ensure the SpatiaLite"
            " extension is installed and available in the system PATH."
        )

    # Open the SQLite database and build the database structure.
    db = service.open_database(Path(db_path), use_spatialite=spatialite)
    service.build_database(db, use_spatialite=spatialite)

    # Get the path to the Arc export directory.
    try:
        arc_export_path = service.get_arc_export_file_path(
            Path(arc_root_dir),
            export_type,
        )
    except ArcToSqliteError as error:
        raise click.ClickException(error.message)

    # Get the list of export files and process them.
    # Transforming this from a generator to a list, so we can sort it and show
    # a progress bar.
    arc_export_file_paths = list(service.list_arc_export_files(arc_export_path))
    arc_export_file_paths = sorted(arc_export_file_paths, key=lambda p: p.name)

    with click.progressbar(
        arc_export_file_paths,
        label=f"Processing {export_type} export files",
    ) as bar:
        for arc_export_file_path in bar:
            try:
                service.process_arc_export_file(
                    db=db, file_path=arc_export_file_path, use_spatialite=spatialite
                )
            except ArcToSqliteError as error:
                raise click.ClickException(error.message)
