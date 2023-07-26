import json 
import os
import tkinter


def read_tasks(user):
    # Checking if the file exists to avoid errors
    if os.path.isfile("todo.json"):
        
        with open("todo.json", "r") as file:
            try:
                return json.load(file) # Returning the json file
            except json.decoder.JSONDecodeError:
                if user:
                    return "No tasks to show"
                else:
                    return False
    else:
        if user:
            return "No saves"
        else:
            return False


def add_task(task: str):
    default = {"status":False}
    # Checking to see if we should add to an existing file or to add to a new file 
    # with the inserted task.
    if read_tasks(False):
        all_tasks = read_tasks(False)
        all_tasks[task] = default
        # Placing the new data in the json file,
        with open("todo.json", "w") as file:
            json.dump(all_tasks, file)
            print("Task added!")
    else:
        # In the case of the file not existing the program will create a new json file
        # to place the task to.
        print("doesnt exist/empty")
        with open("todo.json", "w") as file:
            print("Creating new save")
            new = {}
            new[task] = default
            json.dump(new, file)
            print("Task added!")


def add_subtask(task,subtask):
    try:
        all_tasks = read_tasks(False)
        all_tasks[task][subtask] = False
        with open("todo.json", "w") as file:
            json.dump(all_tasks, file)
            print("Sub task added successfully!")
    except KeyError:
        print("The specified task doesnt exist")
