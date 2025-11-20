import json
import os
from datetime import datetime
from typing import List, Optional, Dict, Any


def parse_date(date_str: str) -> Optional[str]:
    """
    Parse a date string in various formats and return in YYYY-MM-DD format.
    Supported: MM-DD-YYYY, YYYY-MM-DD, MM/DD/YYYY, DD-MM-YYYY, etc.
    Returns None if invalid.
    """
    if not date_str.strip():
        return None
    
    # List of possible date formats to try
    formats = [
        '%m-%d-%Y',  # MM-DD-YYYY
        '%Y-%m-%d',  # YYYY-MM-DD
        '%m/%d/%Y',  # MM/DD/YYYY
        '%d-%m-%Y',  # DD-MM-YYYY
        '%d/%m/%Y',  # DD/MM/YYYY
        '%Y/%m/%d',  # YYYY/MM/DD
        '%d-%b-%Y',  # DD-Mon-YYYY (e.g., 01-Jan-2023)
        '%b-%d-%Y',  # Mon-DD-YYYY
        '%Y-%b-%d',  # YYYY-Mon-DD
    ]
    
    for fmt in formats:
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            return parsed_date.strftime('%Y-%m-%d')
        except ValueError:
            continue
    
    # If no format matches, return None
    return None


def _default_data_path() -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")


def _ensure_db(path: str) -> None:
    """Ensure the JSON database file and parent directories exist."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump([], f)


def load_tasks(path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Load tasks from the given JSON file. If path is None, use package default."""
    if path is None:
        path = _default_data_path()
    try:
        _ensure_db(path)
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                return []
            # Migrate existing tasks to include timestamps and status
            now = datetime.now().isoformat()
            for item in data:
                if isinstance(item, dict):
                    # ensure new key exists and default to empty string
                    item.setdefault('due_date', "")
                    # Add timestamps if missing (data migration)
                    item.setdefault('createdAt', now)
                    item.setdefault('updatedAt', now)
                    # Add status field if missing (data migration)
                    if 'status' not in item:
                        # Migrate from done boolean: done=True -> 'done', done=False -> 'todo'
                        item['status'] = 'done' if item.get('done', False) else 'todo'
            return data
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_tasks(tasks: List[Dict[str, Any]], path: Optional[str] = None) -> None:
    if path is None:
        path = _default_data_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2)


def _next_id(tasks: List[Dict[str, Any]]) -> int:
    if not tasks:
        return 1
    return max((t.get('id', 0) for t in tasks), default=0) + 1


VALID_STATUSES = ['todo', 'in-progress', 'done']


def list_tasks(path: Optional[str] = None) -> List[Dict[str, Any]]:
    return load_tasks(path)


def list_tasks_by_status(path: Optional[str], status: str) -> List[Dict[str, Any]]:
    """
    List tasks filtered by status.
    
    Args:
        path: Path to the JSON database file
        status: Status to filter by ('todo', 'in-progress', or 'done')
    
    Returns:
        List of tasks matching the specified status
    
    Raises:
        ValueError: If status is not one of the valid values
    """
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status '{status}'. Must be one of: {', '.join(VALID_STATUSES)}")
    
    tasks = load_tasks(path)
    return [task for task in tasks if task.get('status') == status]


def create_task(path: str, title: str, description: str = "", due_date: Optional[str] = "", status: str = "todo") -> Dict[str, Any]:
    tasks = load_tasks(path)
    tid = _next_id(tasks)
    now = datetime.now().isoformat()
    task = {
        "id": tid,
        "title": title,
        "description": description,
        "done": False,
        "status": status,
        "due_date": due_date if due_date is not None else "",
        "createdAt": now,
        "updatedAt": now,
    }
    tasks.append(task)
    save_tasks(tasks, path)
    return task


def get_task(path: str, task_id: int) -> Optional[Dict[str, Any]]:
    tasks = load_tasks(path)
    for t in tasks:
        if t.get('id') == task_id:
            return t
    return None


def update_task(path: str, task_id: int, **kwargs) -> Optional[Dict[str, Any]]:
    tasks = load_tasks(path)
    for i, t in enumerate(tasks):
        if t.get('id') == task_id:
            t_updated = dict(t)
            # ignore keys with value None
            to_update = {k: v for k, v in kwargs.items() if v is not None}
            # allow changing due_date to empty string explicitly
            t_updated.update(to_update)
            # Update the updatedAt timestamp
            t_updated['updatedAt'] = datetime.now().isoformat()
            tasks[i] = t_updated
            save_tasks(tasks, path)
            return t_updated
    return None


def delete_task(path: str, task_id: int) -> bool:
    tasks = load_tasks(path)
    new_tasks = [t for t in tasks if t.get('id') != task_id]
    if len(new_tasks) == len(tasks):
        return False
    save_tasks(new_tasks, path)
    return True
