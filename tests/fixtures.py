SAMPLE_ONE_ID = "F83ACAFE-E4FA-4111-A633-161C5BE3FFF7"
SAMPLE_TWO_ID = "6397550D-D353-4FDB-9B15-DF255CEDE3CC"
SAMPLE_THREE_ID = "F83ACAFE-E4FA-4111-A633-161C5BE3FFF7"

PLACE_ONE_ID = "1B8EB0C5-EB5D-4A93-BE4E-8D839570EBE5"
PLACE_TWO_ID = "D1618FC7-E0E2-4E49-A893-E455444F6B08"
PLACE_THREE_ID = "090FA8EC-5340-418B-972E-0F4E1460B10B"

TIMELINE_ITEM_ONE_ID = "CD40927B-234F-4969-9AC6-162377BC1420"
TIMELINE_ITEM_TWO_ID = "16DB7533-F7DF-4049-AA6C-80D09EBABCC0"

SAMPLE_ONE = {
    "courseVariance": 0.04674363583353203,
    "date": "2024-05-21T17:25:47Z",
    "lastSaved": "2024-05-21T17:29:15Z",
    "location": {
        "course": 303.3725673485157,
        "timestamp": "2024-05-21T17:25:47Z",
        "speed": 0.29863812131809236,
        "altitude": 88.25412084907234,
        "verticalAccuracy": 9.865744092378542,
        "longitude": -79.41240717690286,
        "horizontalAccuracy": 14.390501150304601,
        "latitude": 43.64544093961851,
    },
    "movingState": "moving",
    "recordingState": "recording",
    "sampleId": SAMPLE_ONE_ID,
    "secondsFromGMT": -14400,
    "stepHz": 1.923324704170227,
    "timelineItemId": TIMELINE_ITEM_ONE_ID,
    "xyAcceleration": 0.7052750449750282,
    "zAcceleration": 0.5412744957771787,
}

TRANSFORMED_SAMPLE_ONE = {
    "moving_state": SAMPLE_ONE["movingState"],
    "taken_at": SAMPLE_ONE["date"],
    "z_acceleration": SAMPLE_ONE["zAcceleration"],
    "sample_id": SAMPLE_ONE_ID,
    "last_saved_at": SAMPLE_ONE["lastSaved"],
    "seconds_from_gmt": SAMPLE_ONE["secondsFromGMT"],
    "course": SAMPLE_ONE["location"]["course"],
    "speed": SAMPLE_ONE["location"]["speed"],
    "altitude": SAMPLE_ONE["location"]["altitude"],
    "vertical_accuracy": SAMPLE_ONE["location"]["verticalAccuracy"],
    "longitude": SAMPLE_ONE["location"]["longitude"],
    "horizontal_accuracy": SAMPLE_ONE["location"]["horizontalAccuracy"],
    "latitude": SAMPLE_ONE["location"]["latitude"],
    "recording_state": SAMPLE_ONE["recordingState"],
    "course_variance": SAMPLE_ONE["courseVariance"],
    "step_hz": SAMPLE_ONE["stepHz"],
    "xy_acceleration": SAMPLE_ONE["xyAcceleration"],
    "timeline_item_id": TIMELINE_ITEM_ONE_ID,
}

SAMPLE_TWO = {
    "courseVariance": 0.00700875460490713,
    "date": "2024-05-21T17:43:29Z",
    "lastSaved": "2024-05-21T18:21:43Z",
    "location": {
        "altitude": 95.07555516006282,
        "horizontalAccuracy": 14.492842487107929,
        "longitude": -79.42040853279485,
        "course": 159.97787496806967,
        "timestamp": "2024-05-21T17:43:29Z",
        "verticalAccuracy": 9.69881840273028,
        "latitude": 43.64855618082636,
        "speed": 0.8521664198402463,
    },
    "movingState": "moving",
    "recordingState": "recording",
    "sampleId": SAMPLE_TWO_ID,
    "secondsFromGMT": -14400,
    "stepHz": 1.9765706062316895,
    "timelineItemId": TIMELINE_ITEM_TWO_ID,
    "xyAcceleration": 3.341598249596829,
    "zAcceleration": 2.089857692656623,
}

