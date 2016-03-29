import json
import sys

from .exceptions import DataIsNotJSON


def json_loads(string):
    try:
        return json.loads(string)
    except json.JSONDecodeError as exception:
        exception.args += (('JSON', string),)
        raise DataIsNotJSON(sys.exc_info[:2], value=json)


def json_load(file_):
    try:
        return json.load(file_)
    except json.JSONDecodeError as exception:
        exception.args += (('JSON filename', file_.name),)
        raise DataIsNotJSON(sys.exc_info[:2], value=json, filename=file_.name)
