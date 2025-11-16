"""Search files screen."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button, Input, DataTable
from textual.containers import Container, Vertical, ScrollableContainer


class SearchScreen(Screen):
    """Screen for searching and counting files."""

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("q", "app.pop_screen", "Back"),
    ]

    def __init__(self, organizer):
        super().__init__()
        self.organizer = organizer

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        
        with Container(id="search-container"):
            yield Static("🔍 Search Files", classes="screen-title")
            yield Static(
                "[dim]Enter a search term or file extension to find matching files[/dim]",
                classes="description"
            )
            
            yield Input(
                placeholder="e.g., .pdf or report",
                id="search-input"
            )
            
            with ScrollableContainer(id="results-container"):
                yield Static("", id="results-content")
            
            yield Button("← Back", id="btn-back", variant="default")
        
        yield Footer()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle search when Enter is pressed."""
        self.do_search(event.value)

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle real-time search."""
        if len(event.value) >= 2:  # Only search if at least 2 characters
            self.do_search(event.value)
        else:
            results_widget = self.query_one("#results-content", Static)
            results_widget.update("")

    def do_search(self, term: str) -> None:
        """Perform the search."""
        if not term:
            return
        
        try:
            count = self.organizer.get_filecount(term)
            files = self.organizer.search_files(term)
            
            if count == 0:
                results_widget = self.query_one("#results-content", Static)
                results_widget.update(
                    f"\n[yellow]No files found matching '[b]{term}[/b]'[/yellow]"
                )
                return
            
            # Build results display
            lines = [f"\n[green]Found {count} file(s) matching '[b]{term}[/b]'[/green]\n"]
            
            for file in files[:50]:  # Show first 50
                lines.append(
                    f"[cyan]•[/cyan] {file['name']}  "
                    f"[dim]({file['size_formatted']})[/dim]"
                )
            
            if len(files) > 50:
                lines.append(f"\n[dim]... and {len(files) - 50} more files[/dim]")
            
            results_text = "\n".join(lines)
            results_widget = self.query_one("#results-content", Static)
            results_widget.update(results_text)
            
        except Exception as e:
            results_widget = self.query_one("#results-content", Static)
            results_widget.update(f"[red]Error searching: {e}[/red]")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-back":
            self.app.pop_screen()