TRANSFORMED_SAMPLE_TWO = {
    "xy_acceleration": SAMPLE_TWO["xyAcceleration"],
    "altitude": SAMPLE_TWO["location"]["altitude"],
    "horizontal_accuracy": SAMPLE_TWO["location"]["horizontalAccuracy"],
    "longitude": SAMPLE_TWO["location"]["longitude"],
    "course": SAMPLE_TWO["location"]["course"],
    "vertical_accuracy": SAMPLE_TWO["location"]["verticalAccuracy"],
    "latitude": SAMPLE_TWO["location"]["latitude"],
    "speed": SAMPLE_TWO["location"]["speed"],
    "z_acceleration": SAMPLE_TWO["zAcceleration"],
    "last_saved_at": SAMPLE_TWO["lastSaved"],
    "sample_id": SAMPLE_TWO_ID,
    "moving_state": SAMPLE_TWO["movingState"],
    "timeline_item_id": TIMELINE_ITEM_TWO_ID,
    "seconds_from_gmt": SAMPLE_TWO["secondsFromGMT"],
    "recording_state": SAMPLE_TWO["recordingState"],
    "taken_at": SAMPLE_TWO["date"],
    "step_hz": SAMPLE_TWO["stepHz"],
    "course_variance": SAMPLE_TWO["courseVariance"],
}

SAMPLE_THREE = {
    "courseVariance": 0.00700875460490713,
    "date": "2024-05-21T17:43:29Z",
    "lastSaved": "2024-05-21T18:21:43Z",
    "movingState": "moving",
    "recordingState": "recording",
    "sampleId": SAMPLE_THREE_ID,
    "secondsFromGMT": -14400,
    "stepHz": 1.9765706062316895,
    "timelineItemId": "16DB7533-F7DF-4049-AA6C-80D09EBABCC0",
    "xyAcceleration": 3.341598249596829,
    "zAcceleration": 2.089857692656623,
}

TRANSFORMED_SAMPLE_THREE = {
    "xy_acceleration": SAMPLE_THREE["xyAcceleration"],
    "z_acceleration": SAMPLE_THREE["zAcceleration"],
    "last_saved_at": SAMPLE_THREE["lastSaved"],
    "sample_id": SAMPLE_THREE_ID,
    "moving_state": SAMPLE_THREE["movingState"],
    "timeline_item_id": TIMELINE_ITEM_TWO_ID,
    "seconds_from_gmt": SAMPLE_THREE["secondsFromGMT"],
    "recording_state": SAMPLE_THREE["recordingState"],
    "taken_at": SAMPLE_THREE["date"],
    "step_hz": SAMPLE_THREE["stepHz"],
    "course_variance": SAMPLE_THREE["courseVariance"],
}

PLACE_ONE = {
    "placeId": PLACE_ONE_ID,
    "secondsFromGMT": -14400,
    "radius": {"sd": 1.5841370751938844, "mean": 37.40621024834282},
    "streetAddress": "907 Queen St W",
    "mapboxCategory": "ice cream, ice cream parlor, dessert, craft, shop",
    "name": "White Squirrel",
    "mapboxPlaceId": "poi.403727005260",
    "lastSaved": "2024-05-23T19:38:52Z",
    "center": {"longitude": -79.4128035873503, "latitude": 43.6453939410202},
}

TRANSFORMED_PLACE_ONE = {
    "place_id": PLACE_ONE_ID,
    "seconds_from_gmt": PLACE_ONE["secondsFromGMT"],
    "radius_sd": PLACE_ONE["radius"]["sd"],
    "radius_mean": PLACE_ONE["radius"]["mean"],
    "street_address": PLACE_ONE["streetAddress"],
    "mapbox_category": PLACE_ONE["mapboxCategory"],
    "name": PLACE_ONE["name"],
    "mapbox_place_id": PLACE_ONE["mapboxPlaceId"],
    "last_saved_at": PLACE_ONE["lastSaved"],
    "latitude": PLACE_ONE["center"]["latitude"],
    "longitude": PLACE_ONE["center"]["longitude"],
}

