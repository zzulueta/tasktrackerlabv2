# Task Tracker

A tiny, dependency-light Task Tracker implemented in Python that stores tasks in a JSON file. It's designed as a simple learning/demo project and a minimal CLI for personal task management.

- Language: Python
- Storage: JSON file (src/data.json)
- Tests: pytest

## Features
- Add tasks with title and optional description
- List all tasks
- Get a single task by id
- Update task fields (title, description, done)
- Delete tasks
- Unit tests for core logic

## Repository layout
- src/app.py — CLI entrypoint and argument parsing
- src/tasks.py — Business logic: CRUD operations and JSON I/O
- src/data.json — JSON file used as the datastore
- src/README.md — existing short README for the src folder
- tests/test_tasks.py — Unit tests for tasks.py
- requirements.txt — Test dependencies (pytest)

## Quickstart

1. Clone the repository and change into the src directory:
```bash
git clone https://github.com/zzulueta/tasktrackerlabv2.git
cd tasktrackerlabv2/src
```

2. (Optional) Create and activate a virtual environment:
```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

3. Install test dependencies:
```bash
python -m pip install -r requirements.txt
```

4. Run tests:
```bash
pytest -q
```

5. Use the CLI:
```bash
python app.py add "Buy milk" --desc "2 liters"
python app.py list
python app.py update 1 --done true
python app.py get 1
python app.py delete 1
```

(If you prefer running from the repository root, prefix commands with `python src/app.py` and adjust paths accordingly.)

## CLI reference

- Add a task:
```bash
python app.py add "Task title" --desc "optional description" --due "2025-11-25"
```

- List tasks:
```bash
python app.py list
```

- Get a task by id:
```bash
python app.py get <id>
```

- Update a task (example: mark done or set due date):
```bash
python app.py update <id> --done true --due "2025-12-01"
```

- Delete a task:
```bash
python app.py delete <id>
```

See `src/app.py` for the exact argument names and behavior.

## Data model

Tasks are stored as JSON objects in `src/data.json` inside an array. Typical fields:

- id: integer (unique)
- title: string
- description: string
- done: boolean
- due_date: string (optional, format: YYYY-MM-DD)

The current implementation reads the full file into memory, mutates the in-memory structure, and writes the whole file on every change.

Example `src/data.json` entry:
```json
[
  {
    "id": 1,
    "title": "Buy milk",
    "description": "2 liters",
    "done": false,
    "due_date": "2025-11-25"
  }
]
```

## Development notes & suggestions
- The JSON file approach is simple and human-readable but is not safe for concurrent writes. If you need reliability, consider migrating to SQLite or adding:
  - File locking
  - Atomic writes (write to a temp file and rename)
  - A small wrapper around reads/writes to reduce corruption risk
- Add lightweight schema validation (dataclasses, marshmallow, or pydantic) to validate incoming data and simplify tests.
- Improve error handling for malformed or missing `data.json`.
- Add more unit tests to cover edge cases (corrupt data, invalid IDs, and concurrency scenarios).

## Contributing
Contributions are welcome. Suggested workflow:
- Fork the repository
- Create a topic branch for your change
- Add tests for any new behavior
- Open a pull request describing the change and why it's useful

## License
This repository does not include a license file. Add a LICENSE if you plan to reuse or publish the code to clarify usage terms.
