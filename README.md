# Do more trees mean more money?

#### This package is a submission to the Brightbeam Software Engineer coding assessment

Developed by [Bryan Donnelly](https://www.linkedin.com/in/bryan-donnelly-/)

## Package Description

[![Language - Python](https://img.shields.io/static/v1?label=Language&message=Python&color=green&logo=python)](https://www.python.org/) ![Python Version - >= 3.12](https://img.shields.io/static/v1?label=Python+Version&message=>%3D+3.12&color=Green) [![Code Style - Black](https://img.shields.io/static/v1?label=Code+Style&message=Black&color=black)](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)

This package can be executed as a standalone console application or can be installed as a dependency to another application

It takes two files as input data ([Dublin Property Values](./data/dublin-property.csv) and [Dublin Street Tree Count](./data/dublin-trees.json)) and outputs the average cost of a property:

- on a street with tall trees
- on a street with short trees

## Challenge Specification

The full details of the challenge and its requirements can be found in [challenge.txt](./challenge.txt)

## Stated Reasons for Rejection

- Test are too complicated (I disagree)
- Issues with error handling (No further explanation was provided)

## Usage

To execute the application, navigate to the project root directory, and run the following command (there are no external dependencies):

```bash
python3 -m property_value_analysis.main
```

Example output:

```
[2025-01-10 17:37:00,060][INFO][main.py:82] - Average property value on streets with tall trees:587800.39
[2025-01-10 17:37:00,064][INFO][main.py:91] - Average property value on streets with short trees:488981.66
```


## Testing Instructions

1. Create a Python virtual environment. Navigate to the root project directory via the commandline and run the following command:

    ```bash
    python3 -m venv venv
    ```

2. Activate the newly created virtual environment:

- Linux
    ```bash
    source ./venv/bin/activate
    ```

- Windows

    - Command Prompt
        ```
        venv\Scripts\activate
        ```

    - Powershell
        ```
        .\venv\Scripts\Activate
        ```

3. Install test dependencies:

    ```bash
    pip install -r dev-requirements.txt
    ```

4. Run unit tests with PyTest (PyTest is preconfigured via [pyproject.toml](./pyproject.toml))

    ```bash
    pytest
    ```

5. (Optional) Run Ruff to ensure code strictly adheres to code style guidelines (Ruff is preconfigured via [pyproject.toml](./pyproject.toml))

    ```bash
    ruff check
    ```

## Developer Notes

### Design Notes

#### Loosely-coupled code

This project is designed to be loosely coupled. This is evidenced by its modular design, where each component (e.g., parsers, statistics calculations) has a clear, independent responsibility. It promotes flexibility and extensibility, allowing new features to be added without impacting existing components, and supports easy testing of individual parts.

#### Error Handling

Overall this project employs a fail-fast error-handling approach, ensuring that issues are detected and reported immediately when they occur. This minimizes debugging time and promotes robust, reliable code by addressing problems as early as possible in the application flow. 

When an error is raised, one of two things will happen:

1. The application will stop. For example, when input data is missing or when that data is invalid or corrupted. This is because the application cannot continue with no input data, we should inform the user of the details of this failure and stop the application.

2. Where it is appropriate, the application will skip parts of the data that are invalid/missing, but continue execution of the remaining valid data. The application should also inform the user about the details of the missing or invalid data (in this project's case via a log message). For example, with software that is designed to auto-fill form data, we should fill in as much of that data as possible and inform the user of any form fields that we where unable to fill.

#### Dependencies

This project follows a minimal dependency approach, separating production dependencies from development and testing dependencies. This ensures a lightweight, efficient production environment while maintaining flexibility for development and testing workflows.

#### Testing

This project follows the Arrange, Act, Assert testing methodology to ensure clear and structured test cases. Each test is organized into distinct sections for setup, execution, and verification, making it easy to understand and maintain.

#### Zen of Python

This project closely adheres to the Zen of Python by prioritizing simplicity, readability, and explicitness in its design and implementation. It embraces clarity and avoids unnecessary complexity, making the code intuitive, maintainable, and Pythonic.

To view the Zen of Python (by Tim Peters) simply run the following command:

```bash
python3 -m this
```

#### Google Docstring Style

This project uses Google-style docstrings to ensure consistency and clarity in documentation. The format provides a structured and readable way to describe modules, classes, and functions, enhancing maintainability and ease of understanding for developers.

#### Key Optimizations

1. Preprocessing the Tree Count Data:

    The `_flatten_street_trees` method creates a flattened dictionary (tree_lookup) that maps each street name to its tree type (tall or short). This eliminates the need for nested loops during property processing.
    Example of flattened street tree data:

    ```python
    {
        "the park": {"short": True,},
        "ventry park": {"tall": True},
        "cambridge road": {"short": True, "tall": True},
        ...
    }
    ```

2. Single Pass for Property Values:

    The `_calculate_average_price` method iterates through property_values only once, using the `tree_lookup()` method of the `dict` type, for $O(1)$ street name matching.
    It calculates the sum and count of matching properties on the fly, minimizing memory overhead.

3. Avoiding Temporary Lists:

    The implementation directly sums and counts values without creating intermediate lists, reducing memory usage.

#### Complexity Analysis

- Preprocessing:

    Flattening the tree data: $O(n)$, where $n$ is the total number of streets.
    
    Memory usage: A single dictionary for street lookups.

- Runtime:

    Calculating averages: $O(m)$, where $m$ is the number of properties.
    Overall, the solution is $O(n+m)$, which is highly efficient.


