"""Module that handles toml configuration.

Classes:
    Config:
        Handles the retrieval of application configuration variables from the
        config.toml file.

Example:
    Config.get_value(key_name="logging.level")
"""

import pathlib

from property_value_analysis.file_parsers import TOMLParser


class Config:
    """A static class that handles the retrieval of configuration variable from `config.toml`.

    Methods:
        _name_to_list(name):
            Turns a string containing words separated by periods into a list of those
            words.

        _load_config():
            Load the configuration file into a dictionary.

        get(key_name):
            Retrieve a value from the configuration file for a specified key name.
    """

    @staticmethod
    def _name_to_list(name: str) -> list:
        """Turns a string containing words separated by periods into a list of those words.

        Args:
            name (str):
                A string containing words separated by periods. Example:
                `'one.two.three'`.

        Returns:
            list:
                A list of words. Example: `['one', 'two', 'three]`

        Raises:
            ValueError:
                - If key name is an empty string.
                - If the key name contains no words after removing periods.
        """
        if not name:
            raise ValueError("Input string cannot be empty.")

        words = name.rstrip(".").split(".")
        if not words:
            raise ValueError(
                "Input string contains no words after removing trailing periods."
            )

        return words

    @staticmethod
    def _load_config() -> dict:
        """Load the configuration data.

        Returns:
            dict:
                The dictionary representation of the configuration file.
        """
        config_file = pathlib.Path(__file__).parent / "../../config.toml"

        toml_parser = TOMLParser(filepath=config_file)
        return toml_parser.extract()

    @staticmethod
    def get_value(key_name: str) -> any:
        """Retrieve a value from the configuration file for a specified key name.

        Args:
            key_name (str):
                The key name of a particular configuration variable with is a period
                separated path to the variable. Example: `logging.level`.

        Returns:
            any:
                A config variable of any valid Python type (str, int, list, etc).

        Raises:
            KeyError:
                When no configuration variable exists with the specific key name.

            ValueError:
                When the given key name is an incomplete path to a configuration
                variable.
        """
        words = Config._name_to_list(key_name)
        config = Config._load_config()

        try:
            for word in words:
                config = config[word]
        except KeyError:
            raise KeyError(
                f"The given key name `{key_name}` was not found in the config file."
            )

        if not isinstance(config, dict):
            return config
        else:
            raise ValueError("Incomplete name.")
