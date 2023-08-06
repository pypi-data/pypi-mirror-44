from json import loads, dumps

from pandas.io.json import json_normalize
from rest_framework import exceptions, status
from rest_framework.exceptions import APIException


def make_keys_to_dot(d):
    """
    Flattens the dictionary containing other dictionaries like here:
    https://stackoverflow.com/questions/6027558/flatten-nested-python-dictionaries-compressing-keys
    """
    df = json_normalize(d, sep=".")
    return df.to_dict(orient="records")[0]


def does_data_exist_in_generator(doc):
    """
    :param doc: generator obj
    :return: flag
    """
    for _data in doc:
        yield _data
        return True
    return False


def nested_ordered_dict_to_dict(input_ordered_dict):
    return loads(dumps(input_ordered_dict))


def record_not_found_error(message):
    """
    :param message: the message to be printed
    """
    raise exceptions.NotFound(message)


class RequestBodyNotAcceptable(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "Unprocessable Entity"
    default_code = "unprocessable_entity"


