# Task Tracker

A small Task Tracker implemented in Python using a JSON file as a simple database.

Files
- `app.py` - simple CLI to interact with tasks
- `tasks.py` - task operations (CRUD) against a JSON file
- `data.json` - default JSON data file (initially empty)
- `requirements.txt` - dependencies for running tests
- `tests/test_tasks.py` - unit tests for task operations

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
