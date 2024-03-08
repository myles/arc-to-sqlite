from copy import deepcopy

import pytest

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
        "street_address": place["streetAddress"],
        "name": place["name"],
        "last_saved": place["lastSaved"],
        "seconds_from_gmt": place["secondsFromGMT"],
        "center_latitude": place["center"]["latitude"],
        "center_longitude": place["center"]["longitude"],
        "radius_sd": place["radius"]["sd"],
        "radius_mean": place["radius"]["mean"],
    }


def test_transform_sample():
    sample = deepcopy(fixtures.SAMPLE_ONE)
    result = transformers.transform_sample(fixtures.SAMPLE_ONE)
    assert result == {
        "sample_id": fixtures.SAMPLE_ONE_ID,
        "timeline_item_id": fixtures.TIMELINE_ITEM_ONE_ID,
        "step_hz": sample["stepHz"],
        "date": sample["date"],
        "recording_state": sample["recordingState"],
        "xy_acceleration": sample["xyAcceleration"],
        "seconds_from_gmt": sample["secondsFromGMT"],
        "course_variance": sample["courseVariance"],
        "last_saved": sample["lastSaved"],
        "z_acceleration": sample["zAcceleration"],
        "location_speed": sample["location"]["speed"],
        "location_longitude": sample["location"]["longitude"],
        "location_altitude": sample["location"]["altitude"],
        "location_course": sample["location"]["course"],
        "location_timestamp": sample["location"]["timestamp"],
        "location_horizontal_accuracy": sample["location"][
            "horizontalAccuracy"
        ],
        "location_latitude": sample["location"]["latitude"],
        "location_vertical_accuracy": sample["location"]["verticalAccuracy"],
        "moving_state": sample["movingState"],
    }


def test_transform_timeline_item():
    timeline_item = deepcopy(fixtures.TIMELINE_ITEM_ONE)
    result = transformers.transform_timeline_item(fixtures.TIMELINE_ITEM_ONE)
    assert result == {
        "item_id": fixtures.TIMELINE_ITEM_ONE_ID,
        "place_id": fixtures.PLACE_ONE_ID,
        "hk_step_count": timeline_item["hkStepCount"],
        "floors_ascended": timeline_item["floorsAscended"],
        "altitude": timeline_item["altitude"],
        "center_latitude": timeline_item["center"]["latitude"],
        "center_longitude": timeline_item["center"]["longitude"],
        "average_heart_rate": timeline_item["averageHeartRate"],
        "street_address": timeline_item["streetAddress"],
        "last_saved": timeline_item["lastSaved"],
        "is_visit": timeline_item["isVisit"],
        "manual_place": timeline_item["manualPlace"],
        "start_date": timeline_item["startDate"],
        "max_heart_rate": timeline_item["maxHeartRate"],
        "step_count": timeline_item["stepCount"],
        "next_item_id": timeline_item["nextItemId"],
        "end_date": timeline_item["endDate"],
        "radius_mean": timeline_item["radius"]["mean"],
        "radius_sd": timeline_item["radius"]["sd"],
        "previous_item_id": timeline_item["previousItemId"],
        "floors_descended": timeline_item["floorsDescended"],
        "active_energy_burned": timeline_item["activeEnergyBurned"],
    }
