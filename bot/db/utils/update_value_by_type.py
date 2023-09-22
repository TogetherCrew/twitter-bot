import logging
from datetime import datetime
from typing import Type


def make_val_by_type(
    value: str | datetime | list | int,
    type_val: Type[str] | Type[datetime] | Type[int] | Type[list],
) -> str | int | list:
    """
    In this function, we try to translate value based on the given type
    to which is acceptable for Cypehr in Neo4j

    Parameters:
    ------------
    value : str
        the string value to be converted to a given type of `type_val`
    type_val : str | int | datetime | list
        the value type for the string `value` to be converted

    Returns:
    ----------
    converted_data : str | int | list
        the converted data to be retuernd
        if datetime, the format must match `%Y-%m-%d %H:%M:%S%z`
    """
    converted_data: str | int | list

    if type_val is str:
        try:
            if isinstance(value, str):
                converted_data = value.replace('"', "'")
                converted_data = r'"{}"'.format(converted_data)
            else:
                converted_data = r'"{}"'.format(value)

        except Exception as exp:
            logging.error(exp)
            logging.error("cannot convert to string, defaulting to save empty text")
            converted_data = '""'

    elif type_val is int:
        if isinstance(value, int) or isinstance(value, str):
            converted_data = int(value)
        else:
            logging.error("value must be str or integer if the type_val was datetime!")

    elif type_val is datetime:
        if isinstance(value, datetime):
            converted_data = int(value.timestamp() * 1000)
        else:
            logging.error(
                "value must be a datetime instance if the type_val was datetime!"
            )

    elif type_val is list:
        converted_data = r"{}".format(value)
    elif type_val is bool:
        if value is True or value == "True":
            converted_data = "true"
        elif value is False or value == "False":
            converted_data = "false"
        else:
            logging.warning(
                f"value is not False or True, value: {value}, defaulting to false"
            )
            converted_data = "false"

    return converted_data
