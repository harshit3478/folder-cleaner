"""Folder selection screen."""

import os
from pathlib import Path
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button, Input, DirectoryTree
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer


class FolderSelectScreen(Screen):
    """Screen for selecting a different folder to organize."""

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("q", "app.pop_screen", "Back"),
    ]

    def __init__(self, current_path: str):
        super().__init__()
        self.current_path = Path(current_path)
        self.selected_path = None

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        
        with Container(id="folder-select-container"):
            yield Static("📁 Select Folder", classes="screen-title")
            yield Static(
                f"[dim]Current: {self.current_path}[/dim]",
                classes="description"
            )
            
            # Path input
            with Vertical(id="path-input-container"):
                yield Static("Enter folder path:", id="path-label")
                yield Input(
                    placeholder="e.g., ~/Downloads or /Users/username/Documents",
                    value=str(self.current_path),
                    id="path-input"
                )
            
            # Directory tree for browsing
            with ScrollableContainer(id="tree-container"):
                yield Static("📂 Browse:", id="tree-label")
                yield DirectoryTree(str(Path.home()), id="dir-tree")
            
            # Buttons
            with Horizontal(id="button-row"):
                yield Button("← Back", id="btn-back", variant="default")
                yield Button("✓ Select Folder", id="btn-select", variant="primary")
        
        yield Footer()

    def on_mount(self) -> None:
        """Handle screen mount."""
        # Focus on the input
        self.query_one("#path-input", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-back":
            self.app.pop_screen()
        elif event.button.id == "btn-select":
            self.select_folder()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key in input."""
        if event.input.id == "path-input":
            self.select_folder()

    def on_directory_tree_directory_selected(self, event: DirectoryTree.DirectorySelected) -> None:
        """Handle directory selection from tree."""
        # Update the input with selected path
        path_input = self.query_one("#path-input", Input)
        path_input.value = str(event.path)

    def select_folder(self) -> None:
        """Validate and select the folder."""
        path_input = self.query_one("#path-input", Input)
        entered_path = path_input.value.strip()
        
        if not entered_path:
            self.app.notify("Please enter a folder path", severity="warning")
            return
        
        # Expand user home directory
        entered_path = os.path.expanduser(entered_path)
        folder_path = Path(entered_path).resolve()
        
        # Validate path
        if not folder_path.exists():
            self.app.notify(
                f"Path does not exist: {folder_path}",
                severity="error",
                timeout=5
            )
            return
        
        if not folder_path.is_dir():
            self.app.notify(
                f"Path is not a directory: {folder_path}",
                severity="error",
                timeout=5
            )
            return
        
        # Check if same as current
        if folder_path == self.current_path:
            self.app.notify(
                "This is already the current folder",
                severity="information"
            )
            self.app.pop_screen()
            return
        
        # Set the selected path and notify parent
        self.selected_path = str(folder_path)
        self.app.notify(
            f"Switching to: {self.selected_path}",
            severity="information"
        )
        
        # Pop this screen and trigger folder change
        self.dismiss(self.selected_path)
