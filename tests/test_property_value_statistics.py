"""Unit tests for the PropertyValueStatistics class."""

from property_value_analysis.property_value_statistics import PropertyValueStatistics


class TestPropertyValueStatistics:
    """Unit tests for the PropertyValueStatistics class.

    Attributes:
        property_values (list): A list of property sale records, each containing
            'Street Name', 'Price', and other related data.
        flattened_tree_counts (dict): A dictionary that maps street names to the
            number of tall or short trees on that street.
        property_value_stats (PropertyValueStatistics): An instance of the PropertyValueStatistics
            class initialized with property_values and flattened_tree_counts.
    """

    def setup_method(self) -> None:
        """Setup the test data for each test case."""
        self.property_sales = [
            {
                "Date of Sale (dd/mm/yyyy)": "01/01/2015",
                "Address": "APT 274, THE PARKLANDS, NORTHWOOD",
                "Street Name": "the park",
                "Price": "79500.00",
            },
            {
                "Date of Sale (dd/mm/yyyy)": "12/03/2017",
                "Address": "APT 15, WOODLANDS PARK, SOUTHWOOD",
                "Street Name": "cambridge road",
                "Price": "120000.00",
            },
            {
                "Date of Sale (dd/mm/yyyy)": "25/07/2020",
                "Address": "APT 35, GREENFIELDS, GREENTOWN",
                "Street Name": "ventry park",
                "Price": "150000.00",
            },
        ]

        self.street_trees = {
            "short": {
                "the": {"the park": 10},
                "ventry": {"ventry park": 0},
                "tone": {"wolf": {"wolf tone park": 5}},
            },
            "tall": {
                "road": {
                    "cambridge": {"cambridge road": 20},
                },
                "park": {
                    "ventry": {"ventry park": 20},
                },
            },
        }

        self.property_value_stats = PropertyValueStatistics(
            property_sales=self.property_sales,
            street_trees=self.street_trees,
        )

    def test_average_price_tall_trees(self) -> None:
        """Test for calculating the average price of properties on streets with tall trees.

        Asserts:
            That the correct average property value is calculated for houses on streets
            with tall trees.
        """
        tree_type = "tall"
        expected_avg = 135000.0

        avg_price = self.property_value_stats._calculate_average_price(
            tree_type=tree_type
        )

        assert avg_price == expected_avg

    def test_average_price_short_trees(self) -> None:
        """Test for calculating the average price of properties on streets with short trees.

        Asserts:
            That the correct average property value is calculated for houses on streets
            with short trees.
        """
        tree_type = "short"
        expected_avg = 114750.0

        avg_price = self.property_value_stats._calculate_average_price(
            tree_type=tree_type
        )

        assert avg_price == expected_avg

    def test_flatten_street_trees(self) -> None:
        """Test for flatting street tree data into a lookup dictionary.

        Asserts:
            That the `flatten_street_trees()` method correctly flattens the street tree
            dictionary.
        """
        expected = {
            "the park": {"short": True},
            "ventry park": {"short": True, "tall": True},
            "wolf tone park": {"short": True},
            "cambridge road": {"tall": True},
        }

        actual = self.property_value_stats._flatten_street_trees(
            street_trees=self.street_trees
        )

        assert actual == expected
