from configparser import ConfigParser
from dataclasses import asdict
from os import remove
import pytest

from src.task_manager import TaskManager, Task


config = ConfigParser()
config.read("config.ini")
save_file_path = config.get('TEST', 'SAVE_FILE_PATH')


@pytest.fixture(scope='function')
def task_manager():
    task_manager = TaskManager(save_file_path)
    yield task_manager
    remove(save_file_path)


@pytest.fixture(scope='function')
def add_data():
    add_data = [
        ("title1", "description1", "category1", "deadline1", "priority1"),
        ("title2", "description2", "category2", "deadline2", "priority2"),
        ("title3", "description3", "category3", "deadline3", "priority3"),
        ("title4", "description4", "category4", "deadline4", "priority4"),
        ("title5", "description5", "category5", "deadline5", "priority5"),
        ("title6", "description6", "category1", "deadline6", "priority6"),
    ]

    return add_data


@pytest.fixture(scope='function')
def change_data():
    changing_data = [
        (1, "TITLE1", "DESCRIPTION1", "CATEGORY1", "DEADLINE1", "PRIORITY1"),
        (2, "TITLE2", None, None, None, None),
        (3, None, "DESCRIPTION3", None, None, None),
        (4, None, None, "CATEGORY4", None, None),
        (5, None, None, None, "DEADLINE5", None),
        (6, "TITLE6", None, "CATEGORY1", None, "PRIORITY6"),
    ]

    changed_data = [
        ("TITLE1", "DESCRIPTION1", "CATEGORY1", "DEADLINE1", "PRIORITY1"),
        ("TITLE2", "description2", "category2", "deadline2", "priority2"),
        ("title3", "DESCRIPTION3", "category3", "deadline3", "priority3"),
        ("title4", "description4", "CATEGORY4", "deadline4", "priority4"),
        ("title5", "description5", "category5", "DEADLINE5", "priority5"),
        ("TITLE6", "description6", "CATEGORY1", "deadline6", "PRIORITY6"),
    ]

    return changing_data, changed_data


def test_add(task_manager, add_data):
    # Add data to save file
    for data in add_data:
        result: Task = task_manager.add(*data)
        assert tuple(asdict(result).values())[1:-1] == data


def test_remove_by_id(task_manager, add_data):
    # Add data to save file
    for data in add_data:
        result: Task = task_manager.add(*data)

    # No task with id 6 - must return failure desription
    assert isinstance(task_manager.remove(id=100), str) == True

    # Remove task with id 2 - must return removed task
    removed_task: list[Task] = task_manager.remove(id=2)
    assert tuple(asdict(removed_task[0]).values())[1:-1] == add_data[1]


def test_remove_by_category(task_manager, add_data):
    # Add data to save file
    for data in add_data:
        result: Task = task_manager.add(*data)

    # Remove tasks by non-existent category
    assert isinstance(task_manager.remove(category="category_dont_exist"), str) == True

    # Remove tasks by existent category
    removed_tasks: list[Task] = task_manager.remove(category=add_data[0][2])
    assert len(removed_tasks) == 2

    assert [tuple(asdict(task).values())[1:-1]
            for task in removed_tasks] == [data for data in add_data if data[2] == add_data[0][2]]


def test_change(task_manager, add_data, change_data):
    # Add data to save file
    for data in add_data:
        result: Task = task_manager.add(*data)

    # Change non-existent task
    assert isinstance(task_manager.change(id=100, title="title100"), str) == True

    # Change all values
    for changing_data, changed_data in zip(change_data[0], change_data[1]):
        changed_task = task_manager.change(*changing_data)
        assert tuple(asdict(changed_task).values())[1:-1] == changed_data


def test_status(task_manager, add_data):
    # Add data to save file
    for data in add_data:
        result: Task = task_manager.add(*data)

    # Change status for non-existent task
    assert isinstance(task_manager.change(id=100), str) == True

    # Change status for first task
    assert tuple(asdict(task_manager.status(id=1)).values())[1:] == add_data[0] + ('Done',)
    assert tuple(asdict(task_manager.status(id=1)).values())[1:] == add_data[0] + ("In progress",)


def test_show(task_manager, add_data):
    # No task saved
    assert isinstance(task_manager.show(), str) == True

    # Add data to save file
    for data in add_data:
        result: Task = task_manager.add(*data)

    # Compared showed data with local
    task_list = task_manager.show()
    assert [tuple(asdict(task).values())[1:-1] for task in task_list] == add_data
