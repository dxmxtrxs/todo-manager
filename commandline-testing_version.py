#--------------------------===================IMPORTS===================--------------------------

import json 
import os

#-------------------------===================FUNCTIONS===================-------------------------


def rename(old,new):
    # Getting the tasks from the JSON file
    tasks = read_tasks()
    # checking if the user is trying to replace the old task name with the same task name 
    if old != new:
        # Replacing the task name
        value = tasks[old]
        tasks[new] = value
        # Deleting the old task name
        del tasks[old]
        # Writing back to the JSON file
        with open("todo.json", "w") as file:
            json.dump(tasks, file)
        print("[Main/Select/Rename] ~ Task renamed successfully!")
    else:
        # Printing an error in the case of both names being the same
        print("[Main/Select/Rename] ~ Name can't be the same.")


def show(dictionary):
    try:
        reveal = show_mode(dictionary)
        if reveal:
            print_table(dictionary)
        else:
            print_table_no_sub(dictionary)
    except:
        print("[Main] ~ No tasks!")

# Used to print tasks when we know there are sub-tasks
def print_table(data_dict):
    try:
        # Calculate the maximum width for each category
        max_task_width = max(len(key) for key in data_dict)
        max_status_width = max(len(str(value["status"])) for value in data_dict.values())

        # Calculate the maximum width for subtasks based on the longest subtasks string in each row
        max_subtasks_width = max(
            len(", ".join([f"{subtask}: {'Uncompleted' if not value[subtask] else 'Completed'}" for subtask in value if subtask != "status"]))
            for key, value in data_dict.items()
        )

        # Calculate the total width of the table
        total_width = max_task_width + max_status_width + max_subtasks_width + 11

        # Print the table header
        header = f"| {'Task':^{max_task_width}} | {'Status':^{max_status_width}} |"
        if max_subtasks_width > 0:
            header += f" {'Subtasks':^{max_subtasks_width}}|"
        line = "+" + "-" * (total_width - 2) + "+"
        print(line)
        print(header)
        print(line)

        # Print each row in the table
        for key, value in data_dict.items():
            task = key.ljust(max_task_width)
            if value["status"] == False:
                result = "❌"
            else:
                result = "✅"
            task_status = result.center(max_status_width + 1)

            subtasks_list = [
                f"{subtask}: {'❌' if not value[subtask] else '✅'}"
                for subtask in value if subtask != "status"
            ]
            subtasks_str = ", ".join(subtasks_list)

            if not subtasks_list:
                subtasks_str = "None".center(max_subtasks_width - 1)

            print(f"| {task} | {task_status} | {subtasks_str:<{max_subtasks_width - 2}} |")
        
        # Print the table footer
        print(line)
    except:
        print("No tasks")


# Used to print tasks when we know there are sub-tasks
def print_table_no_sub(data_dict):
    try:
        # Calculate the maximum width for each category
        max_task_width = max(len("Task"), max(len(key) for key in data_dict))
        max_status_width = max(len("Status"), max(len(str(value["status"])) for value in data_dict.values()))

        # Calculate the total width of the table
        total_width = max_task_width + max_status_width + 7

        # Print the table header
        header = f"| {'Task':^{max_task_width}} | {'Status':^{max_status_width}} |"
        line = "+" + "-" * (total_width - 2) + "+"
        print(line)
        print(header)
        print(line)

        # Print each row in the table
        for key, value in data_dict.items():
            task = key.ljust(max_task_width)
            if value["status"] == False:
                result = "❌"
            else:
                result = "✅"
            task_status = result.center(max_status_width)

            print(f"| {task} | {task_status}|")
        
        # Print the table footer
        print(line)
    except:
        print("No tasks")


# Used to find if there are any sub-tasks  
def show_mode(data_dict):
    try:
        # Iterate over the keys of the outer dictionary
        for key in data_dict.keys():
            # Iterate over the keys of the nested dictionary for each outer key
            for k in data_dict[key]:
                # Check if the current key in the nested dictionary is not "status"
                if k != "status":
                    # If a key other than "status" is found, return True immediately
                    return True
                else:
                    # If the key is "status", do nothing and continue iterating the next key in the nested dictionary
                    pass
        # If no key other than "status" is found in any nested dictionary, return False
        return False
    except:
        # If any error occurs during iteration (e.g., data_dict is not a valid dictionary), return False
        return False


