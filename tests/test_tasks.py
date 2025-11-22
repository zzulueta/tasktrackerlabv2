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


def test_delete_task_removes_existing_task(tmp_path):
    from src.tasks import create_task, delete_task, load_tasks

    path = tmp_path / "tasks.json"
    task = create_task(str(path), "To Delete", "desc")
    
    result = delete_task(str(path), task["id"])
    
    assert result is True
    saved = load_tasks(str(path))
    assert len(saved) == 0


def test_delete_task_returns_false_for_nonexistent_id(tmp_path):
    from src.tasks import create_task, delete_task, load_tasks

    path = tmp_path / "tasks.json"
    task = create_task(str(path), "Exists", "desc")
    before = load_tasks(str(path))
    
    result = delete_task(str(path), task["id"] + 999)
    
    assert result is False
    after = load_tasks(str(path))
    assert after == before


def test_delete_task_preserves_other_tasks(tmp_path):
    from src.tasks import create_task, delete_task, load_tasks

    path = tmp_path / "tasks.json"
    t1 = create_task(str(path), "Keep1", "d1")
    t2 = create_task(str(path), "Delete", "d2")
    t3 = create_task(str(path), "Keep2", "d3")
    
    result = delete_task(str(path), t2["id"])
    
    assert result is True
    saved = load_tasks(str(path))
    assert len(saved) == 2
    ids = [t.get("id") for t in saved]
    assert t1["id"] in ids
    assert t3["id"] in ids
    assert t2["id"] not in ids


def test_delete_task_with_multiple_same_title(tmp_path):
    from src.tasks import create_task, delete_task, load_tasks

    path = tmp_path / "tasks.json"
    t1 = create_task(str(path), "Same", "desc1")
    t2 = create_task(str(path), "Same", "desc2")
    t3 = create_task(str(path), "Same", "desc3")
    
    result = delete_task(str(path), t2["id"])
    
    assert result is True
    saved = load_tasks(str(path))
    assert len(saved) == 2
    ids = [t.get("id") for t in saved]
    assert t1["id"] in ids
    assert t3["id"] in ids
    assert t2["id"] not in ids


def test_delete_task_from_empty_database(tmp_path):
    from src.tasks import delete_task, load_tasks

    path = tmp_path / "tasks.json"
    path.write_text("[]", encoding="utf-8")
    
    result = delete_task(str(path), 1)
    
    assert result is False
    saved = load_tasks(str(path))
    assert len(saved) == 0


def test_delete_task_with_invalid_json(tmp_path):
    from src.tasks import delete_task, load_tasks

    path = tmp_path / "tasks.json"
    path.write_text("invalid json", encoding="utf-8")
    
    result = delete_task(str(path), 1)
    
    assert result is False
    # Should handle gracefully by treating as empty list
    saved = load_tasks(str(path))
    assert isinstance(saved, list)


def test_delete_task_with_non_list_json(tmp_path):
    from src.tasks import delete_task, load_tasks

    path = tmp_path / "tasks.json"
    path.write_text('{"id":1,"title":"task"}', encoding="utf-8")
    
    result = delete_task(str(path), 1)
    
    assert result is False
    saved = load_tasks(str(path))
    assert isinstance(saved, list)
    assert len(saved) == 0


def test_delete_task_first_of_many(tmp_path):
    from src.tasks import create_task, delete_task, load_tasks

    path = tmp_path / "tasks.json"
    t1 = create_task(str(path), "First", "d1")
    t2 = create_task(str(path), "Second", "d2")
    t3 = create_task(str(path), "Third", "d3")
    
    result = delete_task(str(path), t1["id"])
    
    assert result is True
    saved = load_tasks(str(path))
    assert len(saved) == 2
    assert saved[0]["id"] == t2["id"]
    assert saved[1]["id"] == t3["id"]


def test_delete_task_last_of_many(tmp_path):
    from src.tasks import create_task, delete_task, load_tasks

    path = tmp_path / "tasks.json"
    t1 = create_task(str(path), "First", "d1")
    t2 = create_task(str(path), "Second", "d2")
    t3 = create_task(str(path), "Third", "d3")
    
    result = delete_task(str(path), t3["id"])
    
    assert result is True
    saved = load_tasks(str(path))
    assert len(saved) == 2
    assert saved[0]["id"] == t1["id"]
    assert saved[1]["id"] == t2["id"]


