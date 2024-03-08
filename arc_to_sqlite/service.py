import datetime
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any, BinaryIO, Dict, Generator, List, Tuple, Union

from sqlite_utils.db import Database, Table

from .transformers import (
    transform_arc_export_file_path,
    transform_place,
    transform_sample,
    transform_timeline_item,
)


def open_database(db_file_path: Path) -> Database:
    """
    Open the Mastodon SQLite database.
    """
    return Database(db_file_path)


def get_table(table_name: str, db: Database) -> Table:
    """
    Returns a Table from a given db Database object.
    """
    return Table(db=db, name=table_name)


def create_table_indexes(table: Table, indexes: List[str]):
    """
    Create indexes for a given table.
    """
    existing_indexes = {tuple(i.columns) for i in table.indexes}

    for index in indexes:
        if (index,) not in existing_indexes:
            table.create_index([index])


def build_database(db: Database):
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

    if places_table.exists() is False:
        places_table.create(
            columns={
                "place_id": str,
                "name": str,
                "street_address": str,
                "center_latitude": float,
                "center_longitude": float,
                "radius_sd": float,
                "radius_mean": float,
                "seconds_from_gmt": int,
                "last_saved": datetime.datetime,
            },
            pk="place_id",
        )
        places_table.enable_fts(
            ["name", "street_address"], create_triggers=True
        )

    create_table_indexes(places_table, ["center_latitude", "center_longitude"])

    if timeline_items_table.exists() is False:
        timeline_items_table.create(
            columns={
                "item_id": str,
                "next_item_id": str,
                "previous_item_id": str,
                "place_id": str,
                "hk_step_count": int,
                "floors_ascended": int,
                "altitude": float,
                "center_latitude": float,
                "center_longitude": float,
                "average_heart_rate": float,
                "street_address": str,
                "last_saved": datetime.datetime,
                "is_visit": bool,
                "manual_place": bool,
                "start_date": datetime.datetime,
                "max_heart_rate": int,
                "step_count": int,
                "end_date": datetime.datetime,
                "floors_descended": int,
                "active_energy_burned": float,
                "radius_sd": float,
                "radius_mean": float,
            },
            pk="item_id",
            foreign_keys=(
                ("next_item_id", "timeline_items", "item_id"),
                ("previous_item_id", "timeline_items", "item_id"),
                ("place_id", "places", "place_id"),
            ),
        )
        timeline_items_table.enable_fts(
            ["street_address"], create_triggers=True
        )

    create_table_indexes(
        timeline_items_table,
        [
            "next_item_id",
            "previous_item_id",
            "place_id",
            "center_latitude",
            "center_longitude",
            "start_date",
            "end_date",
        ],
    )

    if samples_table.exists() is False:
        samples_table.create(
            columns={
                "sample_id": str,
                "timeline_item_id": str,
                "date": datetime.datetime,
                "recording_state": str,
                "xy_acceleration": float,
                "seconds_from_gmt": int,
                "course_variance": int,
                "last_saved": datetime.datetime,
                "z_acceleration": float,
                "location_speed": float,
                "location_longitude": float,
                "location_altitude": float,
                "location_course": float,
                "location_timestamp": datetime.datetime,
                "location_horizontal_accuracy": float,
                "location_latitude": float,
                "location_vertical_accuracy": float,
                "moving_state": str,
                "step_hz": float,
            },
            pk="sample_id",
            foreign_keys=(("timeline_item_id", "timeline_items", "item_id"),),
        )

    create_table_indexes(
        samples_table,
        [
            "timeline_item_id",
            "date",
            "location_longitude",
            "location_latitude",
        ],
    )


def calculate_file_obj_checksum(file_obj: BinaryIO) -> str:
    """
    Calculate the checksum of a file.
    """
    file_hash = hashlib.sha256()
    while chunk := file_obj.read(8192):
        file_hash.update(chunk)

    return file_hash.hexdigest()


def get_arc_export_file_row(
    file_name: str, table: Table
) -> Union[Tuple[int, Dict[str, Any]], None]:
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
    row_id: Union[int, None],
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


def save_places(places: List[Dict[str, Any]], places_table: Table):
    """
    Save the places data to the SQLite database.
    """
    for place in places:
        transform_place(place)

    places_table.upsert_all(places, pk="place_id")


def save_timeline_items(
    timeline_items: List[Dict[str, Any]], timeline_items_table: Table
):
    """
    Save the timeline items data to the SQLite database.
    """
    for item in timeline_items:
        transform_timeline_item(item)

    timeline_items_table.upsert_all(timeline_items, pk="item_id")


def save_samples(samples: List[Dict[str, Any]], samples_table: Table):
    """
    Save the samples data to the SQLite database.
    """
    for sample in samples:
        transform_sample(sample)

    samples_table.upsert_all(samples, pk="sample_id")


def list_arc_export_files(arc_export_path: Path) -> Generator[Path, None, None]:
    """
    List the Arc export files in the given directory.
    """
    for file_path in arc_export_path.iterdir():
        if file_path.suffixes == [".json", ".gz"]:
            yield file_path


def extract_places_and_samples_from_timeline_items(
    timeline_items: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Extract places and samples from the timeline items.
    """
    places = []
    samples = []

    for item in timeline_items:
        try:
            places.append(item.pop("place"))
        except KeyError:
            ...

        samples.extend(item.pop("samples"))

    return timeline_items, places, samples


def process_arc_export_file(db: Database, file_path: Path):
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

        if arc_export_file_data["file_checksum"] == file_checksum:
            return
    else:
        arc_export_file_row_id = None

    save_arc_export_file(
        file_path,
        file_checksum=file_checksum,
        row_id=arc_export_file_row_id,
        table=arc_export_files_table,
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

    save_places(places, places_table)
    save_timeline_items(timeline_items, timeline_items_table)
    save_samples(samples, samples_table)
