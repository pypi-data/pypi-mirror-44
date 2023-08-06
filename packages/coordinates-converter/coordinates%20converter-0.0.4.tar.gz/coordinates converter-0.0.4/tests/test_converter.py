# encoding: utf-8
from __future__ import unicode_literals
import sys
import pytest

from coordinates.converter import *

if sys.version_info.major == 2:
    # nothing else seemed to enforce in tests utf8
    reload(sys)
    sys.setdefaultencoding('utf8')

test_coordinates_data = [
    (L_Est97(6584335.6, 537731.1), WGS84(24.664104611385, 59.395284958281)),
    (L_Est97(6543210.14, 543210.86), WGS84(24.752426843059, 59.025604914502)),
    (L_Est97(6543210.14, 543210.86), WGS84(24.752426843059, 59.025604914502)),
    (L_Est97(6543421.54, 543228.55), WGS84(24.752776160968, 59.027500845678)),
    (L_Est97(6543866.63, 543268.44), WGS84(24.753557811146, 59.031492341966)),
]


@pytest.mark.parametrize("l_est97, expected_wgs97", test_coordinates_data, ids=str)
def test_est97_to_wgs84(l_est97, expected_wgs97):
    tolerance = 0.00001
    actual_wgs97 = CoordinateConverter.l_est97_to_wgs84(l_est97)
    assert actual_wgs97.long == pytest.approx(expected_wgs97.long, abs=tolerance)
    assert actual_wgs97.lat == pytest.approx(expected_wgs97.lat, abs=tolerance)


@pytest.mark.parametrize("expected_l_est97, wgs97", test_coordinates_data, ids=str)
def test_wgs84_to_est97(wgs97, expected_l_est97):
    tolerance = 0.001
    actual_est97 = CoordinateConverter.wgs84_to_l_est97(wgs97)
    print("wgs", wgs97, "actual", actual_est97, "expected", expected_l_est97)
    assert actual_est97.x == pytest.approx(expected_l_est97.x, abs=tolerance)
    assert actual_est97.y == pytest.approx(expected_l_est97.y, abs=tolerance)


def test_decimal_to_degrees():
    assert convert_decimal_to_degrees(30.56) == (30, 33, 36)
    assert convert_decimal_to_degrees(30.429) == (30, 25, 44.4)


def test_degrees_to_decimal():
    assert convert_degrees_to_decimal(10, 23, 42) == 10.395
    assert convert_degrees_to_decimal(40, 51, 10.395) == 40.8528875


def test_try_convert_float__simple_numbers__returns_float():
    assert try_convert_float("12") == (12., True)
    assert try_convert_float("32.42") == (32.42, True)


def test_try_convert_float__with_comma_as_a_separator__returns_float():
    assert try_convert_float("32,42") == (32.42, True)


def test_try_convert_float__negative_number__returns_float():
    assert try_convert_float("-32.42") == (-32.42, True)
    assert try_convert_float("-32,42") == (-32.42, True)


def test_try_convert_float__value_is_already_float__returns_float():
    assert try_convert_float(10.2) == (10.2, True)


def test_try_convert_float__value_is_int__returns_float():
    assert try_convert_float(1) == (1., True)


def test_try_convert_float__not_number_string__returns_false():
    assert not try_convert_float("just a string")[1]


def test_try_convert_float__empty_string__returns_false():
    assert not try_convert_float("")[1]

def test_try_convert_float__invalid_type__returns_false():
    assert not try_convert_float(object)[1]


def test_format_degrees():
    assert format_degrees(11, 22, 33) == "11° 22' 33\""
