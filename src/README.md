# Task Tracker

A small Task Tracker implemented in Python using a JSON file as a simple database.

Files
- `app.py` - simple CLI to interact with tasks
- `tasks.py` - task operations (CRUD) against a JSON file
- `data.json` - default JSON data file (initially empty)
- `requirements.txt` - dependencies for running tests
- `tests/test_tasks.py` - unit tests for task operations

## Features

- **Automatic Timestamp Tracking**: All tasks automatically track creation and modification times
  - `createdAt` - ISO 8601 timestamp when task is created (immutable)
  - `updatedAt` - ISO 8601 timestamp when task is last modified
- **Data Migration**: Existing tasks without timestamps are automatically migrated with default values
- **Due Date Support**: Optional due dates for task scheduling

Quick start

1. (Optional) Create a virtualenv and activate it.
2. Install deps for tests:

```powershell
python -m pip install -r requirements.txt
```

3. Run tests:

```powershell
pytest -q
```

4. Try the CLI:

```powershell
python app.py add "Buy milk" --desc "2 liters"
python app.py list
python app.py update 1 --done true
python app.py get 1
python app.py delete 1
```

## Task Data Structure

Each task is stored as a JSON object with the following fields:

```json
{
  "id": 1,
  "title": "Buy milk",
  "description": "2 liters",
  "done": false,
  "due_date": "2025-11-25",
  "createdAt": "2025-11-20T10:30:00.123456",
  "updatedAt": "2025-11-20T14:45:00.789012"
}
```

### Fields

- `id` (integer): Unique identifier for the task
- `title` (string): Task title
- `description` (string): Task description
- `done` (boolean): Task completion status
- `due_date` (string): Optional due date in YYYY-MM-DD format
- `createdAt` (string): ISO 8601 timestamp of task creation (automatically set, immutable)
- `updatedAt` (string): ISO 8601 timestamp of last modification (automatically updated)
