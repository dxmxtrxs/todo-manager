#--------------------------===================IMPORTS===================--------------------------

import json 
import os

#-------------------------===================FUNCTIONS===================-------------------------


def rename(old,new):
    # Getting the tasks from the JSON file
    tasks = read_tasks(False)
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
        print("Task renamed successfully!")
    else:
        # Printing an error in the case of both names being the same
        print("Name can't be the same.")


def show(dictionary):
    try:
        reveal = show_mode(dictionary)
        if reveal:
            print_table(dictionary)
        else:
            print_table_no_sub(dictionary)
    except:
        print("No tasks!")

# Used to print tasks when we know there are sub tasks
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
            task_status = result.center(max_status_width)

            subtasks_list = [
                f"{subtask}: {'Uncompleted' if not value[subtask] else 'Completed'}"
                for subtask in value if subtask != "status"
            ]
            subtasks_str = ", ".join(subtasks_list)

            if not subtasks_list:
                subtasks_str = "None".center(max_subtasks_width)

            print(f"| {task} | {task_status} | {subtasks_str:<{max_subtasks_width}} |")
        
        # Print the table footer
        print(line)
    except:
        print("No tasks")


# Used to print tasks when we know there are sub tasks
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
            task_status = str(value["status"]).center(max_status_width)

            print(f"| {task} | {task_status} |")
        
        # Print the table footer
        print(line)
    except:
        print("No tasks")


# Used to find if there are any sub tasks  
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
            print(f"\nAll subtasks in {selected}:")
            print(", ".join(subtasks_list))
        else:
            # If there are no subtasks, print a message indicating that
            print(f"Task '{key}' has no subtasks.")
    else:
        # If the key (task) is not found in the data_dict, print an error message
        print(f"Task '{key}' not found in the data.")


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
        with open("todo.json", "w") as file:
            new = {}
            new[task] = default
            json.dump(new, file)
            print("Task added!")


def add_subtask(task,subtask):
    # Running in a try statement in the case of the task not existing
    try:
        all_tasks = read_tasks(False)
        if subtask.lower() != "status":
            all_tasks[task][subtask] = False
            # Writing to the file the sub-task in the case of the file existing. 
            with open("todo.json", "w") as file:
                json.dump(all_tasks, file)
                print("Sub task added successfully!")
        else:
            print("That task name is not allowed")
    except KeyError:
        print("The specified task doesnt exist")


#---------------------------====================Main====================---------------------------



while True:
    prompt = input("What would you like to do? ")

    if prompt.lower() == "add":
        while True:
            response = input("What task would you like to add? ")
            if len(response) != 0:
                add_task(response)
                break
            elif prompt.lower() == "exit":
                break
            else:
                print("Please enter a task to add or type exit to exit this menu.")

    elif prompt.lower() == "select":
        while True:
            selected = input("What item would you like to select? ")
            if selected in read_tasks(False):
                response = input("What action would you like to take? ")
                if response.lower() == "subtask":
                    add_subtask(selected, input("What should the sub task be? "))
                    break

                elif response.lower() == "help":
                    break

                elif response.lower() == "list":
                    
                    print_subtasks(read_tasks(False),selected)
                    pass

                elif response.lower() == "rename":
                    while True:
                        new = input("What should the new task name be? ")
                        if len(new) != 0:
                            rename(selected,new)
                            break
                        else:
                            print("Invalid input")
                elif response.lower() == "exit":
                    break
                else:
                    print("Please enter a valid input or type \"help\" for instructions")

            elif selected.lower() == "list":
                tasks = read_tasks(False)
                show(tasks)

            elif selected.lower() == "exit":
                print("Exiting select menu...")
                break
            else:
                print("The specified task is not listed.")


    elif prompt.lower() == "list":
        tasks = read_tasks(False)
        show(tasks)


    elif prompt.lower() == "exit":
        print("Exiting...")
        break

    else:
        print("Please enter a valid input or type \"help\" for instructions")
        
