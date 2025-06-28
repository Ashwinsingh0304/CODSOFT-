import datetime
from tkinter import *
import os

root = Tk()
root.title("To-Do List")
root.geometry("400x650+400+100")
root.resizable(False, False)
root.configure(bg="#2C3E50")
root.option_add("*Font", ("Segoe UI", 12))

task_list = []  # List of tuples (task_text, done)


def format_task_text(task, done):
    return f"[{'✓' if done else ' '}] {task}"


def addTask(task):
    task = task_entry.get()
    task_entry.delete(0, END)

    if task:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        formatted_task = f"{task} ({timestamp})"
        task_list.append((formatted_task, False))
        with open("task.txt", "a") as file:
            file.write(f"{formatted_task}|False\n")
        listbox.insert(END, format_task_text(formatted_task, False))


def save_tasks():
    with open("task.txt", "w") as file:
        for task, done in task_list:
            file.write(f"{task}|{done}\n")


def deleteTask():
    global task_list
    selected_tasks = listbox.curselection()
    if not selected_tasks:
        return
    for index in reversed(selected_tasks):
        task_text = listbox.get(index)
        task = task_text[4:]  # Remove "[✓] " or "[ ] "
        task_list = [t for t in task_list if t[0] != task]
        listbox.delete(index)
    save_tasks()


def toggle_done(event=None):
    global task_list
    selected_tasks = listbox.curselection()
    if not selected_tasks:
        return
    for index in selected_tasks:
        task_text = listbox.get(index)
        task = task_text[4:]  # Remove "[✓] " or "[ ] "
        for i, (t, done) in enumerate(task_list):
            if t == task:
                task_list[i] = (t, not done)
                listbox.delete(index)
                listbox.insert(index, format_task_text(t, not done))
                break
    save_tasks()


def openTaskFile():
    try:
        global task_list
        task_list.clear()
        listbox.delete(0, END)
        if not os.path.exists("task.txt"):
            open("task.txt", "w").close()

        with open("task.txt", "r") as file:
            tasks = file.readlines()
            for i, line in enumerate(tasks):
                if line.strip():
                    parts = line.strip().split("|")
                    task = parts[0]
                    done = parts[1].lower() == "true" if len(parts) > 1 else False
                    task_list.append((task, done))
                    listbox.insert(END, format_task_text(task, done))
                    # Optional alternating row colors
                    if i % 2 == 0:
                        listbox.itemconfig(END, bg="#2F2F3F")
    except Exception as e:
        print("Error loading tasks:", e)


# ---------------------- UI Redesign ----------------------

# Header bar
title_bar = Frame(root, bg="#1F2A36")
title_bar.pack(fill=X)

title_label = Label(title_bar, text="📝 To-Do List", font=("Segoe UI", 20, "bold"), bg="#1F2A36", fg="white", padx=10, pady=10)
title_label.pack(side=LEFT)

# Heading
heading = Label(root, text="Tasks", font=("Segoe UI", 16, "bold"), bg="#2C3E50", fg="#ECECEC")
heading.pack(pady=(10, 5))

# Main Listbox Frame
frame1 = Frame(root, bg="#2C3E50")
frame1.pack(pady=10)

listbox = Listbox(
    frame1, font=("Segoe UI", 13), width=40, height=15,
    bg="#2A2A3A", fg="white", selectbackground="#5A5AFF",
    selectforeground="white", bd=0, highlightthickness=0
)
listbox.pack(side=LEFT, fill=BOTH)

scrollbar = Scrollbar(frame1)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Task Entry + Add Button
frame = Frame(root, bg="#2C3E50")
frame.pack(pady=(0, 15))

task_entry = Entry(frame, width=30, font=("Segoe UI", 14), bd=0, bg="#3B3B4F", fg="white", insertbackground="white", relief=FLAT)
task_entry.grid(row=0, column=0, ipady=7, padx=(0, 8))
task_entry.focus()

add_button = Button(frame, text="➕ Add Task", font=("Segoe UI", 12, "bold"), bg="#00C853", fg="white", bd=0, padx=20, pady=10, activebackground="#00B347", command=lambda: addTask(task_entry.get()))
add_button.grid(row=0, column=1)

# Delete Button
frame2 = Frame(root, bg="#2C3E50")
frame2.pack(pady=(10, 20))

delete_button = Button(frame2, text="🗑 Delete Selected", font=("Segoe UI", 12, "bold"), bg="#E53935", fg="white", bd=0, padx=15, pady=10, activebackground="#C62828", command=deleteTask)
delete_button.pack()

# Bind double click to toggle done
listbox.bind("<Double-Button-1>", toggle_done)

# Load saved tasks
openTaskFile()

# Run app
root.mainloop()
