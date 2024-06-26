from pathlib import Path
from typing import Literal

import click

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
def cli(
    db_path: str,
    arc_root_dir: str,
    export_type: Literal["daily", "monthly"] = "daily",
):
    """
    Save data from Arc's export to a SQLite database.
    """
    # Open the SQLite database and build the database structure.
    db = service.open_database(Path(db_path))
    service.build_database(db)

    # Get the Arc export path for the given export type.
    arc_json_export_path = Path(arc_root_dir) / "Documents/Export/JSON"

    if export_type == "monthly":
        arc_export_path = arc_json_export_path / "Monthly"
    else:
        arc_export_path = arc_json_export_path / "Daily"

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
            service.process_arc_export_file(db, arc_export_file_path)
