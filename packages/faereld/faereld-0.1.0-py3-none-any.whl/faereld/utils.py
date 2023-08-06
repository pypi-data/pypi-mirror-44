# -*- coding: utf-8 -*-
"""
faereld.utils
-----------

Various useful static functions and variables for use within Færeld.
"""

import re
from math import floor
from shutil import get_terminal_size
from string import Formatter

from faereld.printer import Highlight, Printer

header = "FÆRELD :: {0} MODE"


def time_diff(from_date, to_date):
    diff_delta = to_date - from_date
    return format_time_delta(diff_delta)


def format_time_delta(time_delta):
    hours, remainder = divmod(time_delta.total_seconds(), 3600)
    minutes = floor(remainder / 60)
    return "{0}h{1}m".format(floor(hours), minutes)


def print_rendered_string(
    area_code, area, date_to_display, object_name, duration, purpose
):
    p = Printer()
    e = get_rendered_string(
        area_code, area, date_to_display, object_name, duration, purpose
    )
    p.add(*e)
    p.print()


def get_rendered_string(
    area_code, area, date_to_display, object_name, duration, purpose
):
    fields = {
        "area": area_code,
        "area_name": area["name"],
        "object": object_name,
        "date": date_to_display,
        "duration": duration,
        "purpose": purpose,
    }
    elements = []
    for literal, field, _, _ in Formatter().parse(area["rendering_string"]):
        if len(literal) > 0:
            elements.append(literal)
        if field is not None:
            if field not in fields:
                raise ValueError(
                    "{0} is an invalid rendering string. ".format(
                        area["rendering_string"]
                    )
                    + "Reason: '{1}' is an invalid field.".format(field)
                )

            elements.append(Highlight(fields.get(field)))
    return elements


def terminal_width():
    return get_terminal_size().columns


def max_width(max_config_width):
    return min(terminal_width(), max_config_width)


def strip_colour_codes(string):
    return re.sub(r"\x1b\[[0-9;]*m", "", string)