def print_subtasks(data_dict, key):
    #  Checking if the key (task) exists in the data_dict
    if key in data_dict:
        # Getting the value (task details) associated with the key
        value = data_dict[key]
        # Creating a list of subtasks with their completion status
        subtasks_list = [
            f"{subtask}: {'Uncompleted' if not value[subtask] else 'Completed'}\n"
            for subtask in value if subtask != "status"
        ]
        # Check if there are any subtasks for the given task
        if subtasks_list:
            # Print the subtasks as a comma-separated string
            print(f"\nAll sub-tasks in {selected}:")
            print("".join(subtasks_list))
        else:
            # If there are no subtasks, print a message indicating that
            print(f"[Main/Select] Task '{key}' has no sub-tasks.")
    else:
        # If the key (task) is not found in the data_dict, print an error message
        print(f"[Main/Select] Task '{key}' not found in the data.")


def read_tasks():
    # Checking if the file exists to avoid errors
    if os.path.isfile("todo.json"):
        
        with open("todo.json", "r") as file:
            try:
                return json.load(file) # Returning the json file
            except json.decoder.JSONDecodeError:
                    return False
    else:
        return False


def add_task(task: str):
    default = {"status":False}
    # Checking to see if we should add to an existing file or to add to a new file 
    # with the inserted task.
    if read_tasks():
        all_tasks = read_tasks()
        # Checking if the key exists already
        for key in all_tasks.keys():
            if key == task:
                resume = False
                break
            else: resume = True
        if resume:
            all_tasks[task] = default
            # Placing the new data in the json file,
            with open("todo.json", "w") as file:
                json.dump(all_tasks, file)
                print("[Main/Add task] ~ Task added!")
        else:
            print("[Main/Add task] ~ Task exists already.")
    else:
        # In the case of the file not existing the program will create a new json file
        # to place the task to.
        with open("todo.json", "w") as file:
            new = {}
            new[task] = default
            json.dump(new, file)
            print("[Main/Add task] ~ Task added!")


def add_subtask(task,subtask):
    # Running in a try statement in the case of the task not existing
    try:
        all_tasks = read_tasks()
        if subtask.lower() != "status":
            all_tasks[task][subtask] = False
            # Writing to the file the sub-task in the case of the file existing. 
            with open("todo.json", "w") as file:
                json.dump(all_tasks, file)
                print("Sub-task added successfully!")
        else:
            print("That task name is not allowed")
    except KeyError:
        print("The specified task doesnt exist")

def delete(data,task,sub = None):
    # Checking if we want to delete a sub-task or a task
    if sub == None: # In the case of a normal task
        try:
            del data[task] # Deleteing the task
            # Writing to the todo file
            with open("todo.json", "w") as file: 
                json.dump(data, file)
                print("[Main/Select/Delete] ~ Task deleted sucessfully!")
        except:
            print("[Main/Select/Delete] ~ Task doesnt exist")
    elif sub != "status": # In the case of a sub-task
        try:
            del data[task][sub] # Deleteing the sub-task
            # Writing to the todo file
            with open("todo.json", "w") as file:
                json.dump(data, file)
                print("[Main/Select/Delete] ~ Sub-task deleted sucessfully!")
        except:
            print("[Main/Select/Delete] ~ Sub-task doesnt exist")
    else:
        print("[Main/Select/Delete] ~ Invalid input")

