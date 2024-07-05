import datetime
import gzip
import hashlib
import json
import logging
import typing as t
from copy import deepcopy
from pathlib import Path

from sqlite_utils.db import Database, Table
from sqlite_utils.utils import find_spatialite

from . import errors
from .transformers import (
    transform_arc_export_file_path,
    transform_place,
    transform_sample,
    transform_timeline_item,
)

logger = logging.getLogger(__name__)


def check_spatialite_support() -> bool:
    """
    Check if SpatiaLite is available.
    """
    return find_spatialite() is not None


def open_database(db_file_path: Path, use_spatialite: bool = False) -> Database:
    """
    Open the Arc SQLite database.
    """
    db = Database(db_file_path)

    if use_spatialite:
        db.init_spatialite(find_spatialite())
        logger.info("Spatialite extension loaded.")

    return db


def get_table(table_name: str, db: Database) -> Table:
    """
    Returns a Table from a given db Database object.
    """
    return Table(db=db, name=table_name)


def create_table_indexes(table: Table, indexes: t.List[str]):
    """
    Create indexes for a given table.
    """
    existing_indexes = {tuple(i.columns) for i in table.indexes}

    for index in indexes:
        if (index,) not in existing_indexes:
            table.create_index([index])


def build_database(db: Database, use_spatialite: bool = False):
    """
    Build the Arc Export SQLite database structure.
    """
    arc_export_files_table = get_table("arc_export_files", db=db)
    timeline_items_table = get_table("timeline_items", db=db)
    samples_table = get_table("samples", db=db)
    places_table = get_table("places", db=db)

    if arc_export_files_table.exists() is False:
        arc_export_files_table.create(
            columns={
                "id": int,
                "file_name": str,
                "file_path": str,
                "file_size": int,
                "file_checksum": str,
                "export_type": str,
                "last_processed_at": datetime.datetime,
            },
            pk="id",
        )
        logger.info(f"Created the {arc_export_files_table.name} table.")

    if places_table.exists() is False:
        columns = {
            "place_id": str,
            "name": str,
            "street_address": str,
            "latitude": float,
            "longitude": float,
            "radius_sd": float,
            "radius_mean": float,
            "mapbox_place_id": str,
            "mapbox_category": str,
            "google_place_id": str,
            "google_primary_type": str,
            "seconds_from_gmt": int,
            "last_saved_at": datetime.datetime,
            "arc_export_file_id": int,
            "created_at": datetime.datetime,
            "updated_at": datetime.datetime,
        }

        places_table.create(
            columns=columns,
            pk="place_id",
            foreign_keys=(("arc_export_file_id", "arc_export_files", "id"),),
        )
        places_table.enable_fts(
            ["name", "street_address"], create_triggers=True
        )

        if use_spatialite:
            places_table.add_geometry_column("coordinates", "GEOMETRY")
            places_table.create_spatial_index("coordinates")

        logger.info(f"Created the {places_table.name} table.")

    create_table_indexes(places_table, ["latitude", "longitude"])

    if timeline_items_table.exists() is False:
        columns = {
            "item_id": str,
            "next_item_id": str,
            "previous_item_id": str,
            "place_id": str,
            "starts_at": datetime.datetime,
            "ends_at": datetime.datetime,
            "latitude": float,
            "longitude": float,
            "altitude": float,
            "radius_sd": float,
            "radius_mean": float,
            "step_count": int,
            "hk_step_count": int,
            "floors_ascended": int,
            "floors_descended": int,
            "street_address": str,
            "manual_place": bool,
            "is_visit": bool,
            "average_heart_rate": float,
            "max_heart_rate": int,
            "active_energy_burned": float,
            "activity_type": str,
            "activity_type_confidence_score": float,
            "manual_activity_type": bool,
            "uncertain_activity_type": bool,
            "unknown_activity_type": bool,
            "last_saved_at": datetime.datetime,
            "arc_export_file_id": int,
            "created_at": datetime.datetime,
            "updated_at": datetime.datetime,
        }

        timeline_items_table.create(
            columns=columns,
            pk="item_id",
            foreign_keys=(
                ("next_item_id", "timeline_items", "item_id"),
                ("previous_item_id", "timeline_items", "item_id"),
                ("place_id", "places", "place_id"),
                ("arc_export_file_id", "arc_export_files", "id"),
            ),
        )
        timeline_items_table.enable_fts(
            ["street_address"], create_triggers=True
        )

        if use_spatialite:
            timeline_items_table.add_geometry_column("coordinates", "GEOMETRY")
            timeline_items_table.add_geometry_column("samples_path", "GEOMETRY")

            timeline_items_table.create_spatial_index("coordinates")
            timeline_items_table.create_spatial_index("samples_path")

        logger.info(f"Created the {timeline_items_table.name} table.")

    create_table_indexes(
        timeline_items_table,
        [
            "next_item_id",
            "previous_item_id",
            "place_id",
            "latitude",
            "longitude",
            "starts_at",
            "ends_at",
        ],
    )

    if samples_table.exists() is False:
        samples_table.create(
            columns={
                "sample_id": str,
                "timeline_item_id": str,
                "taken_at": datetime.datetime,
                "latitude": float,
                "longitude": float,
                "altitude": float,
                "recording_state": str,
                "moving_state": str,
                "xy_acceleration": float,
                "z_acceleration": float,
                "course": float,
                "course_variance": int,
                "speed": float,
                "horizontal_accuracy": float,
                "vertical_accuracy": float,
                "step_hz": float,
                "seconds_from_gmt": int,
                "last_saved_at": datetime.datetime,
                "arc_export_file_id": int,
                "created_at": datetime.datetime,
                "updated_at": datetime.datetime,
            },
            pk="sample_id",
            foreign_keys=(
                ("timeline_item_id", "timeline_items", "item_id"),
                ("arc_export_file_id", "arc_export_files", "id"),
            ),
        )

        if use_spatialite:
            samples_table.add_geometry_column("coordinates", "GEOMETRY")
            samples_table.create_spatial_index("coordinates")

        logger.info(f"Created the {samples_table.name} table.")

    create_table_indexes(
        samples_table,
        indexes=["timeline_item_id", "taken_at", "longitude", "latitude"],
    )


