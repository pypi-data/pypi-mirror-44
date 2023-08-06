# encoding: utf-8
"""
Tkinter client for coordinate converter.

Usage: run `converter-app` in the terminal and client pops up.

Author: Kristjan Tärk
"""
from __future__ import unicode_literals
import sys
import click

from .converter import (L_Est97, WGS84,
                        LEst97CoordinatesValidator, CoordinateConverter,
                        convert_degrees_to_decimal, convert_decimal_to_degrees,
                        format_degrees, try_convert_float)

if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding('utf8')
    import Tkinter as tk
    import ttk
else:
    import tkinter as tk
    from tkinter import ttk


@click.command()
def start_app():
    """Click command to launch the app."""
    root = tk.Tk()
    ConverterClient(root)
    root.mainloop()


class ConverterClient:
    """Converter main class that orchestrates creation of UI."""

    def __init__(self, master):
        self.master = master
        self.validator = LEst97CoordinatesValidator()

        master.title("L-Est97 <-> WGS84")

        tabControl = ttk.Notebook(self.master)
        tab_l_est97 = ttk.Frame(tabControl)
        tab_wgs84 = ttk.Frame(tabControl)
        tabControl.add(tab_l_est97, text='L-Est97 -> WGS84')
        tabControl.add(tab_wgs84, text='WGS84 -> L-Est97')
        tabControl.grid(row=1, column=1, columnspan=10)

        LEst97ConverterUI(self.master, tab_l_est97, self.validator)
        WGS97ConverterUI(self.master, tab_wgs84, self.validator)


class LEst97ConverterUI:
    """UI part that handles L-Est97 to WGS84 coordinate converting."""

    def __init__(self, master, tab, validator):
        self.x = 0
        self.y = 0

        label_x_text = "".join(map(str, [
            "Ristkoordinaat X (m) (",
            validator.projected_bounds.min_x,
            " ... ",
            validator.projected_bounds.max_x,
            ")"
        ]))
        label_x = tk.Label(tab, text=label_x_text)

        entry_x = tk.Entry(tab, validate="all")
        entry_x_validator = _create_validator(entry_x,
                                              validator.validate_projected_x,
                                              self._assign_x)
        vcmd_x = master.register(entry_x_validator)
        entry_x["validatecommand"] = vcmd_x, '%P', '%V'

        label_y_text = "".join(map(str, [
            "Ristkoordinaat Y (m) (",
            validator.projected_bounds.min_y,
            " ... ",
            str(validator.projected_bounds.max_y),
            ")"
        ]))
        label_y = tk.Label(tab, text=label_y_text)

        entry_y = tk.Entry(tab, validate="all")
        entry_y_validator = _create_validator(entry_y,
                                              validator.validate_projected_y,
                                              self._assign_y)
        vcmd_y = master.register(entry_y_validator)
        entry_y["validatecommand"] = vcmd_y, '%P', '%V'

        button_convert = tk.Button(
            tab, text="Arvuta", command=self.convert_to_wsg84
        )

        result_entry_lat = tk.Label(tab, text="Põhjalaius")
        result_entry_long = tk.Label(tab, text="Idapikkus")
        self.result_label_lat_decimal = EntryWithSet(tab, state='disabled')
        self.result_label_lat_degrees = EntryWithSet(tab, state='disabled')
        self.result_label_long_decimal = EntryWithSet(tab, state='disabled')
        self.result_label_long_degrees = EntryWithSet(tab, state='disabled')

        label_x.grid(row=1, column=0, columnspan=5, sticky=tk.W)
        entry_x.grid(row=1, column=5, columnspan=5)
        label_y.grid(row=2, column=0, columnspan=5, sticky=tk.W)
        entry_y.grid(row=2, column=5, columnspan=5)
        button_convert.grid(row=3, column=8, columnspan=2)
        result_entry_lat.grid(row=4, column=0, columnspan=3, sticky=tk.E)
        self.result_label_lat_decimal.grid(row=4, column=3, columnspan=4)
        self.result_label_lat_degrees.grid(row=4, column=7, columnspan=4)
        result_entry_long.grid(row=5, column=0, columnspan=3, sticky=tk.E)
        self.result_label_long_decimal.grid(row=5, column=3, columnspan=4)
        self.result_label_long_degrees.grid(row=5, column=7, columnspan=4)

    def _assign_x(self, x):
        """Helper to pass assigning function to input validator object."""
        self.x = x

    def _assign_y(self, y):
        """Helper to pass assigning function to input validator object."""
        self.y = y

    def convert_to_wsg84(self):
        """Convert user input to WGS84 and display it to user."""
        est97 = L_Est97(self.x, self.y)
        result = CoordinateConverter.l_est97_to_wgs84(est97)
        self.result_label_lat_decimal.value = result.lat
        self.result_label_lat_degrees.value = format_degrees(
            *convert_decimal_to_degrees(result.lat)
        )
        self.result_label_long_decimal.value = result.long
        self.result_label_long_degrees.value = format_degrees(
            *convert_decimal_to_degrees(result.long)
        )