PLACE_TWO = {
    "secondsFromGMT": -14400,
    "googlePrimaryType": "point_of_interest",
    "lastSaved": "2024-05-21T20:37:47Z",
    "streetAddress": "186 Ossington Ave, Toronto",
    "center": {"latitude": 43.64850321438813, "longitude": -79.42052655137904},
    "googlePlaceId": "ChIJOdyG5OM0K4gRYGhH2tJIXT0",
    "name": "Rotate This",
    "placeId": PLACE_TWO_ID,
    "radius": {"sd": 3.654503445585429, "mean": 8},
}

TRANSFORMED_PLACE_TWO = {
    "place_id": PLACE_TWO_ID,
    "seconds_from_gmt": PLACE_TWO["secondsFromGMT"],
    "google_primary_type": PLACE_TWO["googlePrimaryType"],
    "last_saved_at": PLACE_TWO["lastSaved"],
    "street_address": PLACE_TWO["streetAddress"],
    "latitude": PLACE_TWO["center"]["latitude"],
    "longitude": PLACE_TWO["center"]["longitude"],
    "google_place_id": PLACE_TWO["googlePlaceId"],
    "name": PLACE_TWO["name"],
    "radius_sd": PLACE_TWO["radius"]["sd"],
    "radius_mean": PLACE_TWO["radius"]["mean"],
}

PLACE_THREE = {
    "placeId": PLACE_THREE_ID,
    "lastSaved": "2024-05-23T19:38:51Z",
    "streetAddress": "2567 Dundas St W",
    "center": {"latitude": 43.65, "longitude": -79.45},
    "secondsFromGMT": -14400,
    "name": "1RG",
    "radius": {"sd": 13.98111421024259, "mean": 9.702352969028617},
}

TRANSFORMED_PLACE_THREE = {
    "place_id": PLACE_THREE_ID,
    "last_saved_at": PLACE_THREE["lastSaved"],
    "street_address": PLACE_THREE["streetAddress"],
    "latitude": PLACE_THREE["center"]["latitude"],
    "longitude": PLACE_THREE["center"]["longitude"],
    "seconds_from_gmt": PLACE_THREE["secondsFromGMT"],
    "name": PLACE_THREE["name"],
    "radius_sd": PLACE_THREE["radius"]["sd"],
    "radius_mean": PLACE_THREE["radius"]["mean"],
}

TIMELINE_ITEM_ONE = {
    "place": PLACE_ONE,
    "isVisit": True,
    "lastSaved": "2024-05-23T12:47:25Z",
    "previousItemId": "D1618FC7-E0E2-4E49-A893-E455444F6B08",
    "itemId": "BBB12A29-A604-4A0E-93B1-506FAF8FB3CD",
    "floorsAscended": 0,
    "nextItemId": "090FA8EC-5340-418B-972E-0F4E1460B10B",
    "maxHeartRate": 116,
    "activeEnergyBurned": 16.02499999999999,
    "stepCount": 968,
    "placeId": "14EEA365-411F-4A94-98EC-5DA469CA2346",
    "manualPlace": False,
    "floorsDescended": 0,
    "startDate": "2024-05-21T17:25:47Z",
    "endDate": "2024-05-21T17:31:24Z",
    "averageHeartRate": 101.56731723924611,
    "hkStepCount": 968,
    "radius": {"mean": 2.8059859426359575, "sd": 1.5553486899973161},
    "streetAddress": "907 Queen St W",
    "samples": [SAMPLE_ONE],
    "center": {"latitude": 43.64549602595442, "longitude": -79.4124450271659},
    "altitude": 88.95823949203351,
}

