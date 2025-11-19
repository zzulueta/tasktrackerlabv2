import json
import os
from typing import List, Optional, Dict, Any


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
            for item in data:
                if isinstance(item, dict):
                    # ensure new key exists and default to empty string
                    item.setdefault('due_date', "")
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


def list_tasks(path: Optional[str] = None) -> List[Dict[str, Any]]:
    return load_tasks(path)


def create_task(path: str, title: str, description: str = "", due_date: Optional[str] = "") -> Dict[str, Any]:
    tasks = load_tasks(path)
    tid = _next_id(tasks)
    task = {
        "id": tid,
        "title": title,
        "description": description,
        "done": False,
        "due_date": due_date if due_date is not None else "",
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