def test_delete_task_with_missing_id_field(tmp_path):
    from src.tasks import delete_task, load_tasks

    path = tmp_path / "tasks.json"
    initial = '[{"title":"noid","description":"d","done":false}, {"id":3,"title":"t3","description":"d3","done":false}]'
    path.write_text(initial, encoding="utf-8")
    
    result = delete_task(str(path), 3)
    
    assert result is True
    saved = load_tasks(str(path))
    assert len(saved) == 1
    assert saved[0].get("id") is None
    assert saved[0]["title"] == "noid"


# Edge cases and boundary conditions

def test_delete_task_with_negative_id(tmp_path):
    """Edge case: Negative task ID"""
    from src.tasks import create_task, delete_task, load_tasks

    path = tmp_path / "tasks.json"
    task = create_task(str(path), "Normal", "desc")
    
    result = delete_task(str(path), -1)
    
    assert result is False
    saved = load_tasks(str(path))
    assert len(saved) == 1


def test_delete_task_with_zero_id(tmp_path):
    """Boundary case: Zero ID"""
    from src.tasks import create_task, delete_task, load_tasks

    path = tmp_path / "tasks.json"
    task = create_task(str(path), "Normal", "desc")
    
    result = delete_task(str(path), 0)
    
    assert result is False
    saved = load_tasks(str(path))
    assert len(saved) == 1


def test_delete_task_with_very_large_id(tmp_path):
    """Boundary case: Very large ID number"""
    from src.tasks import create_task, delete_task, load_tasks

    path = tmp_path / "tasks.json"
    task = create_task(str(path), "Normal", "desc")
    
    result = delete_task(str(path), 999999999)
    
    assert result is False
    saved = load_tasks(str(path))
    assert len(saved) == 1


def test_delete_task_single_task(tmp_path):
    """Boundary case: Delete only task in database"""
    from src.tasks import create_task, delete_task, load_tasks

    path = tmp_path / "tasks.json"
    task = create_task(str(path), "Only One", "desc")
    
    result = delete_task(str(path), task["id"])
    
    assert result is True
    saved = load_tasks(str(path))
    assert len(saved) == 0
    assert isinstance(saved, list)


def test_delete_task_preserves_task_order(tmp_path):
    """Edge case: Verify order of remaining tasks is preserved"""
    from src.tasks import create_task, delete_task, load_tasks

    path = tmp_path / "tasks.json"
    tasks = []
    for i in range(1, 11):
        tasks.append(create_task(str(path), f"Task{i}", f"desc{i}"))
    
    # Delete task in the middle
    result = delete_task(str(path), tasks[4]["id"])
    
    assert result is True
    saved = load_tasks(str(path))
    assert len(saved) == 9
    # Verify order is preserved
    expected_titles = [f"Task{i}" for i in range(1, 11) if i != 5]
    actual_titles = [t["title"] for t in saved]
    assert actual_titles == expected_titles


def test_delete_task_with_gaps_in_ids(tmp_path):
    """Edge case: Tasks with non-sequential IDs"""
    from src.tasks import delete_task, load_tasks

    path = tmp_path / "tasks.json"
    # Create tasks with gaps in IDs
    initial = '[{"id":1,"title":"t1","description":"d","done":false}, {"id":10,"title":"t10","description":"d","done":false}, {"id":100,"title":"t100","description":"d","done":false}]'
    path.write_text(initial, encoding="utf-8")
    
    result = delete_task(str(path), 10)
    
    assert result is True
    saved = load_tasks(str(path))
    assert len(saved) == 2
    ids = [t["id"] for t in saved]
    assert 1 in ids
    assert 100 in ids
    assert 10 not in ids


def test_delete_task_multiple_times_same_id(tmp_path):
    """Edge case: Delete same task twice"""
    from src.tasks import create_task, delete_task, load_tasks

    path = tmp_path / "tasks.json"
    task = create_task(str(path), "Delete Twice", "desc")
    
    result1 = delete_task(str(path), task["id"])
    assert result1 is True
    
    result2 = delete_task(str(path), task["id"])
    assert result2 is False
    
    saved = load_tasks(str(path))
    assert len(saved) == 0


