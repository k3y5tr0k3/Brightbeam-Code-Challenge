"""test_file_parsers.py.

This module contains unit tests for the file parsers. The tests verify that
the parsers correctly handle file reading, data extraction, and error cases.
"""

import pathlib

import pytest

from property_value_analysis.file_parsers import CSVParser, JSONParser, TOMLParser


class TestCSVParser:
    """Test cases for the CSVParser class to validate its behavior."""

    @pytest.fixture
    def valid_csv_file(self) -> pathlib.Path:
        """Fixture to provide a valid CSV file for testing."""
        return pathlib.Path("tests/data/valid.csv")

    @pytest.fixture
    def missing_csv_file(self) -> pathlib.Path:
        """Fixture to provide a missing CSV file for testing."""
        return pathlib.Path("tests/data/missing.csv")

    def test_extract_valid_csv(self, valid_csv_file: pathlib.Path) -> None:
        """Test that the CSVParser correctly extracts data from a valid CSV file.

        Args:
            valid_csv_file (str): Path to the valid CSV file.

        Asserts:
            The data extracted from the CSV file should be a list of dictionaries.
        """
        parser = CSVParser(valid_csv_file)

        data = parser.extract()

        assert isinstance(data, list)
        assert len(data) > 0
        assert isinstance(data[0], dict)

    def test_missing_csv_file(self, missing_csv_file: pathlib.Path) -> None:
        """Test that the CSVParser raises an error when the CSV file is missing.

        Args:
            missing_csv_file (str): Path to the missing CSV file.

        Asserts:
            The test should raise a FileNotFoundError if the file does not exist.
        """
        parser = CSVParser(missing_csv_file)

        with pytest.raises(FileNotFoundError):
            parser.extract()


class TestJSONParser:
    """Test cases for the JSONParser class to validate its behavior."""

    @pytest.fixture
    def valid_json_file(self) -> pathlib.Path:
        """Fixture to provide a valid JSON file for testing."""
        return pathlib.Path("tests/data/valid.json")

    @pytest.fixture
    def missing_json_file(self) -> pathlib.Path:
        """Fixture to provide a missing JSON file for testing."""
        return pathlib.Path("tests/data/missing.json")

    def test_extract_valid_json(self, valid_json_file: pathlib.Path) -> None:
        """Test that the JSONParser correctly extracts data from a valid JSON file.

        Args:
            valid_json_file (str): Path to the valid JSON file.

        Asserts:
            The data extracted from the JSON file should be in a dictionary.
        """
        parser = JSONParser(valid_json_file)
        data = parser.extract()

        # Assert that the extracted data is a dictionary or a list
        assert isinstance(data, (dict, list))
        assert len(data) > 0

    def test_missing_json_file(self, missing_json_file: pathlib.Path) -> None:
        """Test that the JSONParser raises an error when the JSON file is missing.

        Args:
            missing_json_file (str): Path to the missing JSON file.

        Asserts:
            The test should raise a FileNotFoundError if the file does not exist.
        """
        parser = JSONParser(missing_json_file)

        with pytest.raises(FileNotFoundError):
            parser.extract()


class TestTOMLParser:
    """Test cases for the TOMLParser class to validate its behavior."""

    @pytest.fixture
    def valid_toml_file(self) -> pathlib.Path:
        """Fixture to provide a valid TOML file for testing."""
        return pathlib.Path("tests/data/valid.toml")

    @pytest.fixture
    def missing_toml_file(self) -> pathlib.Path:
        """Fixture to provide a missing TOML file for testing."""
        return pathlib.Path("tests/data/missing.toml")

    def test_extract_valid_json(self, valid_toml_file: pathlib.Path) -> None:
        """Test that the TOMLParser correctly extracts data from a valid TOML file.

        Args:
            valid_toml_file (str): Path to the valid TOML file.

        Asserts:
            The data extracted from the TOML file should be in a dictionary.
        """
        parser = TOMLParser(valid_toml_file)
        data = parser.extract()

        assert isinstance(data, (dict, list))
        assert len(data) > 0

    def test_missing_toml_file(self, missing_toml_file: pathlib.Path) -> None:
        """Test that the TOMLParser raises an error when the TOML file is missing.

        Args:
            missing_toml_file (str): Path to the missing TOML file.

        Asserts:
            The test should raise a FileNotFoundError if the file does not exist.
        """
        parser = TOMLParser(missing_toml_file)

        with pytest.raises(FileNotFoundError):
            parser.extract()
