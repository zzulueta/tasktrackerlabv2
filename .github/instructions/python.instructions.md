---
applyTo: "**/*.py"
---
# Project Coding Standards for Python

Apply the general coding guidelines to all code.

## Python Guidelines
- **Use Python 3.x** for all new code
- **Follow PEP 8** for code style and formatting
- **Type Hints**: Use type annotations for function parameters and return types
- **Immutability**: Prefer immutable data structures where possible (e.g., tuples instead of lists for fixed data)
- **Error Handling**:
  - Use `try/except` blocks for predictable error handling
  - Avoid bare `except` clauses
- **Imports**:
  - Use absolute imports
  - Group imports: standard library, third-party, local modules
- **Functions & Classes**:
  - Keep functions small and focused
  - Use docstrings for all public functions and classes (see Docstring Guidelines below)
- **Data Structures**:
  - Prefer `dataclasses` for structured data
  - Use `Enum` for fixed sets of constants
- **Logging**:
  - Use the `logging` module instead of `print` for production code
- **Testing**:
  - Write unit tests using `pytest` or `unittest`
  - Aim for high coverage on critical logic
- **Performance**:
  - Use list comprehensions and generator expressions where appropriate
  - Avoid premature optimization; profile before optimizing
- **Security**:
  - Never hardcode secrets; use environment variables or secure vaults
  - Validate external inputs to prevent injection attacks

## Docstring Guidelines
- Follow **PEP 257** conventions for docstrings
- Use **Google style** or **NumPy style** consistently across the project
- Each docstring should include:
  - **Summary line**: A short description of what the function/class/module does
  - **Args**: List all parameters with type and description
  - **Returns**: Describe return type and meaning
  - **Raises**: Document exceptions that may be raised
  - **Examples**: Provide usage examples when helpful
- Example (Google style):

```python
def calculate_area(radius: float) -> float:
    """
    Calculate the area of a circle.

    Args:
        radius (float): The radius of the circle. Must be non-negative.

    Returns:
        float: The computed area of the circle.

    Raises:
        ValueError: If radius is negative.

    Example:
        >>> calculate_area(5)
        78.53981633974483
    """