def test_delete_task_with_special_characters_in_data(tmp_path):
    """Edge case: Tasks with special characters"""
    from src.tasks import create_task, delete_task, load_tasks

    path = tmp_path / "tasks.json"
    t1 = create_task(str(path), "Normal", "desc")
    t2 = create_task(str(path), "Special: @#$%^&*()", "unicode: 你好 🎉")
    t3 = create_task(str(path), "Quote\"Test", "backslash\\test")
    
    result = delete_task(str(path), t2["id"])
    
    assert result is True
    saved = load_tasks(str(path))
    assert len(saved) == 2
    assert any(t["title"] == "Normal" for t in saved)
    assert any(t["title"] == "Quote\"Test" for t in saved)


def test_delete_task_with_empty_fields(tmp_path):
    """Edge case: Tasks with empty string fields"""
    from src.tasks import create_task, delete_task, load_tasks

    path = tmp_path / "tasks.json"
    t1 = create_task(str(path), "", "")
    t2 = create_task(str(path), "Normal", "desc")
    
    result = delete_task(str(path), t1["id"])
    
    assert result is True
    saved = load_tasks(str(path))
    assert len(saved) == 1
    assert saved[0]["title"] == "Normal"


def test_delete_task_with_malformed_task_structure(tmp_path):
    """Edge case: Task with extra or missing fields"""
    from src.tasks import delete_task, load_tasks

    path = tmp_path / "tasks.json"
    # Some tasks with extra fields, some missing fields
    initial = '[{"id":1,"title":"t1","extra":"field"}, {"id":2,"title":"t2","description":"d2","done":true}, {"id":3}]'
    path.write_text(initial, encoding="utf-8")
    
    result = delete_task(str(path), 2)
    
    assert result is True
    saved = load_tasks(str(path))
    assert len(saved) == 2
    ids = [t.get("id") for t in saved]
    assert 1 in ids
    assert 3 in ids
    assert 2 not in ids


def test_delete_task_preserves_done_status(tmp_path):
    """Edge case: Ensure deletion preserves state of other tasks"""
    from src.tasks import create_task, update_task, delete_task, load_tasks

    path = tmp_path / "tasks.json"
    t1 = create_task(str(path), "Done", "d1")
    update_task(str(path), t1["id"], done=True)
    t2 = create_task(str(path), "ToDelete", "d2")
    t3 = create_task(str(path), "NotDone", "d3")
    
    result = delete_task(str(path), t2["id"])
    
    assert result is True
    saved = load_tasks(str(path))
    assert len(saved) == 2
    task1 = next(t for t in saved if t["id"] == t1["id"])
    assert task1["done"] is True
    task3 = next(t for t in saved if t["id"] == t3["id"])
    assert task3["done"] is False


def test_delete_task_preserves_due_dates(tmp_path):
    """Edge case: Ensure deletion preserves due dates"""
    from src.tasks import create_task, delete_task, load_tasks

    path = tmp_path / "tasks.json"
    t1 = create_task(str(path), "Dated", "d1", due_date="2025-12-01")
    t2 = create_task(str(path), "ToDelete", "d2")
    t3 = create_task(str(path), "Also Dated", "d3", due_date="2025-12-15")
    
    result = delete_task(str(path), t2["id"])
    
    assert result is True
    saved = load_tasks(str(path))
    assert len(saved) == 2
    task1 = next(t for t in saved if t["id"] == t1["id"])
    assert task1["due_date"] == "2025-12-01"
    task3 = next(t for t in saved if t["id"] == t3["id"])
    assert task3["due_date"] == "2025-12-15"


def test_delete_task_with_duplicate_ids(tmp_path):
    """Edge case: Multiple tasks with same ID (corrupted data)"""
    from src.tasks import delete_task, load_tasks

    path = tmp_path / "tasks.json"
    # Corrupted data with duplicate IDs
    initial = '[{"id":5,"title":"t1","description":"d1","done":false}, {"id":5,"title":"t2","description":"d2","done":false}, {"id":6,"title":"t3","description":"d3","done":false}]'
    path.write_text(initial, encoding="utf-8")
    
    result = delete_task(str(path), 5)
    
    assert result is True
    saved = load_tasks(str(path))
    # Should remove all tasks with id=5
    assert len(saved) == 1
    assert saved[0]["id"] == 6
    assert saved[0]["title"] == "t3"


