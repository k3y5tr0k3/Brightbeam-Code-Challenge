"""property_value_statistics.py.

This module provides classes and methods for property value statistics calculations.

Classes:
    PropertyValueStatistics: Handles property value statistics calculations.

Examples:
    Initialize the PropertyValueStatistics with property and tree data:

        property_sales = [
            {
                "Date of Sale (dd/mm/yyyy)": "01/01/2015",
                "Address": "APT 274, THE PARKLANDS, NORTHWOOD",
                "Street Name": "the park",
                "Price": "79500.00"
            },
            {
                "Date of Sale (dd/mm/yyyy)": "01/01/2016",
                "Address": "123 ADELAIDE ROAD",
                "Street Name": "adelaide road",
                "Price": "120000.00"
            }
        ]

        street_trees = {
            "short": {
                "drive": {
                    "abbey": {
                        "abbey drive": 0
                    }
                }
            },
            "tall": {
                "road": {
                    "adelaide": {
                        "adelaide road": 25
                    }
                }
            }
        }

        property_value_stats = PropertyValueStatistics(
            property_sales = property_sales,
            street_trees = street_trees
        )

    Calculate the average property price on streets with tall trees:

        tall_trees_avg = property_value_stats.calculate_average_price_tall_trees()
        print(f"Average price on streets with tall trees: {tall_trees_avg}")

    Calculate the average property price on streets with short trees:

        short_trees_avg = property_value_stats.calculate_average_price_short_trees()
        print(f"Average price on streets with short trees: {short_tree_avg}")
"""

from property_value_analysis.utils.logger import Logger


class PropertyValueStatistics:
    """A class for calculating various property value statistics.

    This class provides methods for calculating statistics related to property
    values, such as the average cost of a property on a street with tall trees and the
    average cost of a property on a street with short trees.

    Attributes:
        property_sales (dict):
            A list of property sales to calculate statistics from. Example of data format:

                property_sales = [
                    {
                        "Date of Sale (dd/mm/yyyy)": "01/01/2015",
                        "Address": "APT 274, THE PARKLANDS, NORTHWOOD",
                        "Street Name": "the park",
                        "Price": "79,500.00"
                    },
                    ...
                ]

        street_trees (dict):
            A dataset containing the height of short and tall trees per street name,
            used for calculating related property value trends. Example dictionary data
            format:

                street_trees = {
                    "short":
                        "drive": {
                            "abbey": {
                                "abbey drive": 0
                            },
                        },
                        ...
                    },
                    "tall": {
                        "road": {
                            "adelaide": {
                                "adelaide road": 25
                            },
                        ...
                    }
                }

    Methods:
        _flatten_street_tree_type(street_trees, tree_type, flattened_street_trees):
            Recursive function to traverse nested dictionaries for a given tree type.

        _flatten_street_trees(street_trees: dict):
            Flattens street tree data and combines streets with both short and tall trees.

        _calculate_average_price(tree_type):
            Calculates the average price of properties on streets with the specified
            tree type.

        calculate_average_price_tall_trees():
            Calculates the average price for properties on streets with tall trees.

        calculate_average_price_short_trees():
            Calculates the average price for properties on streets with short trees.
    """

    def __init__(self, property_sales: list, street_trees: dict) -> None:
        """Default initializer.

        Args:
            property_sales (list):
                A list of dictionaries containing property details (e.g. Street name and
                price).

            street_trees (dict):
                A nested dictionary with heights of tall and short trees by street.
        """
        self.__property_sales = property_sales
        self.__street_trees = self._flatten_street_trees(street_trees)

        self.logger = Logger.get_logger()

    def _flatten_street_tree_type(
        self, street_trees: dict, tree_type: str, flattened_street_trees: dict
    ) -> None:
        """Recursive function to traverse nested dictionaries for a given tree type.

        Recursive function to traverse nested dictionary until height is found, then
        adds this tree type to the street name in `flattened_street_trees` dictionary.
        If the street name doesn't already exist in `flattened_street_trees` it will be
        added.

        Args:
            street_trees (dict):
                A dictionary of streets with trees for a specific tree type.

            tree_type (str):
                The current tree type (e.g.'short' or 'tall').

            flattened_street_trees (dict):
                The dictionary to store flattened street tree data.
        """
        for key, value in street_trees.items():
            if isinstance(value, dict):
                self._flatten_street_tree_type(
                    street_trees=value,
                    tree_type=tree_type,
                    flattened_street_trees=flattened_street_trees,
                )

            else:
                if isinstance(value, int) and value >= 0:
                    if key not in flattened_street_trees:
                        flattened_street_trees[key] = {}
                    flattened_street_trees[key][tree_type] = True

    def _flatten_street_trees(self, street_trees: dict) -> dict:
        """Flattens street tree data and combines streets with both short and tall trees.

        Flattens the street tree data and generates a dictionary with streets as keys
        and tree type booleans. This allows for handling of arbitrary dictionary depths.

        Args:
            street_trees (dict):
                Deeply nested dictionary (of unknown depth) containing tree heights
                categorized e.g. 'short' and 'tall'.

        Returns:
            dict:
                Dictionary with streets as keys and their tree type. Example:
                    ```
                    {
                        "the park": {"short": True},
                        "ventry park": {"short": True, "tall": True},
                        "wolf tone park": {"tall": True},
                        "cambridge road": {"short": True, "tall": True},
                    }
                    ```
        """
        flattened_street_trees = {}

        if street_trees:
            for tree_type, nested_data in street_trees.items():
                self._flatten_street_tree_type(
                    street_trees=nested_data,
                    tree_type=tree_type,
                    flattened_street_trees=flattened_street_trees,
                )

        return flattened_street_trees

    def _calculate_average_price(self, tree_type: str) -> float:
        """Calculates the average price of properties on streets with the specified tree type.

        Args:
            tree_type (str):
                The tree type to calculate the average for (`tall` or `short`).

        Returns:
            float:
                The average property price for streets with the specified tree type.
        """
        total_price = 0
        property_count = 0

        for property in self.__property_sales:
            try:
                if "Price" not in property or "Street Name" not in property:
                    raise KeyError(
                        "Property record is missing required keys ('Price' or 'Street"
                        f"Name'). Property Record: `{property}`."
                    )

                street_name = property.get("Street Name", "").lower()
                price = str(property.get("Price", "0"))
                price = float(price.replace(",", ""))

                if not street_name:
                    raise ValueError(
                        f"Invalid Street Name `{street_name}` in property record."
                    )

                if street_name not in self.__street_trees:
                    raise KeyError(
                        f"Street `{street_name}` not found in street tree data."
                    )

                if tree_type in self.__street_trees.get(street_name):
                    total_price += price
                    property_count += 1

            except (ValueError, KeyError, TypeError) as e:
                self.logger.error(
                    f"Skipping invalid property record: `{property}`. "
                    f"Error Detail: `{str(e)}`"
                )
                continue

        average_price = total_price / property_count if property_count != 0 else 0.0
        return round(average_price, 2)

    def calculate_average_price_tall_trees(self) -> float:
        """Calculates the average price for properties on streets with tall trees.

        Returns:
            float:
                The average property price for streets with tall trees.
        """
        return self._calculate_average_price("tall")

    def calculate_average_price_short_trees(self) -> float:
        """Calculates the average price for properties on streets with short trees.

        Returns:
            float:
                The average property price for streets with short trees.
        """
        return self._calculate_average_price("short")