def status(sub_exists,task):
    changed = True
    # In the case of a sub task existing
    if sub_exists:
        while changed:
            # Asking the user if they want to delete a task or a sub-task
            decision = input("[Main/Select/Change status] ~ Did you complete a task or a sub-task?\nTask = 1\nSub-task = 2\n")
            # In the case of the user wanting ot delete a task
            if decision == "1":
                if read_tasks()[task]["status"] == False:
                    tasks = read_tasks()
                    tasks[task]["status"] = True
                    # Writing to the JSON file
                    with open("todo.json", "w") as file:
                        json.dump(tasks, file)
                    print("[Main/Select/Change status] ~ Task completed!")
                    changed = False
                    break
                else:
                    # Changing status to false if true
                    tasks = read_tasks()
                    tasks[task]["status"] = False
                    # Writing to the JSON file
                    with open("todo.json", "w") as file:
                        json.dump(tasks, file)
                    print("[Main/Select/Change status] ~ Task status changed.")
                    changed = False
                    break

            if decision == "2":
                changed = True
                while changed:
                    # Ask for the sub-task to change
                    sub_task = input("[Main/Select/Change status] ~ What sub task would you like to change the status of?\n(type list to view available subtasks)\n")
                    if sub_task.lower() == "list":
                        print_subtasks(read_tasks(), task) # Listing the subtasks
                    elif sub_task.lower() != "status":
                        # Checking if the key exists
                        sub_task_found = False
                        for key in read_tasks()[task].keys():
                            # In the case of the specified sub-task existing
                            if key.lower() == sub_task.lower():
                                sub_task_found = True
                                tasks = read_tasks()
                                # In the case of the task being false set it to true
                                if tasks[task][sub_task] == False:
                                    tasks[task][sub_task] = True
                                    # Writing to the JSON file
                                    with open("todo.json", "w") as file:
                                        json.dump(tasks, file)
                                    print("[Main/Select/Change status] ~ Sub-task completed!")
                                    changed = False
                                    break
                                # In the case of the task being true set it to false
                                elif tasks[task][sub_task] == True:
                                    tasks[task][sub_task] = False
                                    # Writing to the JSON file
                                    with open("todo.json", "w") as file:
                                        json.dump(tasks, file)
                                    print("[Main/Select/Change status] ~ Sub-task status changed.")
                                    changed =False
                                    break
                        if not sub_task_found:
                            print("[Main/Select/Change status] ~ Sub-task cant be found")
                            changed = False
                            break

            elif sub_task.lower() == "exit":
                changed = False
                break
            else:
                print("Invalid input")


    #In the case of no subtasks
    else:
        # Changing status to true if false
        if read_tasks()[task]["status"] == False:
            tasks = read_tasks()
            tasks[task]["status"] = True
            # Writing to the JSON file
            with open("todo.json", "w") as file:
                json.dump(tasks, file)
                print("[Main/Select/Change status] ~ Task completed!")
        else:
            # Changing status to false if true
            tasks = read_tasks()
            tasks[task]["status"] = False
            # Writing to the JSON file
            with open("todo.json", "w") as file:
                json.dump(tasks, file)
                print("[Main/Select/Change status] ~ Task status changed.")

#---------------------------====================Main====================---------------------------



while True:
    prompt = input("[Main] ~ What would you like to do? ").strip()

    if prompt.lower() == "add":
        while True:
            response = input("[Main/Add task] ~ What task would you like to add? ")
            if len(response) != 0:
                add_task(response)
                break
            elif prompt.lower() == "exit":
                break
            else:
                print("[Main/Add task] ~ Please enter a task to add or type exit to exit this menu.")

    elif prompt.lower() == "select":
        while True:
            selected = input("[Main/Select] ~ What task would you like to select? ")
            if selected in read_tasks():
                response = input("[Main/Select] ~ What action would you like to take? ").strip()
                if response.lower() == "subtask":
                    add_subtask(selected, input("[Main/Select/Sub-task menu] ~ What should the sub-task be? "))
                    break

                elif response.lower() == "help":
                    break

                elif response.lower() == "list":
                    print_subtasks(read_tasks(),selected)
                    pass

                elif response.lower() == "rename":
                    while True:
                        new = input("[Main/Select/Rename] ~ What should the new task name be? ")
                        if len(new) != 0:
                            rename(selected,new)
                            break
                        else:
                            print("[Main/Select/Rename] ~ Invalid input")

                elif response.lower() == "exit":
                    break
                
                elif response.lower() == "delete":
                    for sub_task in read_tasks()[selected]:
                        if sub_task != "status":
                            sub_exists = True
                            break
                        else:
                            sub_exists = False
                    while True:
                        if sub_exists:
                            deletion_mode = input("[Main/Select/Delete] ~ Would you like to delete a task or a sub-task?\nTask = 1\nSub-task = 2\n")
                            if deletion_mode == "1":
                                delete(read_tasks(),selected)
                                break
                            elif deletion_mode == "2":
                                delete(read_tasks(),selected,input("[Main/Select/Delete] ~ What sub task would you like to delete? "))
                                break
                            else: 
                                print("[Main/Select/Delete] ~ Invalid input.")

                        else:
                            delete(read_tasks(),selected)
                            break
                        break

                elif response.lower() == "status":
                    for sub_task in read_tasks()[selected]:
                        if sub_task != "status":
                            sub_exists = True
                            break
                        else:
                            sub_exists = False
                    status(sub_exists,selected)
                    break

                else:
                    print("[Main/Select] ~ Please enter a valid instruction or type \"help\" for help")

            elif selected.lower() == "list":
                tasks = read_tasks()
                show(tasks)

            elif selected.lower() == "exit":
                print("[Main/Select] ~ Exiting select menu...")
                break
            else:
                print("[Main/Select] ~ The specified task is not listed.")


    elif prompt.lower() == "list":
        tasks = read_tasks()
        show(tasks)


    elif prompt.lower() == "exit":
        print("[Main] ~ Exiting...")
        break

    else:
        print("[Main] ~ Please enter a valid input or type \"help\" for instructions")