def test_delete_task_with_whitespace_path(tmp_path):
    """Edge case: Path with spaces"""
    from src.tasks import create_task, delete_task, load_tasks

    nested = tmp_path / "folder with spaces"
    nested.mkdir()
    path = nested / "tasks.json"
    
    task = create_task(str(path), "In Spaces", "desc")
    result = delete_task(str(path), task["id"])
    
    assert result is True
    saved = load_tasks(str(path))
    assert len(saved) == 0


def test_delete_task_concurrent_deletes_simulation(tmp_path):
    """Edge case: Simulate multiple sequential deletes"""
    from src.tasks import create_task, delete_task, load_tasks

    path = tmp_path / "tasks.json"
    tasks = []
    for i in range(5):
        tasks.append(create_task(str(path), f"Task{i}", f"desc{i}"))
    
    # Delete all tasks one by one
    for task in tasks:
        result = delete_task(str(path), task["id"])
        assert result is True
    
    saved = load_tasks(str(path))
    assert len(saved) == 0


def test_delete_task_nonexistent_file_path(tmp_path):
    """Edge case: Delete from non-existent file path"""
    from src.tasks import delete_task, load_tasks

    path = tmp_path / "nonexistent" / "tasks.json"
    
    # Should handle gracefully by creating empty DB
    result = delete_task(str(path), 1)
    
    assert result is False
    # Should create the file
    assert path.exists()
    saved = load_tasks(str(path))
    assert len(saved) == 0


# ========================================
# Timestamp Tests (createdAt/updatedAt)
# ========================================

def test_create_task_includes_timestamps(tmp_path):
    """Test that newly created tasks have createdAt and updatedAt timestamps"""
    from src.tasks import create_task
    from datetime import datetime

    path = tmp_path / "tasks.json"
    task = create_task(str(path), "New Task", "Description")
    
    assert "createdAt" in task
    assert "updatedAt" in task
    assert task["createdAt"] is not None
    assert task["updatedAt"] is not None
    
    # Verify timestamps are in ISO 8601 format
    created = datetime.fromisoformat(task["createdAt"])
    updated = datetime.fromisoformat(task["updatedAt"])
    
    # For new tasks, both should be approximately the same
    assert task["createdAt"] == task["updatedAt"]
    assert isinstance(created, datetime)
    assert isinstance(updated, datetime)


def test_create_task_timestamps_are_current(tmp_path):
    """Test that timestamps reflect the current time"""
    from src.tasks import create_task
    from datetime import datetime, timedelta

    path = tmp_path / "tasks.json"
    before = datetime.now()
    task = create_task(str(path), "Test", "Test")
    after = datetime.now()
    
    created = datetime.fromisoformat(task["createdAt"])
    
    # Timestamp should be between before and after
    assert before - timedelta(seconds=1) <= created <= after + timedelta(seconds=1)


def test_update_task_updates_updatedAt_timestamp(tmp_path):
    """Test that updating a task updates the updatedAt timestamp"""
    from src.tasks import create_task, update_task
    from datetime import datetime
    import time

    path = tmp_path / "tasks.json"
    original = create_task(str(path), "Task", "Description")
    original_created = original["createdAt"]
    original_updated = original["updatedAt"]
    
    # Wait a moment to ensure different timestamp
    time.sleep(0.01)
    
    updated = update_task(str(path), original["id"], title="Updated Task")
    
    assert updated is not None
    assert "createdAt" in updated
    assert "updatedAt" in updated
    
    # createdAt should remain unchanged
    assert updated["createdAt"] == original_created
    
    # updatedAt should be different (newer)
    assert updated["updatedAt"] != original_updated
    
    updated_time = datetime.fromisoformat(updated["updatedAt"])
    original_time = datetime.fromisoformat(original_updated)
    assert updated_time > original_time


