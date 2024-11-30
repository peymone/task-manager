from dataclasses import dataclass, asdict
from os.path import exists, getsize
from json import dump, load


@dataclass
class Task:
    id: int
    title: str
    description: str
    category: str
    deadline: str
    priority: str
    status: str = "In progress"

    def __str__(self):
        show_str = f"ID: {self.id}:\ntitle: {self.title}\ndescription: {self.description}\ncategory: {self.category}\ndeadline: {self.deadline}\npriority: {self.priority}\nstatus: {self.status}"
        return show_str


class TaskManager:
    """Manager for task cli, providing following operations:

    1 add task to save file
    2 remove tasks from save file
    3 change data for existing task
    4 swith status for existing task
    5 find tasks by id, title, category, priority or status
    6 show all saved tasks
    """

    def __init__(self, save_file_path: str) -> None:
        """Create save file if not exist

        Args:
            save_file_path (str): path to save file
        """

        self.save_file = save_file_path

        if not exists(save_file_path):
            save_file = open(save_file_path, "x")
            save_file.close()

    def __get_tasks_and_last_id(self) -> tuple[list[dict], int]:
        """Get task list and last task id from save file

        Returns:
            tuple[list[dict], int]: Task objects and last task id
        """

        # After removing all tasks, only brackets remained - clear them
        if getsize(self.save_file) == 2:
            file = open(self.save_file, "w")
            file.close()

        # Save file is empty
        if getsize(self.save_file) == 0:
            return list(), 0

        # Save file is not empty
        with open(self.save_file, "r", encoding="utf-8") as file:
            task_list: list[dict] = load(file)
            last_id: int = task_list[-1].get('id')

            return task_list, last_id

    def __save_tasks(self, task_list: list[dict]) -> None:
        """Save task list to save file

        Args:
            task_list (list[dict]): Task objects
        """

        # Rewrite file on save with new data
        with open(self.save_file, "w", encoding="utf-8") as file:
            dump(task_list, file, indent=4, ensure_ascii=False)

    def __reorder_id(self, task_list: list[dict]) -> list[dict]:
        """Reorder id from beggining of task list

        Args:
            task_list (list[dict]): Task objects

        Returns:
            list[dict]: Task objects with reordered ids
        """

        for id, task in enumerate(task_list, start=1):
            task['id'] = id

        return task_list

    def add(self, title: str, description: str, category: str, deadline: str, priority: str) -> Task | str:
        """Create new Task and save it to json file

        Args:
            title (str): Task's title
            description (str): Task's description
            category (str): Task's category
            deadline (str): Task's deadline
            priority (str): Task's priority

        Returns:
            Task | str: Task object OR description if operation failed
        """

        # Get tasks from save file and last task id
        task_list, last_id = self.__get_tasks_and_last_id()

        try:
            # Create new task and save it
            task = Task(last_id + 1, title, description, category, deadline, priority)
            task_list.append(asdict(task))
            self.__save_tasks(task_list)

            return Task

        except:
            return "Operation failed during adding new task to save file"

    def remove(self, id: int = None, category: str = None) -> list[Task] | str:
        """Remove one task by id OR all tasks with specific category

        Args:
            id (int, optional): Task's id. Defaults to None.
            category (str, optional): Task's category. Defaults to None.

        Returns:
            list[Task] | str: deleted Task objects OR failure description
        """

        # Get tasks from save file and last task id
        task_list, _ = self.__get_tasks_and_last_id()
        removed_tasks = list()

        # Remove task by id
        if id:
            # Check if id not in task list
            if id not in range(1, len(task_list) + 1):
                return f"No task with ID '{id}'"

            # Pop task and create Task object for return
            popped = task_list.pop(id-1)
            removed_tasks.append(Task(*popped.values()))

            # Reorder tasks id and save changes
            task_list = self.__reorder_id(task_list)
            self.__save_tasks(task_list)

        # Remove tasks by category
        if category:
            # Check if category not in task list
            if category not in [task['category'] for task in task_list]:
                return f"No task with category '{category}'"

            # Find tasks with provided category
            for id, task in enumerate(task_list[:]):
                if task['category'] == category:

                    # Pop task and create Task object for return
                    popped = task_list.pop(id)
                    removed_tasks.append(Task(*popped.values()))

            # Reorder tasks id and save changes
            task_list = self.__reorder_id(task_list)
            self.__save_tasks(task_list)

        return removed_tasks

    def change(self, id: int, title: str = None, description: str = None, category: str = None, deadline: str = None, priority: str = None) -> Task | str:
        """Change task by id with new data. All data is optional.

        Args:
            id (int): Task's id.
            title (str, optional): Task's title. Defaults to None.
            description (str, optional): Task's description. Defaults to None.
            category (str, optional): Task's category. Defaults to None.
            deadline (str, optional): Task's deadline. Defaults to None.
            priority (str, optional): Task's priority. Defaults to None.

        Returns:
            Task | str: Task object OR failure description
        """

        # Get tasks from save file and last task id
        task_list, _ = self.__get_tasks_and_last_id()

        # Check if id not in task list
        if id not in range(1, len(task_list) + 1):
            return f"No task with ID '{id}'"

        # Replcae old task data with new one
        for key in task_list[id-1].copy():
            if locals().get(key) is not None:
                task_list[id-1][key] = locals().get(key)

        # Save changes
        self.__save_tasks(task_list)

        return Task(*task_list[id-1].values())

    def status(self, id: int) -> Task | None:
        """Switch status for task with specific id

        Args:
            id (int): Task's id

        Returns:
            Task | str: Task object OR failure description
        """

        # Get tasks from save file and last task id
        task_list, _ = self.__get_tasks_and_last_id()

        # Check if id not in task list
        if id not in range(1, len(task_list) + 1):
            return f"No task with ID '{id}'"

        # Get current status and replace it
        status = task_list[id-1]['status']
        task_list[id-1]['status'] = "Done" if status == "In progress" else "In progress"

        # Save changes
        self.__save_tasks(task_list)

        return Task(*task_list[id-1].values())

    def find(self, id: int = None, title: str = None, category: str = None, priority: str = None, status: str = None) -> list[Task] | str:
        """Filter tasks by id, title, category, priority or status 

        Args:
            id (int, optional): Task's id. Defaults to None.
            title (str, optional): Task's title. Defaults to None.
            category (str, optional): Task's category. Defaults to None.
            priority (str, optional): Task's priority. Defaults to None.
            status (str, optional): Task's status. Defaults to None.

        Returns:
            list[Task] | str: Task objects list OR 'no task found'
        """

        # Get tasks from save file and last task id
        task_list, _ = self.__get_tasks_and_last_id()
        filtered_tasks = list()

        # Filter tasks
        if id:
            filtered_tasks.append(Task(*task_list[id-1].values()))
        if title:
            for task in task_list:
                if title in task['title']:
                    filtered_tasks.append(Task(*task.values()))
        if category:
            for task in task_list:
                if category == task['category']:
                    filtered_tasks.append(Task(*task.values()))
        if priority:
            for task in task_list:
                if priority == task['priority']:
                    filtered_tasks.append(Task(*task.values()))
        if status:
            for task in task_list:
                if status == task['status']:
                    filtered_tasks.append(Task(*task.values()))

        # Check if filtered tasks is empty and return result
        if len(filtered_tasks) == 0:
            return "no task found"
        else:
            return filtered_tasks

    def show(self) -> list[Task] | str:
        """Get Task objects list

        Returns:
            list[Task] | str: Task objects OR result string
        """

        # Get tasks from save file and last task id
        task_list, _ = self.__get_tasks_and_last_id()

        if len(task_list) == 0:
            return "You have no task at the moment - create one! (add)"
        else:
            return [Task(*task.values()) for task in task_list]
