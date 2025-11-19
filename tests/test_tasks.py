from src.tasks import load_tasks, create_task


def test_create_task_creates_and_saves(tmp_path):
    path = tmp_path / "tasks.json"
    # create a new task in an empty DB
    task = create_task(str(path), "My Task", "Some description")
    assert isinstance(task, dict)
    assert task["id"] == 1
    assert task["title"] == "My Task"
    assert task["description"] == "Some description"
    assert task["done"] is False
    # due_date default
    assert task["due_date"] == ""

    saved = load_tasks(str(path))
    assert isinstance(saved, list)
    assert len(saved) == 1
    assert saved[0] == task


def test_create_task_increments_id(tmp_path):
    path = tmp_path / "tasks.json"
    # prepare file with existing tasks having ids 2 and 5
    initial_json = '[{"id":2,"title":"t2","description":"d2","done":false}, {"id":5,"title":"t5","description":"d5","done":true}]'
    path.write_text(initial_json, encoding="utf-8")

    new = create_task(str(path), "New Task", "Added")
    # next id should be max(2,5)+1 == 6
    assert new["id"] == 6
    assert new["title"] == "New Task"
    assert new["description"] == "Added"
    assert new["done"] is False
    assert new["due_date"] == ""

    all_tasks = load_tasks(str(path))
    assert len(all_tasks) == 3
    # ensure the new task is present and other tasks preserved
    ids = [t.get("id") for t in all_tasks]
    assert 2 in ids and 5 in ids and 6 in ids


def test_create_task_default_description(tmp_path):
    path = tmp_path / "tasks.json"
    task = create_task(str(path), "NoDesc")
    assert task["id"] == 1
    assert task["title"] == "NoDesc"
    assert task["description"] == ""
    assert task["done"] is False
    assert task["due_date"] == ""

    saved = load_tasks(str(path))
    assert saved[0] == task


