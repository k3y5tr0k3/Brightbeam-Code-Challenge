"""main.py.

Application entrypoint for standalone execution.

High-level application flow:
    1. Extract property sales data from CSV.
    2. Extract street tree data from JSON.
    3. Initialise PropertyValueStatistics.
    4. Calculate average property value on streets with short trees.
    5. Calculate average property value on streets with tall trees.

Classes:
    Application:
        Handles the high-level execution of the application.

Example:
    Application().run()
"""

import pathlib

from property_value_analysis.utils.logger import Logger
from property_value_analysis.file_parsers import CSVParser, JSONParser
from property_value_analysis.property_value_statistics import PropertyValueStatistics


class Application:
    """This class handles the high-level execution of the application.

    Attributes:
        RAW_STREET_TREES (pathlib.Path):
            JSON file containing street tree data.

        RAW_PROPERTY_SALES (pathlib.Path):
            CSV file containing property sales data.

    Methods:
        run():
            A method for starting and running the standalone application.
    """

    def __init__(self) -> None:
        """Default initializer."""
        base_path = pathlib.Path(__file__).parent
        self.RAW_STREET_TREES = base_path / "../data/dublin-trees.json"
        self.RAW_PROPERTY_SALES = base_path / "../data/dublin-property.csv"

        self.logger = Logger.get_logger()

    def run(self) -> None:
        """This method for starting and running the standalone application.

        This method handles application execution from start to finish for standalone
        usage of this package.
        """
        try:
            csv_parser = CSVParser(filepath=self.RAW_PROPERTY_SALES)
            property_sales = csv_parser.extract()
        except FileNotFoundError or ValueError as e:
            self.logger.critical(
                f"Failed to extract property sales data from CSV file. Message: {e}"
            )
            exit(100)

        try:
            json_parser = JSONParser(filepath=self.RAW_STREET_TREES)
            street_trees = json_parser.extract()
        except FileNotFoundError or ValueError as e:
            self.logger.critical(
                f"Failed to extract street tree data from JSON file. Message: {e}"
            )
            exit(101)

        property_value_stats = PropertyValueStatistics(
            street_trees=street_trees, property_sales=property_sales
        )

        tall_trees_avg_property_value = (
            property_value_stats.calculate_average_price_tall_trees()
        )

        self.logger.info(
            "Average property value on streets with tall trees:"
            f"{tall_trees_avg_property_value}"
        )

        short_trees_avg_property_value = (
            property_value_stats.calculate_average_price_short_trees()
        )

        self.logger.info(
            "Average property value on streets with short trees:"
            f"{short_trees_avg_property_value}"
        )


if __name__ == "__main__":
    Application().run()