TRANSFORMED_TIMELINE_ITEM_ONE = {
    "item_id": "BBB12A29-A604-4A0E-93B1-506FAF8FB3CD",
    "place_id": "14EEA365-411F-4A94-98EC-5DA469CA2346",
    "is_visit": True,
    "last_saved_at": "2024-05-23T12:47:25Z",
    "previous_item_id": "D1618FC7-E0E2-4E49-A893-E455444F6B08",
    "floors_ascended": 0,
    "next_item_id": "090FA8EC-5340-418B-972E-0F4E1460B10B",
    "max_heart_rate": 116,
    "active_energy_burned": 16.02499999999999,
    "step_count": 968,
    "manual_place": False,
    "floors_descended": 0,
    "starts_at": "2024-05-21T17:25:47Z",
    "ends_at": "2024-05-21T17:31:24Z",
    "average_heart_rate": 101.56731723924611,
    "hk_step_count": 968,
    "radius_mean": 2.8059859426359575,
    "radius_sd": 1.5553486899973161,
    "street_address": "907 Queen St W",
    "latitude": 43.64549602595442,
    "longitude": -79.4124450271659,
    "altitude": 88.95823949203351,
}

TIMELINE_ITEM_TWO = {
    "previousItemId": TIMELINE_ITEM_ONE_ID,
    "floorsAscended": 0,
    "maxHeartRate": 112,
    "center": {"latitude": 43.648511045082046, "longitude": -79.42045183649164},
    "isVisit": True,
    "streetAddress": "207 Ossington Ave",
    "endDate": "2024-05-21T17:46:39Z",
    "startDate": "2024-05-21T17:43:29Z",
    "altitude": 93.87385195827153,
    "itemId": TIMELINE_ITEM_TWO_ID,
    "place": PLACE_TWO,
    "stepCount": 801,
    "floorsDescended": 0,
    "activeEnergyBurned": 8.063999999999993,
    "nextItemId": "2E9C80E7-3C70-4AC0-8F73-3526929836D8",
    "samples": [SAMPLE_TWO, SAMPLE_THREE],
    "lastSaved": "2024-05-21T20:37:42Z",
    "placeId": PLACE_TWO_ID,
    "radius": {"mean": 4.577843847020305, "sd": 2.1820948992412137},
    "hkStepCount": 801,
    "averageHeartRate": 108.02198421672875,
    "manualPlace": True,
}

TRANSFORMED_TIMELINE_ITEM_TWO = {
    "previous_item_id": TIMELINE_ITEM_ONE_ID,
    "floors_ascended": 0,
    "max_heart_rate": 112,
    "latitude": 43.648511045082046,
    "longitude": -79.42045183649164,
    "is_visit": True,
    "street_address": "207 Ossington Ave",
    "ends_at": "2024-05-21T17:46:39Z",
    "starts_at": "2024-05-21T17:43:29Z",
    "altitude": 93.87385195827153,
    "item_id": TIMELINE_ITEM_TWO_ID,
    "place_id": PLACE_TWO_ID,
    "step_count": 801,
    "floors_descended": 0,
    "active_energy_burned": 8.063999999999993,
    "next_item_id": "2E9C80E7-3C70-4AC0-8F73-3526929836D8",
    "radius_mean": 4.577843847020305,
    "radius_sd": 2.1820948992412137,
    "hk_step_count": 801,
    "average_heart_rate": 108.02198421672875,
    "manual_place": True,
    "last_saved_at": "2024-05-21T20:37:42Z",
}

