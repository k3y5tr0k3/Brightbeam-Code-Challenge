"""Test custom logger module."""

import logging

from property_value_analysis.utils.logger import Logger


class TestLogger:
    """Test Logger class."""

    def test_get_logger(self) -> None:
        """Tests get_logger method.

        Asserts:
            The get_logger() method should return an instance of logging.Logger.
        """
        expected_type = logging.Logger
        logger = Logger.get_logger()

        assert isinstance(logger, expected_type)