def test_update_task_preserves_createdAt(tmp_path):
    """Test that createdAt is never modified during updates"""
    from src.tasks import create_task, update_task
    import time

    path = tmp_path / "tasks.json"
    original = create_task(str(path), "Task", "Desc")
    original_created = original["createdAt"]
    
    time.sleep(0.01)
    
    # Multiple updates
    update_task(str(path), original["id"], title="Update 1")
    time.sleep(0.01)
    update_task(str(path), original["id"], description="Update 2")
    time.sleep(0.01)
    final = update_task(str(path), original["id"], done=True)
    
    # createdAt should still be the original
    assert final["createdAt"] == original_created


def test_load_tasks_migrates_existing_tasks_without_timestamps(tmp_path):
    """Test that existing tasks without timestamps get default values"""
    from src.tasks import load_tasks
    from datetime import datetime

    path = tmp_path / "tasks.json"
    
    # Create a task without timestamps (simulating old data)
    old_task_json = '[{"id": 1, "title": "Old Task", "description": "No timestamps", "done": false, "due_date": ""}]'
    path.write_text(old_task_json, encoding="utf-8")
    
    # Load tasks - should trigger migration
    tasks = load_tasks(str(path))
    
    assert len(tasks) == 1
    task = tasks[0]
    
    # Timestamps should be added
    assert "createdAt" in task
    assert "updatedAt" in task
    assert task["createdAt"] is not None
    assert task["updatedAt"] is not None
    
    # Verify timestamps are valid ISO 8601
    created = datetime.fromisoformat(task["createdAt"])
    updated = datetime.fromisoformat(task["updatedAt"])
    assert isinstance(created, datetime)
    assert isinstance(updated, datetime)
    
    # For migrated tasks, both should be the same
    assert task["createdAt"] == task["updatedAt"]


def test_load_tasks_preserves_existing_timestamps(tmp_path):
    """Test that tasks with existing timestamps keep their values"""
    from src.tasks import load_tasks

    path = tmp_path / "tasks.json"
    
    # Create a task with specific timestamps
    existing_created = "2025-01-15T10:30:00.123456"
    existing_updated = "2025-11-19T14:45:00.789012"
    
    task_json = f'[{{"id": 1, "title": "Task", "description": "Desc", "done": false, "due_date": "", "createdAt": "{existing_created}", "updatedAt": "{existing_updated}"}}]'
    path.write_text(task_json, encoding="utf-8")
    
    tasks = load_tasks(str(path))
    
    assert len(tasks) == 1
    task = tasks[0]
    
    # Timestamps should be preserved
    assert task["createdAt"] == existing_created
    assert task["updatedAt"] == existing_updated


def test_timestamps_persist_across_save_load(tmp_path):
    """Test that timestamps are properly saved and loaded"""
    from src.tasks import create_task, load_tasks

    path = tmp_path / "tasks.json"
    
    original = create_task(str(path), "Persistent Task", "Test")
    original_created = original["createdAt"]
    original_updated = original["updatedAt"]
    
    # Load tasks again
    loaded = load_tasks(str(path))
    
    assert len(loaded) == 1
    task = loaded[0]
    
    # Timestamps should match
    assert task["createdAt"] == original_created
    assert task["updatedAt"] == original_updated


def test_multiple_tasks_have_unique_timestamps(tmp_path):
    """Test that tasks created at different times have different timestamps"""
    from src.tasks import create_task
    import time

    path = tmp_path / "tasks.json"
    
    task1 = create_task(str(path), "Task 1", "First")
    time.sleep(0.01)
    task2 = create_task(str(path), "Task 2", "Second")
    
    # Timestamps should be different
    assert task1["createdAt"] != task2["createdAt"]
    assert task1["updatedAt"] != task2["updatedAt"]


def test_timestamp_format_is_iso8601(tmp_path):
    """Test that timestamps are in proper ISO 8601 format"""
    from src.tasks import create_task
    from datetime import datetime
    import re

    path = tmp_path / "tasks.json"
    task = create_task(str(path), "Format Test", "Check format")
    
    # ISO 8601 pattern (simplified check)
    iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'
    
    assert re.match(iso_pattern, task["createdAt"])
    assert re.match(iso_pattern, task["updatedAt"])
    
    # Should be parseable by datetime
    datetime.fromisoformat(task["createdAt"])
    datetime.fromisoformat(task["updatedAt"])
