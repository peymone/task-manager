import re
from dataclasses import asdict

from src.task_manager import TaskManager, Task
from src.prettifier import pf


class CLI:
    def __init__(self, task_manager: TaskManager) -> None:
        self.commands = {
            "help": "show all commands",
            "add": "add new task",
            "remove": "remove tasks",
            "change": "change existing task",
            "status": "switch status for existing task",
            "find": "filter tasks by id, title, category, priority or status",
            "show": "show all tasks"
        }

        self.task_manager = task_manager
        self.deadline_pattern = '\d{4}-\d{2}-\d{2}'

    def show_commands(self) -> None:
        """Print all available commands"""

        pf.print("\nAvailable commands: ", end='\n\n', style="info")

        for command, description in self.commands.items():
            pf.print(command + ":", end=" ", style="command")
            pf.print(description)

        pf.print("\nEnter CTRL + C to enter\n", style="info")

    def command_handler(self) -> None:
        try:  # Handle keyboard interruption
            while True:
                command = pf.input("Enter command: ")

                # Command handler
                match command:
                    case "help": self.show_commands()

                    case "add":
                        pf.print("\nEnter data for new task\n", style="info")

                        # Fill data for new task
                        title = pf.ask("Title")
                        description = pf.ask("Description")
                        category = pf.ask("Category")

                        deadline = pf.ask("Deadline", description="(like 2024-12-31)")
                        while not re.fullmatch(self.deadline_pattern, deadline):
                            deadline = pf.ask("Deadline", description="(like 2024-12-31)", style="error")

                        priority = pf.ask("Priority", description="(low/medium/high)")
                        while priority not in ("low", "medium", "high"):
                            priority = pf.ask("Priority", description="(low/medium/high)", style="error")

                        # Create task
                        result = self.task_manager.add(title, description, category, deadline, priority)

                        # Check result
                        if isinstance(result, str):
                            pf.print("\t" + result, style="error")

                        print('\n')

                    case "remove":
                        print("\n")
                        id = pf.ask("Task ID", description="(omit if you want to remove task by category)")

                        # Remove by id
                        if id:
                            while not id.isdigit():
                                id = pf.ask(
                                    "Task ID", description="(omit if you want to remove task by category)", style="error")

                            # Remove task
                            result = self.task_manager.remove(id=int(id))

                            # Check if operation failed
                            if isinstance(result, str):
                                pf.print("\t" + result, style="error")

                        # Remove by category
                        else:
                            category = pf.ask("Category")
                            while not category:
                                category = pf.ask("Category", description="(field cannot be empty)", style="error")

                            # Remove task
                            result = self.task_manager.remove(category=category)

                            # Check result
                            if isinstance(result, str):
                                pf.print("\t" + result, style="error")

                        print('\n')

                    case "change":

                        print("\n")
                        id = pf.ask("Task ID")

                        # Check if id is entered and is digit
                        while (not id) or (not id.isdigit()):
                            id = pf.ask("Task ID", description="(task id must be digit)", style="error")

                        pf.print("\n\tYou can omit every field if you do not want to change it\n", style="info")

                        # Enter new data for task
                        def check_len(value):
                            return None if len(value) == 0 else value

                        title = pf.ask("\tTitle")
                        title = check_len(title)

                        description = pf.ask("\tDescription")
                        description = check_len(description)

                        category = pf.ask("\tCategory")
                        category = check_len(category)

                        deadline = pf.ask("\tDeadline", description="(like 2024-12-31)")
                        if deadline:
                            while not re.fullmatch(self.deadline_pattern, deadline):
                                deadline = pf.ask("\tDeadline", description="(like 2024-12-31)", style="error")
                        deadline = check_len(deadline)

                        priority = pf.ask("\tPriority", description="(low/medium/high)")
                        if priority:
                            while priority not in ("low", "medium", "high"):
                                priority = pf.ask("\tPriority", description="(low/medium/high)", style="error")
                        priority = check_len(priority)

                        # Change task
                        result = self.task_manager.change(int(id), title, description, category, deadline, priority)

                        # Check result
                        if isinstance(result, str):
                            pf.print("\t\t" + result, style="error")

                        print('\n')

                    case "status":
                        print("\n")
                        id = pf.ask("Task ID")

                        # Check if id is entered and is digit
                        while (not id) or (not id.isdigit()):
                            id = pf.ask("Task ID", description="(task id must be digit)", style="error")

                        # Change status
                        result = self.task_manager.status(int(id))

                        # Check result
                        if isinstance(result, str):
                            pf.print("\t" + result, style="error")

                        print('\n')

                    case "find":
                        print("\n")
                        filter = pf.ask("Choose field by which you want to search tasks",
                                        description="(id/title/category/priority/status)")

                        while filter not in ("id", "title", "category", "priority", "status"):
                            filter = pf.ask("Choose field by which you want to search tasks",
                                            description="(id/title/category/priority/status)", style="error")

                        # Filter tasks
                        match filter:
                            case "id":
                                id = pf.ask("Task ID")

                                while (not id) or (not id.isdigit()):
                                    id = pf.ask("Task ID", description="(task id must be digit)", style="error")

                                result = self.task_manager.find(id=int(id))

                            case "title":
                                title = pf.ask("Title")
                                result = self.task_manager.find(title=title)
                            case "category":
                                category = pf.ask("Category")
                                result = self.task_manager.find(category=category)
                            case "priority":
                                priority = pf.ask("Priority")
                                result = self.task_manager.find(priority=priority)
                            case "status":
                                status = pf.ask("Status")
                                result = self.task_manager.find(status=status)

                        # Check result
                        if isinstance(result, str):
                            pf.print("\t" + result, style="error")
                            print("\n")
                        else:
                            print("\n")
                            for task in result:
                                for name, value in asdict(task).items():
                                    pf.print(f"\t\t{name}: ", style="command", end="")
                                    pf.print(value)

                                print("\n")

                    case "show":
                        task_list: list[Task] = self.task_manager.show()
                        if isinstance(task_list, str):
                            pf.print("\n\t\t" + task_list)
                            print("\n")
                        else:
                            print("\n")
                            for task in task_list:
                                for name, value in asdict(task).items():
                                    pf.print(f"\t\t{name}: ", style="command", end="")
                                    pf.print(value)

                                print("\n")

        except KeyboardInterrupt:
            print('\n')
