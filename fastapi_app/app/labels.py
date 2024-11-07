from enum import Enum

class Labels(Enum):
    NULL = {'id': 0, 'name': "null"}
    STILL = {'id': 1, 'name': "still"}
    WALKING = {'id': 2, 'name': "walking"}
    RUN = {'id': 3, 'name': "run"}
    BIKE = {'id': 4, 'name': "bike"}
    CAR = {'id': 5, 'name': "car"}
    BUS = {'id': 6, 'name': "bus"}
    TRAIN = {'id': 7, 'name': "train"}
    SUBWAY = {'id': 8, 'name': "subway"}