TIMELINE_ITEM_THREE = {
    "place": PLACE_ONE,
    "isVisit": True,
    "lastSaved": "2024-05-23T12:47:25Z",
    "previousItemId": "D1618FC7-E0E2-4E49-A893-E455444F6B08",
    "itemId": "BBB12A29-A604-4A0E-93B1-506FAF8FB3CD",
    "floorsAscended": 0,
    "nextItemId": "090FA8EC-5340-418B-972E-0F4E1460B10B",
    "maxHeartRate": 116,
    "activeEnergyBurned": 16.02499999999999,
    "stepCount": 968,
    "placeId": "14EEA365-411F-4A94-98EC-5DA469CA2346",
    "manualPlace": False,
    "floorsDescended": 0,
    "startDate": "2024-05-21T17:25:47Z",
    "endDate": "2024-05-21T17:31:24Z",
    "averageHeartRate": 101.56731723924611,
    "hkStepCount": 968,
    "streetAddress": "907 Queen St W",
    "altitude": 88.95823949203351,
}

TRANSFORMED_TIMELINE_ITEM_THREE = {
    "item_id": "BBB12A29-A604-4A0E-93B1-506FAF8FB3CD",
    "place_id": "14EEA365-411F-4A94-98EC-5DA469CA2346",
    "is_visit": True,
    "last_saved_at": "2024-05-23T12:47:25Z",
    "previous_item_id": "D1618FC7-E0E2-4E49-A893-E455444F6B08",
    "floors_ascended": 0,
    "next_item_id": "090FA8EC-5340-418B-972E-0F4E1460B10B",
    "max_heart_rate": 116,
    "active_energy_burned": 16.02499999999999,
    "step_count": 968,
    "manual_place": False,
    "floors_descended": 0,
    "starts_at": "2024-05-21T17:25:47Z",
    "ends_at": "2024-05-21T17:31:24Z",
    "average_heart_rate": 101.56731723924611,
    "hk_step_count": 968,
    "street_address": "907 Queen St W",
    "altitude": 88.95823949203351,
}

TIMELINE_ITEM_FOUR = {
    "hkStepCount": 1630,
    "stepCount": 1630,
    "lastSaved": "2024-05-23T12:50:09Z",
    "endDate": "2024-05-21T17:25:47Z",
    "manualActivityType": False,
    "averageHeartRate": 105.59242144122362,
    "startDate": "2024-05-21T17:05:16Z",
    "isVisit": False,
    "activeEnergyBurned": 121.91300000000001,
    "maxHeartRate": 114,
    "floorsAscended": 0,
    "floorsDescended": 1,
    "altitude": 90.68901323082461,
    "nextItemId": "BBB12A29-A604-4A0E-93B1-506FAF8FB3CD",
    "activityType": "walking",
    "itemId": "D1618FC7-E0E2-4E49-A893-E455444F6B08",
    "uncertainActivityType": False,
    "activityTypeConfidenceScore": 40.66899060304041,
    "previousItemId": "17FAA692-0F76-4D05-98C9-A13550D238C1",
    "unknownActivityType": False,
}

TRANSFORMED_TIMELINE_ITEM_FOUR = {
    "hk_step_count": 1630,
    "step_count": 1630,
    "last_saved_at": "2024-05-23T12:50:09Z",
    "ends_at": "2024-05-21T17:25:47Z",
    "manual_activity_type": False,
    "average_heart_rate": 105.59242144122362,
    "starts_at": "2024-05-21T17:05:16Z",
    "is_visit": False,
    "active_energy_burned": 121.91300000000001,
    "max_heart_rate": 114,
    "floors_ascended": 0,
    "floors_descended": 1,
    "altitude": 90.68901323082461,
    "next_item_id": "BBB12A29-A604-4A0E-93B1-506FAF8FB3CD",
    "activity_type": "walking",
    "item_id": "D1618FC7-E0E2-4E49-A893-E455444F6B08",
    "uncertain_activity_type": False,
    "activity_type_confidence_score": 40.66899060304041,
    "previous_item_id": "17FAA692-0F76-4D05-98C9-A13550D238C1",
    "unknown_activity_type": False,
}

DAILY_EXPORT = {
    "timelineItems": [TIMELINE_ITEM_ONE, TIMELINE_ITEM_TWO, TIMELINE_ITEM_THREE]
}
