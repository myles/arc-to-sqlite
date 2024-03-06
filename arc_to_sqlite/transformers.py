import re
from typing import Any, Dict


CAMEL_CASE_TO_SNAKE_CASE = re.compile(r'(?<!^)(?=[A-Z])')

def convert_to_snake_case(name: str) -> str:
    """
    Convert a string to snake_case.
    """
    return CAMEL_CASE_TO_SNAKE_CASE.sub('_', name).lower()


def transform_place(place: Dict[str, Any]):
    """
    Transform the place data from the Arc JSON to the SQLite schema.
    """
    radius = place.pop('radius')
    for key, value in radius.items():
        place[f'radius_{convert_to_snake_case(key)}'] = value

    center = place.pop('center')
    for key, value in center.items():
        place[f'center_{convert_to_snake_case(key)}'] = value

    # Convert the keys to snake_case
    to_convert = ['streetAddress', 'lastSaved', 'placeId', 'secondsFromGMT']
    for key in to_convert:
        place[convert_to_snake_case(key)] = place.pop(key)

    # Remove any keys that are not in the schema
    to_remove = [
        k for k in place.keys()
        if k not in ('name', 'street_address', 'center_latitude', 'center_longitude', 'radius_sd', 'radius_mean', 'seconds_from_gmt', 'last_saved')
    ]
    for key in to_remove:
        place.pop(key)

    return place


def transform_timeline_item(timeline_item: Dict[str, Any]):
    """
    Transform the timeline item data from the Arc JSON to the SQLite schema.
    """
    center = timeline_item.pop('center')
    for key, value in center.items():
        timeline_item[f'center_{convert_to_snake_case(key)}'] = value

    # Convert the keys to snake_case
    to_convert = ['hkStepCount', 'floorsAscended', 'altitude', 'averageHeartRate', 'streetAddress', 'lastSaved', 'isVisit', 'manualPlace', 'startDate', 'maxHeartRate', 'stepCount', 'nextItemId', 'endDate', 'placeId', 'previousItemId', 'floorsDescended', 'activeEnergyBurned', 'itemId']
    for key in to_convert:
        timeline_item[convert_to_snake_case(key)] = timeline_item.pop(key)

    # Remove any keys that are not in the schema
    to_remove = [
        k for k in timeline_item.keys()
        if k not in ('center_latitude', 'center_longitude', 'hk_step_count', 'floors_ascended', 'altitude', 'average_heart_rate', 'street_address', 'last_saved', 'is_visit', 'manual_place', 'start_date', 'max_heart_rate', 'step_count', 'next_item_id', 'end_date', 'place_id', 'previous_item_id', 'floors_descended', 'active_energy_burned', 'item_id')
    ]
    for key in to_remove:
        timeline_item.pop(key)

    return timeline_item


def transform_sample(sample: Dict[str, Any]):
    """
    Transform the sample data from the Arc JSON to the SQLite schema.
    """
    location = sample.pop('location')
    for key, value in location.items():
        sample[f'location_{convert_to_snake_case(key)}'] = value

    # Convert the keys to snake_case
    to_convert = ['courseVariance', 'zAcceleration', 'secondsFromGMT', 'sampleId', 'movingState', 'xyAcceleration', 'recordingState', 'stepHz', 'timelineItemId', 'lastSaved']
    for key in to_convert:
        sample[convert_to_snake_case(key)] = sample.pop(key)

    # Remove any keys that are not in the schema
    to_remove = [
        k for k in sample.keys()
        if k not in ('date', 'location_latitude', 'location_longitude', 'location_speed', 'location_timestamp', 'location_horizontal_accuracy', 'location_vertical_accuracy', 'location_altitude', 'location_course', 'location_horizontal_accuracy', 'location_vertical_accuracy', 'location_speed', 'location_timestamp', 'location_longitude', 'location_latitude', 'seconds_from_gmt', 'sample_id', 'moving_state', 'xy_acceleration', 'recording_state', 'step_hz', 'timeline_item_id', 'last_saved')
    ]
    for key in to_remove:
        sample.pop(key)

    return sample
