"""file_parsers.py.

This module provides classes and methods to extract and parse data from various
file formats. It is designed to provide a unified interface for data extraction.

Classes:
    CSVParser:
        Handles extraction of data from CSV files.

    JSONParser:
        Handles extraction of data from JSON files.

Example:
    Extract data from a CSV file:
        csv_parser = CSVParser("data.csv")
        csv_data = extractor.extract()

    Extract data from a JSON file:
        json_parser = JSONParser("data.json")
        json_data = json_parser.extract()
"""

import abc
import csv
import json
import pathlib
import tomllib


class FileParser(abc.ABC):
    """Abstract base class for data extraction and parsing.

    Defines the interface for data extraction from various file formats.
    """

    @abc.abstractmethod
    def extract(self) -> any:
        """Extracts data from the source file.

        Returns:
            Data (varies by implementation):
                Extracted data.
        """
        ...


class CSVParser(FileParser):
    """A class for extracting data from CSV files.

    This class provides functionality to extract data from a given CSV file and
    return it in a structured format (i.e., a list of dictionaries).

    Attributes:
        filepath (str):
            The path to the CSV file to be parsed.

    Methods:
        extract():
            Reads the CSV file and returns the extracted data as a list of
            dictionaries, where each dictionary represents a row.
    """

    def __init__(self, filepath: pathlib.Path) -> None:
        """Default initializer.

        Args:
            filepath (pathlib.Path):
                Absolute path to the CSV file
        """
        self.filepath = filepath

    def extract(self) -> list:
        """Extracts data from the CSV file.

        Reads the CSV file located at `self.filepath`, parses it, and returns the data
        as a list of dictionaries, where each dictionary represents a row in the CSV
        file. The keys of the dictionary are the column headers from the CSV file.

        Returns:
            list of dict:
                A list where each dictionary represents a row from the CSV file, with
                column headers as keys.

        Raises:
            FileNotFoundError:
                If the CSV file at the given filepath does not exist.

            ValueError:
                If the CSV file is empty or cannot be read correctly.
        """
        data = []

        try:
            with open(self.filepath, mode="r", errors="ignore") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)

        except FileNotFoundError:
            raise FileNotFoundError(
                f"The CSV file at `{self.filepath}` could not be found."
            )

        except csv.Error as e:
            raise csv.Error(f"Error: `{e}`")

        return data


class JSONParser(FileParser):
    """A class for extracting data from JSON files.

    This class provides functionality to extract data from a given JSON file and
    return it in a structured format (i.e., a dictionary or a list).

    Attributes:
        filepath (str):
            The path to the JSON file to be parsed.

    Methods:
        extract():
            Reads the JSON file and returns the extracted data as a dictionary or a
            list.
    """

    def __init__(self, filepath: str) -> None:
        """Initializes the JSONParser with the given file path.

        Args:
            filepath (str):
                The path to the JSON file to be parsed.
        """
        self.filepath = filepath

    def extract(self) -> list | dict:
        """Extracts data from the JSON file.

        Reads the JSON file located at `self.filepath`, parses it, and returns
        the data in its structured form (dictionary or list depending on JSON content).

        Returns:
            dict or list:
                The parsed data from the JSON file.

        Raises:
            FileNotFoundError:
                If the JSON file at the given filepath does not exist.

            ValueError:
                If the JSON file is invalid or cannot be read correctly.
        """
        try:
            with open(self.filepath, mode="r", encoding="utf-8") as file:
                data = json.load(file)

                if not data:
                    raise ValueError(
                        f"Parsing the JSON file at `{self.filepath}` resulted in an"
                        "empty data set."
                    )

        except FileNotFoundError:
            raise FileNotFoundError(
                f"The file at `{self.filepath}` could not be found."
            )

        except ValueError as e:
            raise ValueError(f"Error: `{e}`")

        except json.JSONDecodeError as e:
            raise ValueError(f"Error: `{e}`")

        return data


class TOMLParser(FileParser):
    """A class for extracting data from TOML files.

    This class provides functionality to extract data from a given TOML file and
    return it in a structured format (i.e., a dictionary).

    Attributes:
        filepath (str):
            The path to the TOML file to be parsed.

    Methods:
        extract():
            Reads the TOML file and returns the extracted data as a dictionary.
    """

    def __init__(self, filepath: pathlib.Path) -> None:
        """Default initializer.

        Args:
            filepath (pathlib.Path):
                Absolute path to the TOML file
        """
        self.filepath = filepath

    def extract(self) -> list:
        """Extracts data from the TOML file.

        Reads the TOML file located at `self.filepath`, parses it, and returns the data
        as a dictionary..

        Returns:
            dict:
                A dictionary representation of a TOML file.

        Raises:
            FileNotFoundError:
                If the TOML file at the given filepath does not exist.

            ValueError:
                If the TOML file is empty or cannot be read correctly.
        """
        data = {}

        if self.filepath.exists():
            try:
                with open(self.filepath, "rb") as f:
                    data = tomllib.load(f)

                if not data:
                    raise ValueError(f"TOML file at `{self.filepath}` is empty.")

            except tomllib.TomlDecodeError as e:
                raise tomllib.TomlDecodeError(
                    f"Error decoding TOML file at `{self.filepath}`."
                    f"Error message: `{e}`"
                )

        else:
            raise FileNotFoundError(
                f"The TOML file at `{self.filepath}` doesn't exist."
            )

        return data
