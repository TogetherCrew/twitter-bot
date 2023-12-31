from datetime import datetime

from bot.db.utils.update_value_by_type import make_val_by_type


def test_make_value_by_type_input_int():
    value = "5"

    updated_value = make_val_by_type(value, int)

    assert isinstance(updated_value, int)
    assert updated_value == 5


def test_make_value_by_type_input_str():
    value = r"""Happy \}Appl%^&*()_!@#$^"'][e"""

    updated_value = make_val_by_type(value, str)

    assert isinstance(updated_value, str)
    expected_value = r""""Happy \}Appl%^&*()_!@#$^''][e" """
    expected_value = expected_value[:-1]
    assert updated_value == expected_value


def test_make_value_by_type_input_str_non_str():
    value = 5

    updated_value = make_val_by_type(value, str)

    assert isinstance(updated_value, str)
    assert updated_value == '"5"'


def test_make_value_by_type_input_datetime():
    value = datetime.strptime("2023-04-16 19:05:38+00:00", "%Y-%m-%d %H:%M:%S%z")

    updated_value = make_val_by_type(value, datetime)

    assert isinstance(updated_value, int)
    assert updated_value == 1681671938000


def test_make_value_by_type_input_list():
    value = ["apple", "banan", "sunshine"]

    updated_value = make_val_by_type(value, list)

    assert isinstance(updated_value, str)
    assert updated_value == str(value)


def test_make_value_by_type_input_bool_true():
    value = True

    updated_value = make_val_by_type(value, bool)

    assert isinstance(updated_value, str)
    assert updated_value == "true"


def test_make_value_by_type_input_bool_false():
    value = False

    updated_value = make_val_by_type(value, bool)

    assert isinstance(updated_value, str)
    assert updated_value == "false"


def test_make_value_by_type_input_bool_string_true():
    """
    in case of no valid input the results should be "false"
    """
    value = "True"

    updated_value = make_val_by_type(value, bool)

    assert isinstance(updated_value, str)
    assert updated_value == "true"


def test_make_value_by_type_input_bool_string_false():
    """
    in case of no valid input the results should be "false"
    """
    value = "False"

    updated_value = make_val_by_type(value, bool)

    assert isinstance(updated_value, str)
    assert updated_value == "false"


def test_make_value_by_type_input_bool_no_valid_input():
    """
    in case of no valid input the results should be "false"
    """
    value = "samplesample"

    updated_value = make_val_by_type(value, bool)

    assert isinstance(updated_value, str)
    assert updated_value == "false"
