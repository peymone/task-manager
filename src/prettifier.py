from rich.console import Console
from rich.prompt import Prompt
from rich.theme import Theme
import pyfiglet


class Prettifier:
    def __init__(self):
        self.styles = {
            "handler": "i spring_green3",
            "command": "cyan",
            "data": "bright_yellow",
            "desc": "grey35",
            "error": "bold red",
            "info": "i grey35",
        }

        self.banner_text = "Task Manager"
        self.cign_text = "Made by(c) Vladimir Reymer"

        self.theme = Theme(styles=self.styles)
        self.console = Console(theme=self.theme)
        self.prompt = Prompt()

    def show_banner(self):
        """Show banner, sign and rule"""

        ascii_banner = pyfiglet.figlet_format(self.banner_text, font="banner3-d")
        self.console.print(ascii_banner, justify="center")
        self.console.rule("[spring_green3]" + self.cign_text, style="bright_yellow")

    def print(self, text: str, style: str = None, end: str = "\n") -> None:
        self.console.print(text, end=end, style=style)

    def input(self, prompt: str, style: str = "handler") -> str:
        command = self.console.input(f"[{self.styles[style]}]" + prompt)
        return command

    def ask(self, text: str,  style: str = "data", description: str = "") -> str:
        data = self.prompt.ask(f"\t[{self.styles[style]}]{text}[/]" + f"[{self.styles['desc']}] {description}[/]")
        return data


pf = Prettifier()
