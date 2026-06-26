import os
import json
from datetime import datetime

DATA_FILE = "tasks.txt"

# ─── File Handling ───────────────────────────────────────────────

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)

# ─── Display Helper ──────────────────────────────────────────────

def print_tasks(tasks):
    if not tasks:
        print("  No tasks found.")
        return
    print()
    for i, task in enumerate(tasks, 1):
        status = "✓" if task["done"] else "○"
        title  = task["title"]
        added  = task.get("added", "")
        if task["done"]:
            print(f"  [{i}] {status}  {title}  (added: {added})")
        else:
            print(f"  [{i}] {status}  {title}  (added: {added})")

def get_task_index(tasks, prompt="  Enter task number: "):
    try:
        idx = int(input(prompt).strip()) - 1
        if 0 <= idx < len(tasks):
            return idx
        print("  Invalid task number.")
        return None
    except ValueError:
        print("  Please enter a valid number.")
        return None

# ─── Core Functions ──────────────────────────────────────────────

def add_task(tasks):
    print("\n── Add New Task ──")
    title = input("  Task title: ").strip()
    if not title:
        print("  Task title cannot be empty.")
        return
    tasks.append({
        "title": title,
        "done": False,
        "added": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    save_tasks(tasks)
    print(f"  ✓ Task '{title}' added.")

def view_tasks(tasks):
    print("\n── All Tasks ──")
    print_tasks(tasks)
    total     = len(tasks)
    completed = sum(1 for t in tasks if t["done"])
    pending   = total - completed
    if total:
        print(f"\n  Total: {total}  |  Completed: {completed}  |  Pending: {pending}")

def mark_completed(tasks):
    print("\n── Mark Task as Completed ──")
    print_tasks(tasks)
    idx = get_task_index(tasks)
    if idx is None:
        return
    if tasks[idx]["done"]:
        print(f"  Task '{tasks[idx]['title']}' is already completed.")
        return
    tasks[idx]["done"] = True
    save_tasks(tasks)
    print(f"  ✓ Task '{tasks[idx]['title']}' marked as completed.")

def edit_task(tasks):
    print("\n── Edit Task ──")
    print_tasks(tasks)
    idx = get_task_index(tasks)
    if idx is None:
        return
    current = tasks[idx]["title"]
    new_title = input(f"  New title [{current}]: ").strip()
    if not new_title:
        print("  No changes made.")
        return
    tasks[idx]["title"] = new_title
    save_tasks(tasks)
    print(f"  ✓ Task updated to '{new_title}'.")

def delete_task(tasks):
    print("\n── Delete Task ──")
    print_tasks(tasks)
    idx = get_task_index(tasks)
    if idx is None:
        return
    title = tasks[idx]["title"]
    confirm = input(f"  Delete '{title}'? (y/n): ").strip().lower()
    if confirm == "y":
        tasks.pop(idx)
        save_tasks(tasks)
        print(f"  ✓ Task '{title}' deleted.")
    else:
        print("  Cancelled.")

# ─── Main ────────────────────────────────────────────────────────

def main():
    tasks = load_tasks()

    menu = {
        "1": ("Add new task",           add_task),
        "2": ("View all tasks",          view_tasks),
        "3": ("Mark task as completed",  mark_completed),
        "4": ("Edit task",               edit_task),
        "5": ("Delete task",             delete_task),
        "6": ("Exit",                    None),
    }

    while True:
        print("\n" + "=" * 40)
        print("         ✅ To-Do List")
        print("=" * 40)
        for k, (label, _) in menu.items():
            print(f"  {k}. {label}")

        choice = input("\nEnter choice (1-6): ").strip()

        if choice == "6":
            print("Goodbye!")
            break
        elif choice in menu:
            _, func = menu[choice]
            func(tasks)
        else:
            print("  Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
