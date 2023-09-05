from datetime import datetime

from bot.db.utils import make_val_by_type


def test_make_value_by_type_input_int():
    value = "5"

    updated_value = make_val_by_type(value, int)

    assert type(updated_value) is int
    assert updated_value == 5


def test_make_value_by_type_input_str():
    value = r"""Happy \}Appl%^&*()_!@#$^"'][e"""

    updated_value = make_val_by_type(value, str)

    assert type(updated_value) is str
    assert updated_value == r"""'Happy \}Appl%^&*()_!@#$^""][e'"""


def test_make_value_by_type_input_str_non_str():
    value = 5

    updated_value = make_val_by_type(value, str)

    assert type(updated_value) is str
    assert updated_value == "5"


def test_make_value_by_type_input_datetime():
    value = "2023-04-16 19:05:38+00:00"

    updated_value = make_val_by_type(value, datetime)

    assert type(updated_value) is int
    assert updated_value == 1681671938000


def test_make_value_by_type_input_list():
    value = ["apple", "banan", "sunshine"]

    updated_value = make_val_by_type(value, list)

    assert type(updated_value) is str
    assert updated_value == str(value)
