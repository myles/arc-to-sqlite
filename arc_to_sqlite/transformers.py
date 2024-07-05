import datetime
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from shapely import Point, LineString


def convert_coordinates_to_wkt_point(*, latitude: str, longitude: str) -> str:
    """
    Convert a latitude and longitude to a Well-Known Text (WKT) string.
    """
    return Point(float(latitude), float(longitude)).wkt


def convert_samples_to_wkt_line_string(samples: List[Dict[str, Any]]) -> Optional[str]:
    """
    Convert the latitude and longitude of a sample to a Well-Known Text (WKT)
    string.
    """
    # Filter out any samples that do not have a location or latitude and
    # longitude.
    samples = [
        sample
        for sample in samples
        if sample.get("location") and sample["location"].get("latitude") and sample["location"].get("longitude")
    ]

    # If there is less than one sample, return None, as a LineString requires
    # at least two points.
    if len(samples) <= 1:
        return None

    points = [
        Point(float(sample["location"]["latitude"]), float(sample["location"]["longitude"]))
        for sample in samples
    ]
    return LineString(points).wkt


def convert_to_snake_case(name: str) -> str:
    """
    Convert a string to snake_case.

    - Adapted from this StackOverflow response:
      http://stackoverflow.com/a/1176023/1072990
    """
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def transform_place(place: Dict[str, Any], use_spatialite: bool = False):
    """
    Transform the place data from the Arc JSON to the SQLite schema.
    """
    place["last_saved_at"] = place.pop("lastSaved")

    radius = place.pop("radius")
    for key, value in radius.items():
        place[f"radius_{convert_to_snake_case(key)}"] = value

    center = place.pop("center")
    for key, value in center.items():
        place[convert_to_snake_case(key)] = value

    # Convert the keys to snake_case
    to_convert = [
        k
        for k in place.keys()
        if k
        in (
            "placeId",
            "streetAddress",
            "secondsFromGMT",
            "mapboxCategory",
            "mapboxPlaceId",
            "googlePrimaryType",
            "googlePlaceId",
        )
    ]
    for key in to_convert:
        if key in place:
            place[convert_to_snake_case(key)] = place.pop(key)

    # Remove any keys that are not in the schema
    to_remove = [
        k
        for k in place.keys()
        if k
        not in (
            "place_id",
            "name",
            "street_address",
            "latitude",
            "longitude",
            "radius_sd",
            "radius_mean",
            "seconds_from_gmt",
            "last_saved_at",
            "mapbox_category",
            "mapbox_place_id",
            "google_primary_type",
            "google_place_id",
        )
    ]
    for key in to_remove:
        place.pop(key)

    if use_spatialite and "latitude" in place and "longitude" in place:
        place["coordinates"] = convert_coordinates_to_wkt_point(
            latitude=place["latitude"], longitude=place["longitude"]
        )

    return place


def transform_sample(sample: Dict[str, Any], use_spatialite: bool = False):
    """
    Transform the sample data from the Arc JSON to the SQLite schema.
    """
    sample["taken_at"] = sample.pop("date")
    sample["last_saved_at"] = sample.pop("lastSaved")

    # Extract the location data
    location = sample.pop("location", None) or {}
    location.pop("timestamp", None)
    for key, value in location.items():
        sample[convert_to_snake_case(key)] = value

    # Convert the keys to snake_case
    to_convert = [
        "courseVariance",
        "zAcceleration",
        "secondsFromGMT",
        "sampleId",
        "movingState",
        "xyAcceleration",
        "recordingState",
        "stepHz",
        "timelineItemId",
    ]
    for key in to_convert:
        if key not in sample:
            continue

        sample[convert_to_snake_case(key)] = sample.pop(key)

    # Remove any keys that are not in the schema
    to_remove = [
        k
        for k in sample.keys()
        if k
        not in (
            "latitude",
            "longitude",
            "speed",
            "timestamp",
            "horizontal_accuracy",
            "vertical_accuracy",
            "altitude",
            "course",
            "horizontal_accuracy",
            "vertical_accuracy",
            "speed",
            "longitude",
            "latitude",
            "seconds_from_gmt",
            "sample_id",
            "moving_state",
            "xy_acceleration",
            "recording_state",
            "step_hz",
            "timeline_item_id",
            "course_variance",
            "z_acceleration",
            "last_saved_at",
            "taken_at",
        )
    ]
    for key in to_remove:
        if key not in sample:
            continue

        sample.pop(key)

    if use_spatialite and "latitude" in sample and "longitude" in sample:
        sample["coordinates"] = convert_coordinates_to_wkt_point(
            latitude=sample["latitude"], longitude=sample["longitude"]
        )

    return sample


