# encoding: utf-8
"""
Program that converts from WGS84 to L-Est97 coordinate system and vice versa.

Author: Kristjan Tärk
"""
from __future__ import unicode_literals
from typing import Tuple, Union
from math import floor, ceil
from pyproj import Proj
from collections import namedtuple
from coordinates import __pdoc__


__pdoc__['L_Est97'] = 'Namedtuple for L-Est97 coordinate system.'
__pdoc__['L_Est97.x'] = 'x coordinate.'
__pdoc__['L_Est97.y'] = 'y coordinate.'
L_Est97 = namedtuple("L_Est97", ("x", "y"))


__pdoc__['WGS_84'] = 'Namedtuple for WGS84 coordinate system.'
__pdoc__['WGS_84.long'] = 'longitude.'
__pdoc__['WGS_84.lat'] = 'latitude.'
WGS84 = namedtuple("WGS_84", ("long", "lat"))


__pdoc__['CGS_Bounds'] = 'Namedtuple for holding' \
                         ' geographic coordinate system bounds'
__pdoc__['CGS_Bounds.min_long'] = ""
__pdoc__['CGS_Bounds.max_long'] = ""
__pdoc__['CGS_Bounds.min_lat'] = ""
__pdoc__['CGS_Bounds.max_lat'] = ""
GCS_Bounds = namedtuple(
    "CGS_Bounds", ("min_long", "min_lat", "max_long", "max_lat")
)

__pdoc__['PCS_Bounds'] = 'Namedtuple for holding' \
                         ' projected coordinate system bounds'
__pdoc__['PCS_Bounds.min_x'] = ""
__pdoc__['PCS_Bounds.max_x'] = ""
__pdoc__['PCS_Bounds.min_y'] = ""
__pdoc__['PCS_Bounds.max_y'] = ""
PCS_Bounds = namedtuple(
    "PCS_Bounds", ("min_y", "min_x", "max_y", "max_x")
)


class CoordinateConverter:
    """
    Convert from WGS84 to L-Est97 coordinate system and vice versa.

    Coordinates with rules given in http://spatialreference.org/ref/epsg/3301/
    """

    _est_97 = Proj(init="epsg:3301")

    @staticmethod
    def l_est97_to_wgs84(l_est97):
        # type: (L_Est97) -> WGS84
        """
        Convert L-Est97 coordinates to WGS84.

        This method doesn't validate coordinate boundaries,
        validating is users responsibility.
        For validating LEst97CoordinatesValidator class can be used.

        Args:
            l_est97: coordinates as L_Est97 namedtuple
        Returns:
             Coordinates as WGS84 namedtuple
        """
        x, y = l_est97.x, l_est97.y
        long, lat = CoordinateConverter._est_97(y, x, inverse=True)
        return WGS84(long, lat)

    @staticmethod
    def wgs84_to_l_est97(wgs84):
        # type: (WGS84) -> L_Est97
        """
        Convert WGS84 coordinates to L-Est97.

        This method doesn't validate coordinate boundaries,
        validating is users responsibility.
        For validating LEst97CoordinatesValidator class can be used.
        Args:
            wgs84: coordinates as WGS84 namedtuple
        Returns:
             Coordinates as L_Est97 namedtuple
        """
        y, x = CoordinateConverter._est_97(wgs84.long, wgs84.lat)
        y, x = round(y, 2), round(x, 2)
        return L_Est97(x, y)