class WGS97ConverterUI:
    """UI part that handles WGS84 to L-Est97 coordinate converting."""

    def __init__(self, master, tab, validator):
        self.validator = validator

        label_degrees = tk.Label(tab, text="kraadid")
        label_minutes = tk.Label(tab, text="minutid")
        label_seconds = tk.Label(tab, text="sekundid")

        label_lat_text = "".join(map(str, [
            "Põhjalaius (",
            validator.cgs_bounds.min_lat,
            "...",
            validator.cgs_bounds.max_lat,
            ")"
        ]))
        label_lat = tk.Label(tab, text=label_lat_text)
        self.entry_lat_degrees = EntryWithSet(tab)
        self.entry_lat_minutes = EntryWithSet(tab)
        self.entry_lat_seconds = EntryWithSet(tab)

        label_long_text = "".join(map(str, [
            "Idapikkus (",
            validator.cgs_bounds.min_long,
            " ... ",
            validator.cgs_bounds.max_long,
            ")"
        ]))
        label_long = tk.Label(tab, text=label_long_text)
        self.entry_long_degrees = EntryWithSet(tab)
        self.entry_long_minutes = EntryWithSet(tab)
        self.entry_long_seconds = EntryWithSet(tab)

        button_convert = tk.Button(
            tab, text="Arvuta", command=self.convert_to_l_est97
        )

        result_entry_x = tk.Label(tab, text="X (m)")
        result_entry_y = tk.Label(tab, text="Y (m)")
        self.result_label_x = EntryWithSet(tab, state='disabled')
        self.result_label_y = EntryWithSet(tab, state='disabled')

        label_degrees.grid(row=0, column=5, columnspan=2)
        label_minutes.grid(row=0, column=7, columnspan=2)
        label_seconds.grid(row=0, column=9, columnspan=2)
        label_lat.grid(row=1, column=0, columnspan=5, sticky=tk.W)
        self.entry_lat_degrees.grid(row=1, column=5, columnspan=2)
        self.entry_lat_minutes.grid(row=1, column=7, columnspan=2)
        self.entry_lat_seconds.grid(row=1, column=9, columnspan=2)
        label_long.grid(row=3, column=0, columnspan=5, sticky=tk.W)
        self.entry_long_degrees.grid(row=3, column=5, columnspan=2)
        self.entry_long_minutes.grid(row=3, column=7, columnspan=2)
        self.entry_long_seconds.grid(row=3, column=9, columnspan=2)
        button_convert.grid(row=5, column=9, columnspan=2)
        result_entry_x.grid(row=6, column=0, columnspan=3, sticky=tk.E)
        self.result_label_x.grid(row=6, column=3, columnspan=5)
        result_entry_y.grid(row=7, column=0, columnspan=3, sticky=tk.E)
        self.result_label_y.grid(row=7, column=3, columnspan=5)

        self._set_entry_initial_values()

    def _set_entry_initial_values(self):
        self.entry_lat_seconds.value = 0
        self.entry_lat_minutes.value = 0
        self.entry_long_minutes.value = 0
        self.entry_long_seconds.value = 0

    def convert_to_l_est97(self):
        """Convert user provided WGS84 coordinates to L-Est97."""
        lat, is_converted = self.try_get_lat()
        if not is_converted:
            return
        long, is_converted = self.try_get_long()
        if not is_converted:
            return
        wsg98 = WGS84(long, lat)
        result = CoordinateConverter.wgs84_to_l_est97(wsg98)
        self.result_label_x.value = result.x
        self.result_label_y.value = result.y

    def try_get_lat(self):
        """
        Handle user latitude converting to decimal.

        This method also validates that user input is in given range.
        """
        values, is_converted = self._try_get_float_values(
            self.entry_lat_degrees,
            self.entry_lat_minutes,
            self.entry_lat_seconds)
        if not is_converted:
            return 0, False
        degrees, minutes, seconds = values
        validation_result = self.validator.validate_wgs84_latitude_in_degree_minute_second(*values)  # noqa: E501
        decimal_degrees_correct, degrees_correct, minutes_correct, seconds_correct = validation_result  # noqa: E501

        if not decimal_degrees_correct:
            self.entry_lat_degrees.configure(bg="red")
            self.entry_lat_minutes.configure(bg="red")
            self.entry_lat_seconds.configure(bg="red")
            return 0, False
        if not degrees_correct:
            self.entry_lat_degrees.configure(bg="red")
            return 0, False
        if not minutes_correct:
            self.entry_lat_minutes.configure(bg="red")
            return 0, False
        if not seconds_correct:
            self.entry_lat_seconds.configure(bg="red")
            return 0, False
        decimal_degrees = convert_degrees_to_decimal(degrees, minutes, seconds)
        return decimal_degrees, True

    def try_get_long(self):
        """
        Handle user longitude converting to decimal.

        This method also validates that user input is in given range.
        """
        values, is_converted = self._try_get_float_values(
            self.entry_long_degrees,
            self.entry_long_minutes,
            self.entry_long_seconds)
        if not is_converted:
            return 0, False
        degrees, minutes, seconds = values

        validation_result = self.validator.validate_wgs84_longitude_in_degree_minute_second(*values)  # noqa: E501
        decimal_degrees_correct, degrees_correct, minutes_correct, seconds_correct = validation_result  # noqa: E501

        if not decimal_degrees_correct:
            self.entry_long_degrees.configure(bg="red")
            self.entry_long_minutes.configure(bg="red")
            self.entry_long_seconds.configure(bg="red")
            return 0, False
        if not degrees_correct:
            self.entry_long_degrees.configure(bg="red")
            return 0, False
        if not minutes_correct:
            self.entry_long_minutes.configure(bg="red")
            return 0, False
        if not seconds_correct:
            self.entry_long_seconds.configure(bg="red")
            return 0, False
        decimal_degrees = convert_degrees_to_decimal(degrees, minutes, seconds)
        return decimal_degrees, True

    @staticmethod
    def _try_get_float_values(degrees_entry, minutes_entry, seconds_entry):
        float_values = []
        for entry in (degrees_entry, minutes_entry, seconds_entry):
            value, is_converted = try_convert_float(entry.value)
            if not is_converted:
                entry.configure(bg="red")
                return 0, False
            entry.configure(bg="white")
            float_values.append(value)
        return float_values, True


def _create_validator(entry, validator, assign_value_function):
    """
    Create new validator function that validates user input when focus changes.
    :param entry: the entry to validate
    :param validator: method that returns if new value is valid
    :param assign_value_function: callback to bind input value to a variable.
    :return: new validator function
    """

    def validate_value(new_value, event):
        value, is_float = try_convert_float(new_value)
        assign_value_function(value)
        if event != 'focusout':
            return is_float or new_value == ''
        is_valid = validator(value)
        if is_valid:
            entry.configure(bg="white")
        else:
            entry.configure(bg="red")
        return is_valid

    return validate_value


class EntryWithSet(tk.Entry, object):
    """
    tkinter.Entry with properties for getting and setting input values.
    """

    def __init__(self, master=None, cnf={}, **kwargs):
        self.variable = tk.StringVar()
        kwargs["textvariable"] = self.variable
        tk.Entry.__init__(self, master, cnf=cnf, **kwargs)

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, value):
        self.variable.set(str(value))
