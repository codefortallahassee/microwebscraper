import json
import sys
from collections import Sequence

import jsonschema
import lxml.html

from .exceptions import NotValidJSON, JSONDataValidationError
from .htmltidy import normalize_space


def json_loads(string):
    try:
        return json.loads(string)
    except json.JSONDecodeError as exception:
        exception.args += (('JSON', string),)
        raise NotValidJSON(sys.exc_info()[:2], value=json)


def json_load(file_):
    try:
        return json.load(file_)
    except json.JSONDecodeError as exception:
        exception.args += (('JSON filename', file_.name),)
        raise NotValidJSON(sys.exc_info()[:2], value=json,
                           filename=file_.name)


def validate_json(json_data, json_schema, filename=None):
    try:
        jsonschema.validate(json_data, json_schema)
    except jsonschema.exceptions.ValidationError:
        raise JSONDataValidationError(sys.exc_info()[:2], value=json_data,
                                      filename=filename)


def get_validated_json(json_file, schema_file):
    validate_json(json_load(json_file), json_load(schema_file),
                  filename=json_file.name)


def dump_value(value, tidy=False):
    "convert HtmlElement to string"
    if isinstance(value, str):
        return normalize_space(value) if tidy else value
    if isinstance(value, lxml.html.HtmlElement):
        return '[{}]'.format(value.tag)
    if isinstance(value, Sequence):
        if value:
            if all(isinstance(v, lxml.html.HtmlElement) for v in value):
                tags = [v.tag for v in value]
                if len(set(tags)) == 1:
                    return '[<{}>] * {}'.format(tags[0], len(tags))
                return '[{}]'.format(['<{}>'.format(t) for t in tags])
    return repr(value)


def dump_config(data, tidy):
    return {k: [dump_config(i, tidy) for i in v] if v and
            isinstance(v, Sequence) and all(isinstance(i, dict) for i in v)
            else dump_value(v, tidy) for k, v in data.items()}


def dump_json(data, indent=4, tidy=False, sort_keys=True):
    print('tidy', tidy)
    try:
        if normalize_space:
            raise TypeError
        return json.dumps(data, indent=indent, sort_keys=sort_keys)
    except TypeError:
        try:
            config = dump_config(data, tidy)
            return json.dumps(config, indent=indent, sort_keys=sort_keys)
        except TypeError:
            return repr(data)
