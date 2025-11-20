import argparse
import json
import os
from datetime import datetime
from tasks import list_tasks, list_tasks_by_status, create_task, get_task, update_task, delete_task

DEFAULT_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")


def main():
    parser = argparse.ArgumentParser(description="Simple Task Tracker CLI")
    sub = parser.add_subparsers(dest="cmd")

    list_cmd = sub.add_parser("list", help="List all tasks")
    list_cmd.add_argument("--status", choices=["todo", "in-progress", "done"], help="Filter tasks by status")

    add = sub.add_parser("add", help="Add a task")
    add.add_argument("title")
    add.add_argument("--desc", default="", help="Task description")
    add.add_argument("--due", help="Due date (YYYY-MM-DD)")

    get = sub.add_parser("get", help="Get task by id")
    get.add_argument("id", type=int)

    upd = sub.add_parser("update", help="Update task by id")
    upd.add_argument("id", type=int)
    upd.add_argument("--title")
    upd.add_argument("--desc")
    upd.add_argument("--done", choices=["true", "false"])
    upd.add_argument("--due", help="Due date (YYYY-MM-DD)")

    rm = sub.add_parser("delete", help="Delete task by id")
    rm.add_argument("id", type=int)

    parser.add_argument("--db", default=DEFAULT_DB, help="Path to JSON data file")

    args = parser.parse_args()

    db = args.db

    if args.cmd == "list":
        if args.status:
            tasks = list_tasks_by_status(db, args.status)
            print(f"Tasks with status '{args.status}': {len(tasks)}")
        else:
            tasks = list_tasks(db)
        print(json.dumps(tasks, indent=2))
    elif args.cmd == "add":
        if args.due:
            try:
                datetime.strptime(args.due, "%Y-%m-%d")
            except ValueError:
                print("Invalid due date format. Use YYYY-MM-DD")
                return
        t = create_task(db, args.title, args.desc, due_date=args.due)
        print("Created:", json.dumps(t, indent=2))
    elif args.cmd == "get":
        t = get_task(db, args.id)
        print(json.dumps(t, indent=2) if t else "Not found")
    elif args.cmd == "update":
        kwargs = {}
        if args.title is not None:
            kwargs['title'] = args.title
        if args.desc is not None:
            kwargs['description'] = args.desc
        if args.done is not None:
            kwargs['done'] = args.done == 'true'
        if args.due is not None:
            if args.due == "":
                # explicit empty string clears due date
                kwargs['due_date'] = ""
            else:
                try:
                    datetime.strptime(args.due, "%Y-%m-%d")
                except ValueError:
                    print("Invalid due date format. Use YYYY-MM-DD")
                    return
                kwargs['due_date'] = args.due
        t = update_task(db, args.id, **kwargs)
        print(json.dumps(t, indent=2) if t else "Not found")
    elif args.cmd == "delete":
        ok = delete_task(db, args.id)
        print("Deleted" if ok else "Not found")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