def test_create_task_with_invalid_json(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text("not json", encoding="utf-8")
    new = create_task(str(path), "Invalid", "desc")
    assert isinstance(new, dict)
    assert new["id"] == 1
    assert new["title"] == "Invalid"
    assert new["description"] == "desc"
    assert new["done"] is False
    assert new["due_date"] == ""

    saved = load_tasks(str(path))
    assert isinstance(saved, list)
    assert len(saved) == 1
    assert saved[0] == new


def test_create_task_with_non_list_json(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text('{"foo":"bar"}', encoding="utf-8")
    new = create_task(str(path), "ObjRoot", "handled")
    assert new["id"] == 1
    assert new["title"] == "ObjRoot"
    assert new["due_date"] == ""
    saved = load_tasks(str(path))
    assert isinstance(saved, list)
    assert saved[0] == new


def test_create_task_missing_id_fields(tmp_path):
    path = tmp_path / "tasks.json"
    initial = '[{"title":"noid","description":"d","done":false}, {"id":3,"title":"t3","description":"d3","done":false}]'
    path.write_text(initial, encoding="utf-8")

    new = create_task(str(path), "WithMissingIDs", "check")
    # next id should be max(0,3)+1 == 4
    assert new["id"] == 4
    assert new["due_date"] == ""

    all_tasks = load_tasks(str(path))
    assert len(all_tasks) == 3
    # first original entry lacks an id key
    assert all_tasks[0].get("id") is None
    ids = [t.get("id") for t in all_tasks]
    assert 3 in ids and 4 in ids


def test_create_task_creates_parent_dir(tmp_path):
    nested = tmp_path / "nested" / "sub"
    path = nested / "tasks.json"
    # parent dirs don't exist yet
    assert not nested.exists()
    new = create_task(str(path), "MakeDir", "auto")
    assert new["id"] == 1
    assert new["due_date"] == ""
    assert nested.exists()
    saved = load_tasks(str(path))
    assert saved[0] == new


def test_create_task_with_due_date(tmp_path):
    path = tmp_path / "tasks.json"
    new = create_task(str(path), "WithDue", "desc", due_date="2025-11-11")
    assert new["id"] == 1
    assert new["title"] == "WithDue"
    assert new["description"] == "desc"
    assert new["done"] is False
    assert new["due_date"] == "2025-11-11"

    saved = load_tasks(str(path))
    assert saved[0] == new


def test_update_task_updates_due_date(tmp_path):
    from src.tasks import create_task, update_task, load_tasks

    path = tmp_path / "tasks.json"
    orig = create_task(str(path), "Dated", "d")
    # update due_date
    updated = update_task(str(path), orig["id"], due_date="2025-12-01")

    assert isinstance(updated, dict)
    assert updated["id"] == orig["id"]
    assert updated["due_date"] == "2025-12-01"

    saved = load_tasks(str(path))
    assert saved[0] == updated


def test_update_task_ignores_none_due_date(tmp_path):
    from src.tasks import create_task, update_task, load_tasks

    path = tmp_path / "tasks.json"
    orig = create_task(str(path), "Dated2", "d", due_date="2025-11-01")
    res = update_task(str(path), orig["id"], due_date=None)

    assert isinstance(res, dict)
    # due_date should remain unchanged because None values are ignored
    assert res["due_date"] == "2025-11-01"

    saved = load_tasks(str(path))
    assert saved[0]["due_date"] == "2025-11-01"


def test_update_task_updates_and_saves(tmp_path):
    from src.tasks import create_task, update_task, load_tasks

    path = tmp_path / "tasks.json"
    orig = create_task(str(path), "Old Title", "old desc")
    updated = update_task(str(path), orig["id"], title="New Title", done=True)

    assert isinstance(updated, dict)
    assert updated["id"] == orig["id"]
    assert updated["title"] == "New Title"
    assert updated["description"] == "old desc"
    assert updated["done"] is True
    assert updated["due_date"] == ""

    saved = load_tasks(str(path))
    assert isinstance(saved, list)
    assert len(saved) == 1
    assert saved[0] == updated


def test_update_task_returns_none_for_missing_id(tmp_path):
    from src.tasks import create_task, update_task, load_tasks

    path = tmp_path / "tasks.json"
    orig = create_task(str(path), "Only", "one")
    before = load_tasks(str(path))
    res = update_task(str(path), orig["id"] + 1, title="Nope")

    assert res is None
    after = load_tasks(str(path))
    assert after == before


def test_update_task_ignores_none_values(tmp_path):
    from src.tasks import create_task, update_task, load_tasks

    path = tmp_path / "tasks.json"
    orig = create_task(str(path), "KeepTitle", "Desc1")
    res = update_task(str(path), orig["id"], title=None, description="Desc2")

    assert isinstance(res, dict)
    # title should remain unchanged because None values are ignored
    assert res["title"] == "KeepTitle"
    assert res["description"] == "Desc2"
    assert res["due_date"] == ""

    saved = load_tasks(str(path))
    assert saved[0]["title"] == "KeepTitle"
    assert saved[0]["description"] == "Desc2"


def test_update_task_partial_update_preserves_other_tasks(tmp_path):
    from src.tasks import create_task, update_task, load_tasks

    path = tmp_path / "tasks.json"
    t1 = create_task(str(path), "Task1", "d1")
    t2 = create_task(str(path), "Task2", "d2")

    upd = update_task(str(path), t1["id"], description="d1-updated")

    assert isinstance(upd, dict)
    assert upd["id"] == t1["id"]
    assert upd["title"] == "Task1"
    assert upd["description"] == "d1-updated"
    assert upd["due_date"] == ""

    all_tasks = load_tasks(str(path))
    assert len(all_tasks) == 2
    # ensure second task unchanged
    t2_loaded = next(t for t in all_tasks if t.get("id") == t2["id"])
    assert t2_loaded["title"] == "Task2"
    assert t2_loaded["description"] == "d2"
    assert t2_loaded["due_date"] == ""
