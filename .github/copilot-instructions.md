# Copilot Instructions for Task Tracker

Welcome to the Task Tracker codebase! This document provides essential guidance for AI coding agents to be productive in this project. Please follow the conventions and workflows outlined below.

## Project Overview

Task Tracker is a Python-based CLI application for managing tasks. It uses a JSON file (`data.json`) as a simple database. The project is structured as follows:

- `src/app.py`: Implements the CLI for interacting with tasks.
- `src/tasks.py`: Contains task operations (CRUD) that interact with the JSON file.
- `src/data.json`: Default JSON data file (initially empty).
- `tests/test_tasks.py`: Unit tests for the `tasks.py` module.

## Developer Workflows

### Setting Up the Environment
1. (Optional) Create and activate a virtual environment.
2. Install dependencies for testing:
   ```powershell
   python -m pip install -r requirements.txt
   ```

### Running Tests
- Use `pytest` to run unit tests:
  ```powershell
  pytest -q
  ```

### Using the CLI
- Example commands:
  ```powershell
  python app.py add "Buy milk" --desc "2 liters"
  python app.py list
  python app.py update 1 --done true
  python app.py get 1
  python app.py delete 1
  ```

## Project-Specific Conventions

- **Task Representation**: Tasks are stored as JSON objects in `data.json`. Each task has fields like `id`, `title`, `description`, and `done`.
- **CLI Commands**: The CLI in `app.py` supports `add`, `list`, `update`, `get`, and `delete` operations. Refer to the `app.py` file for argument details.
- **Testing**: All tests are located in `tests/test_tasks.py`. Ensure new features have corresponding tests.

## Key Patterns and Examples

- **CRUD Operations**: The `tasks.py` module encapsulates all task-related operations. For example, the `add_task` function adds a new task to the JSON file.
- **Error Handling**: The CLI provides user-friendly error messages for invalid inputs. Follow this pattern for new commands.
- **JSON File Interaction**: Use the `json` module to read/write `data.json`. Always ensure file integrity.

## External Dependencies

- The project uses `pytest` for testing. Install it via `requirements.txt`.

## Integration Points

- **CLI and Task Operations**: The CLI in `app.py` directly calls functions from `tasks.py`.
- **Data Storage**: All task data is stored in `data.json`. Ensure backward compatibility when modifying the schema.

---

Feel free to update this document as the project evolves. If any section is unclear or incomplete, please provide feedback for improvement!