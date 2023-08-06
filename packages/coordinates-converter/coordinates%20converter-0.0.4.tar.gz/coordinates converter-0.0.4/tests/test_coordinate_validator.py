# encoding: utf-8
from __future__ import unicode_literals
import sys

import pytest

from coordinates.converter import CoordinateValidator, LEst97CoordinatesValidator, PCS_Bounds, GCS_Bounds

if sys.version_info.major == 2:
    # nothing else seemed to enforce in tests utf8
    reload(sys)
    sys.setdefaultencoding('utf8')

MIN = 1  # min value that is under test
MAX = 3  # max value that is under test


def message_as_id(value):
    """
    Gives test a name based on message property.
    """
    return ""
    if isinstance(value, str):
        return value
    return ""


@pytest.fixture
def validator_y():
    projected_bounds = PCS_Bounds(min_y=MIN, min_x=-1, max_y=MAX, max_x=-1)
    cgs_bounds = GCS_Bounds(min_long=-1, min_lat=-1, max_long=-1, max_lat=-1)
    return CoordinateValidator(projected_bounds=projected_bounds, cgs_bounds=cgs_bounds)


@pytest.fixture
def validator_x():
    projected_bounds = PCS_Bounds(min_y=-1, min_x=MIN, max_y=-1, max_x=MAX)
    cgs_bounds = GCS_Bounds(min_long=-1, min_lat=-1, max_long=-1, max_lat=-1)
    return CoordinateValidator(projected_bounds=projected_bounds, cgs_bounds=cgs_bounds)


@pytest.fixture
def validator_latitude():
    projected_bounds = PCS_Bounds(min_y=-1, min_x=-1, max_y=-1, max_x=-1)
    cgs_bounds = GCS_Bounds(min_long=-1, min_lat=MIN, max_long=-1, max_lat=MAX)
    return CoordinateValidator(projected_bounds=projected_bounds, cgs_bounds=cgs_bounds)


@pytest.fixture
def validator_longitude():
    projected_bounds = PCS_Bounds(min_y=-1, min_x=-1, max_y=-1, max_x=-1)
    cgs_bounds = GCS_Bounds(min_long=MIN, min_lat=-1, max_long=MAX, max_lat=-1)
    return CoordinateValidator(projected_bounds=projected_bounds, cgs_bounds=cgs_bounds)


test_data = [
    (1, True, "1 is in bounds, min is 1"),
    (1.5, True, "1.5 is in bounds, (1 <= 1.5 <= 3)"),
    (2, True, "2 is in bounds, (1 <= 2 <= 3)"),
    (2.999999, True, "2.999999 is in bounds, (1 <= 2.999999 <= 3)"),
    (3, True, "3 is in bounds, max is 3"),
    (0.9, False, "0.9 is out of bounds, min is 1"),
    (-100, False, "-100 is out of bounds, min is 1"),
    (0, False, "0.9 is out of bounds, min is 1"),
    (3.1, False, "3.1 is out of bounds, max is 3"),
    (3000, False, "3000 is out of bounds, max is 3")
]


@pytest.mark.parametrize("value, in_bounds, message", test_data, ids=message_as_id)
def test_validate_projected_y(value, in_bounds, message, validator_y):
    assert validator_y.validate_projected_y(value) == in_bounds, message


@pytest.mark.parametrize("value, in_bounds, message", test_data, ids=message_as_id)
def test_validate_projected_x(value, in_bounds, message, validator_x):
    assert validator_x.validate_projected_x(value) == in_bounds, message


@pytest.mark.parametrize("value, in_bounds, message", test_data, ids=message_as_id)
def test_validate_wgs84_longitude(value, in_bounds, message, validator_longitude):
    assert validator_longitude.validate_wgs84_longitude(value) == in_bounds, message


@pytest.mark.parametrize("value, in_bounds, message", test_data, ids=message_as_id)
def test_validate_wgs84_latitude(value, in_bounds, message, validator_latitude):
    assert validator_latitude.validate_wgs84_latitude(value) == in_bounds, message


@pytest.fixture()
def validator_latitude_degree_minute_second():
    min_lat = 10.56  # 10° 33' 36"
    max_lat = 20.42  # 20° 25' 12"
    projected_bounds = PCS_Bounds(min_y=-1, min_x=-1, max_y=-1, max_x=-1)
    cgs_bounds = GCS_Bounds(min_long=-1, min_lat=min_lat, max_long=-1, max_lat=max_lat)
    return CoordinateValidator(projected_bounds=projected_bounds, cgs_bounds=cgs_bounds)