def update_or_insert(
    table: Table,
    *,
    conversions: t.Optional[t.Dict[str, str]] = None,
    defaults: t.Optional[t.Dict[str, t.Any]] = None,
    create_defaults: t.Optional[t.Dict[str, t.Any]] = None,
    **kwargs,
) -> Table:
    """
    Update or insert a row in a SQLite table.
    """
    defaults = defaults or {}
    create_defaults = create_defaults or {}

    existing_rows = table.pks_and_rows_where(
        where=" AND ".join(f"{k} = :{k}" for k in kwargs),
        where_args=kwargs,
    )
    row_pk, _ = next(existing_rows, (None, None))

    # Check if there are multiple rows for the given query.
    try:
        next(existing_rows)
        raise errors.UpdateOrInsertError(
            "Failed to update or insert the row because multiple rows match query were found."
        )
    except StopIteration:
        ...

    if row_pk is not None:
        return table.update(
            pk_values=row_pk,
            updates={**defaults, **kwargs},
            conversions=conversions,
        )

    return table.insert(
        record={**kwargs, **defaults, **create_defaults},
        conversions=conversions,
    )


def get_arc_export_file_path(
    arc_root_dir: Path,
    export_type: t.Literal["daily", "monthly"] = "daily",
) -> Path:
    """
    Get the Arc export file path for the given export type.
    """
    arc_json_export_path = arc_root_dir / "Documents/Export/JSON"

    if export_type == "monthly":
        arc_json_export_path = arc_json_export_path / "Monthly"
    else:
        arc_json_export_path = arc_json_export_path / "Daily"

    if arc_json_export_path.exists() is False:
        raise errors.ArcExportPathNotFoundError(
            f"Directory {arc_json_export_path} does not exist."
        )

    return arc_json_export_path


def calculate_file_obj_checksum(file_obj: t.BinaryIO) -> str:
    """
    Calculate the checksum of a file.
    """
    file_hash = hashlib.sha256()
    while chunk := file_obj.read(8192):
        file_hash.update(chunk)

    return file_hash.hexdigest()


def get_arc_export_file_row(
    file_name: str, table: Table
) -> t.Union[t.Tuple[int, t.Dict[str, t.Any]], None]:
    """
    Get the Arc export file metadata from the SQLite database.
    """
    try:
        pk, row = next(
            table.pks_and_rows_where(
                where="file_name = :file_name",
                where_args={"file_name": file_name},
            )
        )
    except StopIteration:
        return None

    return pk, row


def save_arc_export_file(
    path: Path,
    file_checksum: str,
    row_id: t.Union[int, None],
    table: Table,
) -> Table:
    """
    Save the Arc export file metadata to the SQLite database.
    """
    data = transform_arc_export_file_path(
        path=path,
        file_checksum=file_checksum,
    )

    # Insert or update the file metadata.
    if row_id is None:
        return table.insert(data)
    return table.update(row_id, data)


def save_places(
    places: t.List[t.Dict[str, t.Any]],
    arc_export_file_id: int,
    places_table: Table,
    use_spatialite: bool = False,
):
    """
    Save the places data to the SQLite database.
    """
    conversions = {}
    if use_spatialite:
        conversions["coordinates"] = "GeomFromText(?, 4326)"

    for place in places:
        transform_place(place, use_spatialite=use_spatialite)
        place_id = place.pop("place_id")

        place["update_at"] = datetime.datetime.utcnow()

        update_or_insert(
            table=places_table,
            conversions=conversions,
            defaults=place,
            create_defaults={
                "arc_export_file_id": arc_export_file_id,
                "created_at": datetime.datetime.utcnow(),
            },
            place_id=place_id,
        )


