"""Tests for the config utility module."""

import pytest

from property_value_analysis.utils.config import Config


class TestConfig:
    """Test Config class."""

    def test_get_value(self) -> None:
        """Test that a value can be successfully retrieved from config.toml.

        Asserts:
            That the retrieved value is of the correct type.
        """
        key_name = "logging.level"
        expected_type = str

        config_value = Config.get_value(key_name=key_name)

        assert isinstance(config_value, expected_type)

    def test_name_to_list(self) -> None:
        """Test that a config key name is successfully converted to a list of words.

        Asserts:
            A configuration key name is correcting converted into a list on words.
        """
        key_name = "one.two.three"
        expected_value = ["one", "two", "three"]

        actual_value = Config._name_to_list(name=key_name)

        assert actual_value == expected_value

    def test_load_config(self) -> None:
        """Test that the config file can be opened, parsed and returned successfully.

        Asserts:
            - config dictionary is not None or empty.
            - config dictionary is of type `dict`
        """
        expected_type = dict

        config = Config._load_config()

        assert config
        assert isinstance(config, expected_type)

    def test_empty_key_name(self) -> None:
        """Test that Config will raise an error when an empty string is passed as a key name.

        Asserts:
            The test should raise a ValueError if the given key name is an empty string.
        """
        key_name = ""

        with pytest.raises(ValueError):
            Config.get_value(key_name=key_name)

    def test_incomplete_key_name(self) -> None:
        """Test that Config will raise an error when attempting to retrieve a value with an incomplete key name.

        Asserts:
            The test should raise a Value error if the key name is incomplete.
        """
        key_name = "logging"

        with pytest.raises(ValueError):
            Config.get_value(key_name=key_name)
