"""Property Value Analysis Package.

This package provides tools for analyzing property value data based on
the presence of tall or short trees on streets.

Modules:
    file_parsers:
        Contains classes for extracting and parsing data from various file formats
        (e.g., CSV, JSON).

    property_value_statistics:
        Contains the PropertyValueStatistics class for calculating property value
        averages based on tree data.

Usage:
    from property_value_analysis import PropertyValueStatistics

    property_value_stats = PropertyValueStatistics(property_data, tree_data)
    tall_value_avg = property_value_stats.calculate_average_price_tall_trees()
    short_value_avg = property_value_stats.calculate_average_price_short_trees()
"""
