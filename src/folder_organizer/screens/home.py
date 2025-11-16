"""Home screen for the folder organizer TUI."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button, Label
from textual.containers import Container, Vertical, Horizontal
from rich.text import Text


class HomeScreen(Screen):
    """Main home screen showing folder info and actions."""

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("o", "change_folder", "Open Folder"),
        ("1", "organize", "Organize"),
        ("2", "search", "Search"),
        ("3", "move", "Move"),
        ("4", "delete", "Delete"),
        ("s", "settings", "Settings"),
    ]

    def __init__(self, folder_path: str, organizer):
        super().__init__()
        self.folder_path = folder_path
        self.organizer = organizer

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        
        with Container(id="home-container"):
            yield Static(f"📁 [b cyan]{self.folder_path}[/b cyan]", id="folder-path")
            yield Static("[dim]Press 'o' to change folder, 'q' to quit[/dim]", id="folder-hint")
            
            # Stats panel
            yield Static("📊 Folder Stats", classes="section-title")
            with Container(id="stats-container"):
                yield Static("Loading...", id="stats-content")
            
            # Quick actions
            yield Static("🎯 Quick Actions", classes="section-title")
            with Vertical(id="actions-container"):
                yield Button("[1] 📦 Organize Files", id="btn-organize", variant="primary")
                yield Button("[2] 🔍 Search/Count Files", id="btn-search")
                yield Button("[3] 📤 Move Files by Extension", id="btn-move")
                yield Button("[4] 🗑️  Delete Files by Extension", id="btn-delete", variant="error")
                yield Button("[s] ⚙️  Settings", id="btn-settings")
        
        yield Footer()

    def on_mount(self) -> None:
        """Handle screen mount."""
        self.load_stats()

    def load_stats(self) -> None:
        """Load and display folder statistics."""
        try:
            meta = self.organizer.get_meta()
            
            stats_text = f"""
[cyan]💾 Size:[/cyan] {meta['size']}
[cyan]📄 Files:[/cyan] {meta['file_count']:,}
[cyan]📂 Subfolders:[/cyan] {meta['folder_count']:,}
[cyan]🕐 Created:[/cyan] {meta['creation_time']}
            """.strip()
            
            stats_widget = self.query_one("#stats-content", Static)
            stats_widget.update(stats_text)
        except Exception as e:
            stats_widget = self.query_one("#stats-content", Static)
            stats_widget.update(f"[red]Error loading stats: {e}[/red]")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id
        
        if button_id == "btn-organize":
            self.action_organize()
        elif button_id == "btn-search":
            self.action_search()
        elif button_id == "btn-move":
            self.action_move()
        elif button_id == "btn-delete":
            self.action_delete()
        elif button_id == "btn-settings":
            self.action_settings()

    def action_change_folder(self) -> None:
        """Change the target folder."""
        from folder_organizer.screens.folder_select import FolderSelectScreen
        
        def handle_folder_change(new_path) -> None:
            """Handle the new folder selection."""
            if new_path:
                # Import here to avoid circular dependency
                from folder_organizer.organizer import FolderOrganizer
                
                try:
                    # Create new organizer for the new path
                    self.organizer = FolderOrganizer(str(new_path))
                    self.folder_path = str(new_path)
                    
                    # Update the folder path display
                    folder_widget = self.query_one("#folder-path", Static)
                    folder_widget.update(f"📁 [b cyan]{self.folder_path}[/b cyan]")
                    
                    # Reload stats
                    self.load_stats()
                    
                    self.app.notify(
                        f"✅ Switched to: {new_path}",
                        severity="information",
                        timeout=3
                    )
                except Exception as e:
                    self.app.notify(
                        f"Error loading folder: {e}",
                        severity="error",
                        timeout=5
                    )
        
        # Push the folder select screen and handle result
        self.app.push_screen(
            FolderSelectScreen(self.folder_path),
            handle_folder_change
        )

    def action_organize(self) -> None:
        """Show organize screen."""
        from folder_organizer.screens.organize import OrganizeScreen
        self.app.push_screen(OrganizeScreen(self.organizer))

    def action_search(self) -> None:
        """Show search screen."""
        from folder_organizer.screens.search import SearchScreen
        self.app.push_screen(SearchScreen(self.organizer))

    def action_move(self) -> None:
        """Show move files screen."""
        from folder_organizer.screens.move import MoveScreen
        self.app.push_screen(MoveScreen(self.organizer))

    def action_delete(self) -> None:
        """Show delete files screen."""
        from folder_organizer.screens.delete import DeleteScreen
        self.app.push_screen(DeleteScreen(self.organizer))

    def action_settings(self) -> None:
        """Show settings screen."""
        self.app.notify("Settings screen coming soon!", severity="information")

    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()