@pytest.fixture()
def validator_longitude_degree_minute_second():
    min_long = 10.56  # 10° 33' 36"
    max_long = 20.42  # 20° 25' 12"
    projected_bounds = PCS_Bounds(min_y=-1, min_x=-1, max_y=-1, max_x=-1)
    cgs_bounds = GCS_Bounds(min_long=min_long, min_lat=-1, max_long=max_long, max_lat=-1)
    return CoordinateValidator(projected_bounds=projected_bounds, cgs_bounds=cgs_bounds)


"""
Test data for degree-minute-second validations.
"""
test_data_degree_minute_second = [
    (  # 0
        (2, 2, 2),
        (False, False, True, True),
        "2° 2' 2\" is out of bounds"
    ),
    (  # 1
        (10, 33, 2),
        (False, True, True, True),
        "10° 33' 2\" is out of bounds"
    ),
    (  # 2
        (10, 33, 35,),
        (False, True, True, True),
        "10° 33' 35\" is out of bounds"
    ),
    (  # 3
        (10, 33, 36,),
        (True, True, True, True),
        "10° 33' 36\" is in bounds"
    ),
    (  # 4
        (11, 22, 33,),
        (True, True, True, True),
        "11° 22' 33\" is in bounds"
    ),
    (  # 5
        (20, 22, 33,),
        (True, True, True, True),
        "20° 22' 33\" is in bounds"
    ),
    (  # 6
        (19, 22, 59,),
        (True, True, True, True),
        "19° 22' 59\" is in bounds"
    ),
    (  # 7
        (19, 22, 60,),
        (True, True, True, False),
        "19° 22' 60\" is in bounds, but seconds can't be over 59"
    ),
    (  # 8
        (19, 22, 62,),
        (True, True, True, False),
        "19° 22' 62\" is in bounds, but seconds can't be over 59"
    ),
    (  # 9
        (19, 59, 33,),
        (True, True, True, True),
        "19° 59' 33\" is in bounds"
    ),
    (  # 10
        (19, 60, 33,),
        (True, True, False, True),
        "19° 60' 33\" is in bounds, but minutes can't be over 59"
    ),
    (  # 11
        (18, 123, 33,),
        (True, True, False, True),
        "18° 123' 33\" is in bounds, but minutes can't be over 59"
    ),
    (  # 12
        (20, 25, 12,),
        (True, True, True, True),
        "20° 25' 12\" is in bounds"),
    (  # 13
        (20, 25, 13,),
        (False, True, True, True),
        "20° 25' 13\" is in out of  bounds"
    ),
    (  # 14
        (20, 26, 12,),
        (False, True, True, True),
        "20° 26' 12\" is in out of  bounds"
    ),
    (  # 15
        (21, 25, 12,),
        (False, True, True, True),
        "21° 25' 12\" is in out of  bounds"
    ),
    (  # 16
        (15, 25, -1,),
        (True, True, True, False),
        "second can't be negative"
    ),
    (  # 17
        (15, -25, 0),
        (True, True, False, True),
        "minute can't be negative"
    )
]


@pytest.mark.parametrize("values, in_bounds, message",
                         test_data_degree_minute_second, ids=message_as_id)
def test_validate_wgs84_latitude_in_degree_minute_second(values, in_bounds, message,
                                                         validator_latitude_degree_minute_second):
    degree, minute, second = values
    validator = validator_latitude_degree_minute_second
    assert validator.validate_wgs84_latitude_in_degree_minute_second(degree, minute, second) == in_bounds, message


@pytest.mark.parametrize("values, in_bounds, message",
                         test_data_degree_minute_second, ids=message_as_id)
def test_validate_wgs84_longitude_in_degree_minute_second(values, in_bounds, message,
                                                          validator_longitude_degree_minute_second):
    degree, minute, second = values
    validator = validator_longitude_degree_minute_second
    assert validator.validate_wgs84_longitude_in_degree_minute_second(degree, minute, second) == in_bounds, message


def test_lest97_coordinates_validator():
    validator = LEst97CoordinatesValidator()

    assert not validator.validate_projected_x(370753)
    assert validator.validate_projected_x(6584335.6)
    assert validator.validate_projected_y(739245)
    assert validator.validate_projected_y(739245.6)
    assert not validator.validate_projected_y(739245.7)
