import datetime
from copy import deepcopy
from pathlib import Path

import pytest
from freezegun import freeze_time

from arc_to_sqlite import transformers

from . import fixtures


@pytest.mark.parametrize(
    "latitude, longitude, expected_result",
    (("37.7749", "-122.4194", "POINT ( 37.7749 -122.4194 )"),),
)
def test_convert_coordinates_to_wkt(latitude, longitude, expected_result):
    result = transformers.convert_coordinates_to_wkt(
        latitude=latitude,
        longitude=longitude,
    )
    assert result == expected_result


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


@pytest.mark.parametrize(
    "place, expected_result",
    (
        (fixtures.PLACE_ONE, fixtures.TRANSFORMED_PLACE_ONE),
        (fixtures.PLACE_TWO, fixtures.TRANSFORMED_PLACE_TWO),
        (fixtures.PLACE_THREE, fixtures.TRANSFORMED_PLACE_THREE),
    ),
)
def test_transform_place(place, expected_result):
    place = deepcopy(place)
    result = transformers.transform_place(place)
    assert result == expected_result


def test_transform_place__use_spatialite():
    place = deepcopy(fixtures.PLACE_ONE)
    result = transformers.transform_place(place, use_spatialite=True)
    assert (
        result["geometry"]
        == f"POINT ( {place['latitude']} {place['longitude']} )"
    )


@pytest.mark.parametrize(
    "sample, expected_result",
    (
        (fixtures.SAMPLE_ONE, fixtures.TRANSFORMED_SAMPLE_ONE),
        (fixtures.SAMPLE_TWO, fixtures.TRANSFORMED_SAMPLE_TWO),
        (fixtures.SAMPLE_THREE, fixtures.TRANSFORMED_SAMPLE_THREE),
    ),
)
def test_transform_sample(sample, expected_result):
    sample = deepcopy(sample)
    result = transformers.transform_sample(sample)
    assert result == expected_result


def test_transform_sample__use_spatialite():
    sample = deepcopy(fixtures.SAMPLE_ONE)
    result = transformers.transform_sample(sample, use_spatialite=True)
    assert (
        result["geometry"]
        == f"POINT ( {sample['latitude']} {sample['longitude']} )"
    )


@pytest.mark.parametrize(
    "timeline_item, expected_result",
    (
        (fixtures.TIMELINE_ITEM_ONE, fixtures.TRANSFORMED_TIMELINE_ITEM_ONE),
        (fixtures.TIMELINE_ITEM_TWO, fixtures.TRANSFORMED_TIMELINE_ITEM_TWO),
        (
            fixtures.TIMELINE_ITEM_THREE,
            fixtures.TRANSFORMED_TIMELINE_ITEM_THREE,
        ),
        (fixtures.TIMELINE_ITEM_FOUR, fixtures.TRANSFORMED_TIMELINE_ITEM_FOUR),
    ),
)
def test_transform_timeline_item(timeline_item, expected_result):
    timeline_item = deepcopy(timeline_item)
    result = transformers.transform_timeline_item(timeline_item)
    assert result == expected_result


def test_transform_timeline_item__use_spatialite():
    item = deepcopy(fixtures.TIMELINE_ITEM_ONE)
    result = transformers.transform_timeline_item(
        item, use_spatialite=True
    )
    assert (
        result["geometry"]
        == f"POINT ( {item['latitude']} {item['longitude']} )"
    )


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
