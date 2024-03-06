import datetime
import json
import gzip
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional
import hashlib

from sqlite_utils.db import Database, Table
from .transformers import transform_place, transform_timeline_item, transform_sample


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
    timeline_items_table = get_table("timeline_items", db=db)
    samples_table = get_table("samples", db=db)
    places_table = get_table("places", db=db)

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
                "last_saved": "datetime",
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
                "prev_item_id": str,
                "place_id": str,
                "hk_step_count": int,
                "floors_ascended": int,
                "altitude": float,
                "center_latitude": float,
                "center_longitude": float,
                "average_heart_rate": float,
                "street_address": str,
                "last_saved": "datetime",
                "is_visit": bool,
                "manual_place": bool,
                "start_date": "datetime",
                "max_heart_rate": int,
                "step_count": int,
                "end_date": "datetime",
                "floors_descended": int,
                "active_energy_burned": float,
                "radius_sd": float,
                "radius_mean": float,
            },
            pk="item_id",
            foreign_keys=(
                ("next_item_id", "timeline_items", "item_id"),
                ("prev_item_id", "timeline_items", "item_id"),
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
            "prev_item_id",
            "place_id",
            "center_latitude", "center_longitude", "start_date", "end_date"
        ],
    )

    if samples_table.exists() is False:
        samples_table.create(
            columns={
                "sample_id": str,
                "timeline_item_id": str,
                "date": "datetime",
                "recording_state": str,
                "xy_acceleration": float,
                "seconds_from_gmt": int,
                "course_variance": int,
                "last_saved": "datetime",
                "z_acceleration": float,
                "location_speed": float,
                "location_longitude": float,
                "location_altitude": float,
                "location_course": float,
                "location_timestamp": "datetime",
                "location_horizontal_accuracy": float,
                "location_latitude": float,
                "location_vertical_accuracy": float,
                "moving_state": str,
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


def save_places(places: List[Dict[str, Any]], places_table: Table):
    """
    Save the places data to the SQLite database.
    """
    for place in places:
        transform_place(place)

    places_table.upsert_all(places, pk="place_id")


def save_timeline_items(timeline_items: List[Dict[str, Any]], timeline_items_table: Table):
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
    for file in arc_export_path.iterdir():
        if file.suffix == ".json.gz":
            yield file


def load_arc_export_file(file_path: Path) -> Dict[str, Any]:
    """
    Load the Arc export file from the given path.
    """
    with gzip.open(file_path, "rt") as f:
        return json.load(f)