class CoordinateValidator(object):
    """
    Validates that coordinates are in given bounds.

    For coordinate systems there are upper and lower bounds for coordinates.
    This class verifies that given coordinate is in the bounds.
    """

    def __init__(self, projected_bounds, cgs_bounds):
        # type: (PCS_Bounds, GCS_Bounds) -> CoordinateValidator
        """
        Creates new validator.

        Args:
            projected_bounds: projected coordinate system (PCS) boundaries
            cgs_bounds: geographic coordinate system (GCS) boundaries
        """
        self.projected_bounds = projected_bounds
        self.cgs_bounds = cgs_bounds

    def validate_projected_x(self, value):
        # type: (float) -> bool
        """Validate that x coordinate is in given boundaries."""
        bounds = self.projected_bounds
        return self._is_in_range(value, bounds.min_x, bounds.max_x)

    def validate_projected_y(self, value):
        # type: (float) -> bool
        """Validate that y coordinate is in given boundaries."""
        bounds = self.projected_bounds
        return self._is_in_range(value, bounds.min_y, bounds.max_y)

    def validate_wgs84_latitude(self, value):
        # type: (float) -> bool
        """Validate that latitude is in given boundaries."""
        bounds = self.cgs_bounds
        return self._is_in_range(value, bounds.min_lat, bounds.max_lat)

    def validate_wgs84_latitude_in_degree_minute_second(self, degree, minutes,
                                                        seconds):
        # type: (int, int, float) -> Tuple[bool, bool, bool, bool]
        """
        Validate that latitude in degrees-minutes-seconds is in given bounds.

        Args:
            minutes: has to be between 0 and 59 inclusive
            seconds: has to be between 0 and 59 inclusive
        Returns:
            Tuple of four booleans, where booleans indicate:

            1. if coordinates are in given bounds.
            2. if degree is in given bounds.
            3. if minute is between 0 and 59 inclusive.
            4. if second is between 0 and 59 inclusive.
        """
        bounds = self.cgs_bounds
        decimal_degrees = convert_degrees_to_decimal(degree, minutes, seconds)
        bounds_result = self._is_in_range(
            decimal_degrees, bounds.min_lat, bounds.max_lat
        )
        degree_result = floor(bounds.min_lat) <= degree <= ceil(bounds.max_lat)
        minutes_result = 0 <= minutes < 60
        seconds_result = 0 <= seconds < 60
        return bounds_result, degree_result, minutes_result, seconds_result

    def validate_wgs84_longitude(self, value):
        # type: (float) -> bool
        """Validate that longitude is in given boundaries."""
        bounds = self.cgs_bounds
        return self._is_in_range(value, bounds.min_long, bounds.max_long)

    def validate_wgs84_longitude_in_degree_minute_second(self, degree, minutes,
                                                         seconds):
        # type: (int, int, float) -> Tuple[bool, bool, bool, bool]
        """
        Validate that longitude in degrees-minutes-seconds is in given bounds.

        Args:
            minutes: has to be between 0 and 59 inclusive
            seconds: has to be between 0 and 59 inclusive
        Returns:
            Tuple of four booleans, where booleans indicate:

            1. if coordinates are in given bounds.
            2. if degree is in given bounds.
            3. if minute is between 0 and 59 inclusive.
            4. if second is between 0 and 59 inclusive.
        """
        bounds = self.cgs_bounds
        decimal_degrees = convert_degrees_to_decimal(degree, minutes, seconds)
        bound_result = self._is_in_range(
            decimal_degrees, bounds.min_long, bounds.max_long
        )
        degree_result = floor(bounds.min_long) <= degree <= ceil(bounds.max_long)  # noqa: E501
        minutes_result = 0 <= minutes < 60
        seconds_result = 0 <= seconds < 60
        return bound_result, degree_result, minutes_result, seconds_result

    @staticmethod
    def _is_in_range(value, min_bound, max_bound):
        # type: (float, float, float) -> bool
        return min_bound <= value <= max_bound


class LEst97CoordinatesValidator(CoordinateValidator):
    """
    Coordinate validator for L-Est97 coordinate system.

    Boundaries taken are from http://spatialreference.org/ref/epsg/3301/
    """

    def __init__(self):
        projected_bounds = PCS_Bounds(
            min_y=370753.1145,
            max_y=739245.6000,
            min_x=6382922.7769,
            max_x=6624811.0577
        )
        cgs_bounds = GCS_Bounds(
            min_long=21.8400,
            max_long=28.000,
            min_lat=57.5700,
            max_lat=59.7000
        )
        super(LEst97CoordinatesValidator, self).__init__(projected_bounds, cgs_bounds)  # noqa: E501


def convert_decimal_to_degrees(decimal):
    # type: (float) -> Tuple[int, int, float]
    """
    Convert decimal degrees to degree-minute-second format.

    Example:
        >>> convert_decimal_to_degrees(30.56)
        (30, 33, 36)

    Args:
        Decimal: degree in decimals
    Returns:
        Tuple of degree-minute-second.
    """
    degrees = int(decimal)
    minutes = int((decimal - degrees) * 60)
    seconds = round((decimal - degrees - minutes / 60.) * 3600, 4)
    return degrees, minutes, seconds


def convert_degrees_to_decimal(degrees, minutes, seconds):
    # type: (int, int, float) -> float
    """
    Convert degree-minute-second format to decimal degrees.

    Example:
    >>> convert_degrees_to_decimal(10, 23, 42)
    10.395

    Returns:
         Degrees in decimal format
    """
    return degrees + minutes / 60. + seconds / 3600.


def try_convert_float(float_value):
    # type: (Union[str, float, int]) -> Tuple[float, bool]
    """
    Try convert object to a float.

    Args:
        Float_value: value of string, float or integer
    Returns:
        Tuple of float and boolean. boolean indicates if value was converted.
    """
    if isinstance(float_value, (float, int)):
        return float_value, True
    try:
        float_value = float(float_value.replace(",", "."))
        return float_value, True
    except ValueError:
        return 0., False
    except:  # noqa: E722
        print("Error converting {} to float".format(float_value))
        return 0., False


def format_degrees(degrees, minutes, seconds):
    # type: (int, int, float) -> str
    """
    Format degree-minute-second to a string

    Example:
    >>> format_degrees(11, 22, 33)
    11° 22' 33"

    Returns:
         String representation of degree.
    """
    return "".join(map(str, [degrees, '° ', minutes, "' ", seconds, '"']))
