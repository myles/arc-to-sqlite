TIMELINE_ITEM_ONE_ID = "CD40927B-234F-4969-9AC6-162377BC1420"
TIMELINE_ITEM_TWO_ID = "16DB7533-F7DF-4049-AA6C-80D09EBABCC0"
SAMPLE_ONE_ID = "F83ACAFE-E4FA-4111-A633-161C5BE3FFF7"
PLACE_ONE_ID = "1B8EB0C5-EB5D-4A93-BE4E-8D839570EBE5"

SAMPLE_ONE = {
    "sampleId": SAMPLE_ONE_ID,
    "timelineItemId": TIMELINE_ITEM_ONE_ID,
    "stepHz": 1.8677083253860474,
    "date": "2024-03-05T02:59:34Z",
    "recordingState": "recording",
    "xyAcceleration": 0.7457033124259038,
    "secondsFromGMT": -18000,
    "courseVariance": 1,
    "lastSaved": "2024-03-05T02:59:45Z",
    "zAcceleration": 0.3909618147218812,
    "location": {
        "speed": 2.9235888772616923,
        "longitude": -79,
        "altitude": 92,
        "course": 164,
        "timestamp": "2024-03-05T02:59:34Z",
        "horizontalAccuracy": 35,
        "latitude": 43,
        "verticalAccuracy": 19,
    },
    "movingState": "stationary",
}

SAMPLE_TWO = {
    "sampleId": "F83ACAFE-E4FA-4111-A633-161C5BE3FFF7",
    "timelineItemId": TIMELINE_ITEM_TWO_ID,
    "stepHz": 1.8677083253860474,
    "date": "2024-03-05T02:59:34Z",
    "recordingState": "recording",
    "xyAcceleration": 0.7457033124259038,
    "secondsFromGMT": -18000,
    "courseVariance": 1,
    "lastSaved": "2024-03-05T02:59:45Z",
    "zAcceleration": 0.3909618147218812,
    "location": None,
    "movingState": "stationary",
}

PLACE_ONE = {
    "placeId": PLACE_ONE_ID,
    "streetAddress": "Place One",
    "name": "Home",
    "lastSaved": "2024-03-06T12:22:25Z",
    "radius": {"sd": 19, "mean": 12},
    "center": {"latitude": 43, "longitude": -79},
    "secondsFromGMT": -18000,
}

TIMELINE_ITEM_ONE = {
    "itemId": TIMELINE_ITEM_ONE_ID,
    "placeId": PLACE_ONE_ID,
    "hkStepCount": 859,
    "floorsAscended": 0,
    "altitude": 92,
    "center": {"latitude": 43, "longitude": -79},
    "averageHeartRate": 75,
    "streetAddress": "51 Camden St",
    "lastSaved": "2024-03-05T22:27:07Z",
    "isVisit": True,
    "manualPlace": False,
    "startDate": "2024-03-05T02:59:34Z",
    "maxHeartRate": 90,
    "stepCount": 859,
    "nextItemId": "16DB7533-F7DF-4049-AA6C-80D09EBABCC0",
    "endDate": "2024-03-05T16:11:59Z",
    "radius": {"mean": 20, "sd": 33},
    "previousItemId": None,
    "floorsDescended": 0,
    "activeEnergyBurned": 64,
    "samples": [SAMPLE_ONE],
    "place": PLACE_ONE,
}

TIMELINE_ITEM_TWO = {
    "itemId": TIMELINE_ITEM_TWO_ID,
    "placeId": PLACE_ONE_ID,
    "hkStepCount": 859,
    "floorsAscended": 0,
    "altitude": 92,
    "averageHeartRate": 75,
    "streetAddress": "51 Camden St",
    "lastSaved": "2024-03-05T22:27:07Z",
    "isVisit": True,
    "manualPlace": False,
    "startDate": "2024-03-05T02:59:34Z",
    "maxHeartRate": 90,
    "stepCount": 859,
    "nextItemId": "16DB7533-F7DF-4049-AA6C-80D09EBABCC0",
    "endDate": "2024-03-05T16:11:59Z",
    "previousItemId": TIMELINE_ITEM_ONE_ID,
    "floorsDescended": 0,
    "activeEnergyBurned": 64,
    "samples": [SAMPLE_TWO],
    "place": PLACE_ONE,
}

DAILY_EXPORT = {"timelineItems": [TIMELINE_ITEM_ONE]}
