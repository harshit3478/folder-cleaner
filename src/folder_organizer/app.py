"""Main Textual TUI application."""

from pathlib import Path
from textual.app import App
from textual.css.query import NoMatches

from folder_organizer.organizer import FolderOrganizer
from folder_organizer.screens.home import HomeScreen
from folder_organizer.config import Config


class FolderOrganizerApp(App):
    """A Textual app for organizing folders."""

    CSS_PATH = "app.tcss"
    TITLE = "Folder Organizer"
    SUB_TITLE = "Beautiful terminal-based folder management"

    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
        ("ctrl+q", "quit", "Quit"),
    ]

    def __init__(self, folder_path: str = "."):
        super().__init__()
        self.folder_path = Path(folder_path).resolve()
        self.config = Config()
        
        try:
            self.organizer = FolderOrganizer(str(self.folder_path))
        except ValueError as e:
            self.exit(message=f"Error: {e}")
            raise

    def on_mount(self) -> None:
        """Handle app mount."""
        self.push_screen(HomeScreen(str(self.folder_path), self.organizer))

    def action_quit(self) -> None:
        """Quit the application."""
        self.exit()


def run_app(folder_path: str = "."):
    """Run the Textual app."""
    app = FolderOrganizerApp(folder_path)
    app.run()


if __name__ == "__main__":
    run_app()
