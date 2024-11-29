from configparser import ConfigParser

from src.task_manager import TaskManager


def load_config() -> str:
    """Load config from config.ini and return it's values

    Returns:
        str: save file path
    """

    config = ConfigParser()
    config.read("config.ini")
    save_file_path = config.get('DEFAULT', 'SAVE_FILE_PATH')

    return save_file_path


if __name__ == '__main__':
    save_file_path = load_config()
    task_manager = TaskManager(save_file_path)
