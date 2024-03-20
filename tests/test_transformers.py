import datetime
from copy import deepcopy
from pathlib import Path

import pytest
from freezegun import freeze_time

from arc_to_sqlite import transformers

from . import fixtures


@pytest.mark.parametrize(
    "name, expected_result",
    (
        ("streetAddress", "street_address"),
        ("street_address", "street_address"),
        ("nameWithACRONYM", "name_with_acronym"),
        ("1Abc2", "1_abc2"),
    ),
)
def test_convert_to_snake_case(name, expected_result):
    result = transformers.convert_to_snake_case(name)
    assert result == expected_result


def test_transform_place():
    place = deepcopy(fixtures.PLACE_ONE)
    result = transformers.transform_place(fixtures.PLACE_ONE)
    assert result == {
        "place_id": fixtures.PLACE_ONE_ID,
        "name": place["name"],
        "street_address": place["streetAddress"],
        "latitude": place["center"]["latitude"],
        "longitude": place["center"]["longitude"],
        "radius_sd": place["radius"]["sd"],
        "radius_mean": place["radius"]["mean"],
        "last_saved_at": place["lastSaved"],
        "seconds_from_gmt": place["secondsFromGMT"],
    }


def test_transform_sample():
    sample = deepcopy(fixtures.SAMPLE_ONE)
    result = transformers.transform_sample(fixtures.SAMPLE_ONE)
    assert result == {
        "sample_id": fixtures.SAMPLE_ONE_ID,
        "timeline_item_id": fixtures.TIMELINE_ITEM_ONE_ID,
        "step_hz": sample["stepHz"],
        "taken_at": sample["date"],
        "recording_state": sample["recordingState"],
        "xy_acceleration": sample["xyAcceleration"],
        "seconds_from_gmt": sample["secondsFromGMT"],
        "course_variance": sample["courseVariance"],
        "last_saved_at": sample["lastSaved"],
        "z_acceleration": sample["zAcceleration"],
        "speed": sample["location"]["speed"],
        "longitude": sample["location"]["longitude"],
        "altitude": sample["location"]["altitude"],
        "course": sample["location"]["course"],
        "horizontal_accuracy": sample["location"]["horizontalAccuracy"],
        "latitude": sample["location"]["latitude"],
        "vertical_accuracy": sample["location"]["verticalAccuracy"],
        "moving_state": sample["movingState"],
    }


def test_transform_sample__no_location():
    sample = deepcopy(fixtures.SAMPLE_TWO)

    result = transformers.transform_sample(sample)
    assert "speed" not in result
    assert "longitude" not in result
    assert "altitude" not in result
    assert "course" not in result
    assert "timestamp" not in result
    assert "horizontal_accuracy" not in result
    assert "latitude" not in result
    assert "vertical_accuracy" not in result


def test_transform_timeline_item():
    timeline_item = deepcopy(fixtures.TIMELINE_ITEM_ONE)
    result = transformers.transform_timeline_item(fixtures.TIMELINE_ITEM_ONE)
    assert result == {
        "item_id": fixtures.TIMELINE_ITEM_ONE_ID,
        "place_id": fixtures.PLACE_ONE_ID,
        "hk_step_count": timeline_item["hkStepCount"],
        "floors_ascended": timeline_item["floorsAscended"],
        "altitude": timeline_item["altitude"],
        "latitude": timeline_item["center"]["latitude"],
        "longitude": timeline_item["center"]["longitude"],
        "average_heart_rate": timeline_item["averageHeartRate"],
        "street_address": timeline_item["streetAddress"],
        "last_saved_at": timeline_item["lastSaved"],
        "is_visit": timeline_item["isVisit"],
        "manual_place": timeline_item["manualPlace"],
        "starts_at": timeline_item["startDate"],
        "max_heart_rate": timeline_item["maxHeartRate"],
        "step_count": timeline_item["stepCount"],
        "next_item_id": timeline_item["nextItemId"],
        "ends_at": timeline_item["endDate"],
        "radius_mean": timeline_item["radius"]["mean"],
        "radius_sd": timeline_item["radius"]["sd"],
        "previous_item_id": timeline_item["previousItemId"],
        "floors_descended": timeline_item["floorsDescended"],
        "active_energy_burned": timeline_item["activeEnergyBurned"],
    }


def test_transform_timeline_item__no_center_and_radius():
    timeline_item = deepcopy(fixtures.TIMELINE_ITEM_TWO)

    result = transformers.transform_timeline_item(timeline_item)
    assert "latitude" not in result
    assert "longitude" not in result
    assert "radius_mean" not in result
    assert "radius_sd" not in result


@freeze_time("2024-01-01")
@pytest.mark.parametrize(
    "path, expected_file_checksum, expected_export_type",
    (
        (
            Path("/path/to/arc_export/Monthly/2024-01.json.gz"),
            "12345678901234567890",
            "monthly",
        ),
        (
            Path("/path/to/arc_export/Daily/2024-01-01.json.gz"),
            "1234567890",
            "daily",
        ),
    ),
)
def test_transform_arc_export_file_path(
    path,
    expected_file_checksum,
    expected_export_type,
    mocker,
):
    expected_file_size = 1234
    expected_last_processed_at = datetime.datetime.now(tz=datetime.timezone.utc)

    mocker.patch(
        "arc_to_sqlite.transformers.Path.stat",
        return_value=mocker.Mock(st_size=expected_file_size),
    )

    result = transformers.transform_arc_export_file_path(
        path,
        file_checksum=expected_file_checksum,
    )
    assert result == {
        "file_name": path.name,
        "file_path": str(path.absolute()),
        "file_size": expected_file_size,
        "file_checksum": expected_file_checksum,
        "export_type": expected_export_type,
        "last_processed_at": expected_last_processed_at,
    }
