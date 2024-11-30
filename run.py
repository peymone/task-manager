from configparser import ConfigParser

# My modules
from src.task_manager import TaskManager
from src.cli import CLI
from src.prettifier import pf


def load_config() -> str:
    """Load config from config.ini and return it's values

    Returns:
        str: save file path
    """

    config = ConfigParser()
    config.read("config.ini")
    save_file_path = config.get('PROD', 'SAVE_FILE_PATH')

    return save_file_path


if __name__ == '__main__':
    # Load config from config.ini
    save_file_path = load_config()

    # Create task manager and cli objects
    task_manager = TaskManager(save_file_path)
    cli = CLI(task_manager)

    # Show banner, commands and start handling user input
    pf.show_banner()
    cli.show_commands()
    cli.command_handler()