def transform_timeline_item(
    timeline_item: Dict[str, Any], use_spatialite: bool = False
):
    """
    Transform the timeline item data from the Arc JSON to the SQLite schema.
    """
    timeline_item["last_saved_at"] = timeline_item.pop("lastSaved")
    timeline_item["starts_at"] = timeline_item.pop("startDate")
    timeline_item["ends_at"] = timeline_item.pop("endDate")

    center = timeline_item.pop("center", None) or {}
    for key, value in center.items():
        timeline_item[convert_to_snake_case(key)] = value

    radius = timeline_item.pop("radius", None) or {}
    for key, value in radius.items():
        timeline_item[f"radius_{convert_to_snake_case(key)}"] = value

    samples = timeline_item.pop("samples", [])

    # Convert the keys to snake_case
    to_convert = [
        "hkStepCount",
        "floorsAscended",
        "altitude",
        "averageHeartRate",
        "streetAddress",
        "isVisit",
        "manualPlace",
        "maxHeartRate",
        "stepCount",
        "nextItemId",
        "placeId",
        "previousItemId",
        "floorsDescended",
        "activeEnergyBurned",
        "itemId",
        "activityType",
        "activityTypeConfidenceScore",
        "manualActivityType",
        "uncertainActivityType",
        "unknownActivityType",
    ]
    for key in to_convert:
        if key not in timeline_item:
            continue

        timeline_item[convert_to_snake_case(key)] = timeline_item.pop(key)

    # Remove any keys that are not in the schema
    to_remove = [
        k
        for k in timeline_item.keys()
        if k
        not in (
            "latitude",
            "longitude",
            "radius_sd",
            "radius_mean",
            "hk_step_count",
            "floors_ascended",
            "altitude",
            "average_heart_rate",
            "street_address",
            "last_saved_at",
            "is_visit",
            "manual_place",
            "starts_at",
            "max_heart_rate",
            "step_count",
            "next_item_id",
            "ends_at",
            "place_id",
            "previous_item_id",
            "floors_descended",
            "active_energy_burned",
            "item_id",
            "last_saved_at",
            "activity_type",
            "activity_type_confidence_score",
            "manual_activity_type",
            "uncertain_activity_type",
            "unknown_activity_type",
        )
    ]
    for key in to_remove:
        timeline_item.pop(key)

    if use_spatialite:
        if "latitude" in timeline_item and "longitude" in timeline_item:
            timeline_item["coordinates"] = convert_coordinates_to_wkt_point(
                latitude=timeline_item["latitude"],
                longitude=timeline_item["longitude"],
            )

        if samples:
            timeline_item["samples_path"] = convert_samples_to_wkt_line_string(samples)

    return timeline_item


def transform_arc_export_file_path(
    path: Path,
    file_checksum: str,
) -> Dict[str, Any]:
    """
    Transform an Arc export file path into a dictionary of values that can be
    safely inserted into the arc_export_files table.
    """
    # Determine the export type based on the file name.
    file_basename = path.name.split(".")[0]

    if re.match(r"^\d{4}-\d{2}$", file_basename):
        export_type = "monthly"
    elif re.match(r"^\d{4}-\d{2}-\d{2}$", file_basename):
        export_type = "daily"
    else:
        raise ValueError(f"Unrecognized export file name: {path.name}")

    return {
        "file_name": path.name,
        "file_path": str(path.absolute()),
        "file_size": path.stat().st_size,
        "file_checksum": file_checksum,
        "export_type": export_type,
        "last_processed_at": datetime.datetime.now(tz=datetime.timezone.utc),
    }