def save_timeline_items(
    timeline_items: t.List[t.Dict[str, t.Any]],
    arc_export_file_id: int,
    timeline_items_table: Table,
    use_spatialite: bool = False,
):
    """
    Save the timeline items data to the SQLite database.
    """
    conversions = {}
    if use_spatialite:
        conversions["coordinates"] = "GeomFromText(?, 4326)"
        conversions["samples_path"] = "GeomFromText(?, 4326)"

    for item in timeline_items:
        transform_timeline_item(item, use_spatialite=use_spatialite)
        item["arc_export_file_id"] = arc_export_file_id

    timeline_items_table.upsert_all(
        timeline_items, pk="item_id", conversions=conversions
    )


def save_samples(
    samples: t.List[t.Dict[str, t.Any]],
    arc_export_file_id: int,
    samples_table: Table,
    use_spatialite: bool = False,
):
    """
    Save the samples data to the SQLite database.
    """
    for sample in samples:
        transform_sample(sample, use_spatialite=use_spatialite)
        sample["arc_export_file_id"] = arc_export_file_id

    conversions = {}
    if use_spatialite:
        conversions["coordinates"] = "GeomFromText(?, 4326)"

    samples_table.upsert_all(samples, pk="sample_id", conversions=conversions)


def list_arc_export_files(
    arc_export_path: Path,
) -> t.Generator[Path, None, None]:
    """
    List the Arc export files in the given directory.
    """
    for file_path in arc_export_path.iterdir():
        if file_path.suffixes == [".json", ".gz"]:
            yield file_path


def extract_places_and_samples_from_timeline_items(
    timeline_items: t.List[t.Dict[str, t.Any]],
) -> t.Tuple[
    t.List[t.Dict[str, t.Any]],
    t.List[t.Dict[str, t.Any]],
    t.List[t.Dict[str, t.Any]],
]:
    """
    Extract places and samples from the timeline items.
    """
    places = []
    samples = []

    for item in timeline_items:
        # Extract places from the timeline item.
        try:
            places.append(item.pop("place"))
        except KeyError:
            ...

        # Extract samples from the timeline item.
        samples.extend(deepcopy(item["samples"]))

    return timeline_items, places, samples


def process_arc_export_file(
    db: Database, file_path: Path, use_spatialite: bool = False
):
    """
    Process an Arc export file and save the data to the SQLite database.
    """
    arc_export_files_table = get_table("arc_export_files", db=db)

    # Calculate the checksum of the file and save the file metadata to the
    # database.
    with file_path.open("rb") as file_obj:
        file_checksum = calculate_file_obj_checksum(file_obj)

    # Check if the file has already been processed.
    arc_export_file_values = get_arc_export_file_row(
        file_path.name, arc_export_files_table
    )
    if arc_export_file_values is not None:
        arc_export_file_row_id, arc_export_file_data = arc_export_file_values

        # If the file checksum is the same, we don't need to process it again.
        if arc_export_file_data["file_checksum"] == file_checksum:
            logger.info(
                f"Skipping file {file_path.name} because it has already been processed."
            )
            return
    else:
        arc_export_file_row_id = None

    arc_export_files_table = save_arc_export_file(
        file_path,
        file_checksum=file_checksum,
        row_id=arc_export_file_row_id,
        table=arc_export_files_table,
    )
    arc_export_file_row_id = arc_export_files_table.last_pk
    if arc_export_file_row_id is None:
        raise errors.ArcExportFilesRowFailedError(
            "The arc_export_files row failed to save to the database."
        )

    # Load the Arc export data and save it to the database.
    with gzip.open(file_path, "rb") as file_obj:
        timeline_items = json.load(file_obj)["timelineItems"]

    timeline_items, places, samples = (
        extract_places_and_samples_from_timeline_items(timeline_items)
    )

    places_table = get_table("places", db=db)
    timeline_items_table = get_table("timeline_items", db=db)
    samples_table = get_table("samples", db=db)

    save_places(
        places,
        arc_export_file_id=arc_export_file_row_id,
        places_table=places_table,
        use_spatialite=use_spatialite,
    )
    save_timeline_items(
        timeline_items,
        arc_export_file_id=arc_export_file_row_id,
        timeline_items_table=timeline_items_table,
        use_spatialite=use_spatialite,
    )
    save_samples(
        samples,
        arc_export_file_id=arc_export_file_row_id,
        samples_table=samples_table,
        use_spatialite=use_spatialite,
    )
