import datetime
import tkinter 
from tkinter import *
from PIL import Image, ImageTk
root=Tk()
root.title("To-Do List")
root.geometry("400x650+400+100")
root.resizable(False,False)
root.configure(bg="#2C3E50")  # Professional dark blue-gray
root.option_add("*Font", ("Segoe UI", 12))

task_list = []  # List of tuples (task_text, done)

def format_task_text(task, done):
    return f"[{'✓' if done else ' '}] {task}"

def addTask(task):
    task= task_entry.get()
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
        # Extract task without prefix
        task = task_text[4:]
        # Remove from task_list
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
        task = task_text[4:]
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
        with open("task.txt", "r") as file:
            tasks = file.readlines()
            for line in tasks:
                if line.strip():
                    parts = line.strip().split("|")
                    task = parts[0]
                    done = parts[1].lower() == "true" if len(parts) > 1 else False
                    task_list.append((task, done))
                    listbox.insert(END, format_task_text(task, done))
    except:
        file = open("task.txt", "w")
        file.close()

#icon
#Image_icon = PhotoImage(file="Task1/daily-tasks.png")
#root.iconphoto(False, Image_icon)

#top bar
#TopImage= PhotoImage(file="Task1/horizontal.png")
#Label(root, image=TopImage).pack()


heading = Label(root, text="My Tasks", font=("Helvetica", 24, "bold"), bg="#2C3E50", fg="white")
heading.pack(pady=(20, 10))

#main
frame1 = Frame(root, bg="#2C3E50")
frame1.pack(pady=10)

listbox = Listbox(frame1, font=("Segoe UI", 13), width=40, height=15, bg="#2A2A3A", fg="white", selectbackground="#5A5AFF", selectforeground="white", bd=0, highlightthickness=0)
listbox.pack(side=LEFT, fill=BOTH)

Scrollbar = Scrollbar(frame1)
Scrollbar.pack(side=RIGHT, fill=Y)

listbox.config(yscrollcommand=Scrollbar.set)
Scrollbar.config(command=listbox.yview)

frame = Frame(root, bg="#2C3E50")
frame.pack(pady=(0, 10))

task = StringVar()
task_entry = Entry(frame, width=28, font=("Segoe UI", 16), bd=0, bg="#3B3B4F", fg="white", insertbackground="white", relief=FLAT)
task_entry.grid(row=0, column=0, ipady=8, padx=(0, 10))
task_entry.focus()

button = Button(frame, text="Add", font=("Segoe UI", 12, "bold"), bg="#00C853", fg="white", bd=0, padx=20, pady=10, activebackground="#00B347", command=lambda: addTask(task_entry.get()))
button.grid(row=0, column=1)

openTaskFile()

#delete
# Resize delete button image to smaller size
delete_img = Image.open("Task1/delete.png")
delete_img = delete_img.resize((50, 60), Image.LANCZOS)
Delete_icon = ImageTk.PhotoImage(delete_img)

frame2 = Frame(root, bg="#2C3E50")
frame2.pack(pady=(10, 20))

delete_button = Button(frame2, image=Delete_icon, bd=0, bg="#2C3E50", activebackground="#2C3E50", command=deleteTask)
delete_button.pack()

# Bind double click on listbox to toggle done status
listbox.bind("<Double-Button-1>", toggle_done)

root.mainloop()