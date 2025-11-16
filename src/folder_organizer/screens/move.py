"""Move files screen."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button, Input, Label, DirectoryTree
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer
from pathlib import Path


class MoveScreen(Screen):
    """Screen for moving files by extension to another folder."""

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("q", "app.pop_screen", "Back"),
    ]

    def __init__(self, organizer):
        super().__init__()
        self.organizer = organizer
        self.destination = None
        self.extension = None

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        
        with Container(id="move-container"):
            yield Static("📤 Move Files by Extension", classes="screen-title")
            yield Static(
                "[dim]Move all files with a specific extension to another folder[/dim]",
                classes="description"
            )
            
            yield Label("Extension (with dot, e.g., .pdf):")
            yield Input(placeholder=".pdf", id="extension-input")
            
            yield Label("Destination folder:")
            yield Static("[dim]Type the full path or use tab completion[/dim]", classes="hint")
            yield Input(placeholder="/path/to/destination", id="destination-input")
            
            yield Static("", id="preview-text")
            
            with Horizontal(id="button-row"):
                yield Button("← Back", id="btn-back", variant="default")
                yield Button("Preview", id="btn-preview", variant="primary")
                yield Button("✓ Move Files", id="btn-confirm", variant="success", disabled=True)
        
        yield Footer()

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes."""
        if event.input.id == "extension-input":
            self.extension = event.value
        elif event.input.id == "destination-input":
            self.destination = event.value
        
        # Enable preview if both fields have values
        preview_btn = self.query_one("#btn-preview", Button)
        if self.extension and self.destination:
            preview_btn.disabled = False
        else:
            preview_btn.disabled = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-back":
            self.app.pop_screen()
        elif event.button.id == "btn-preview":
            self.do_preview()
        elif event.button.id == "btn-confirm":
            self.do_move()

    def do_preview(self) -> None:
        """Preview the move operation."""
        if not self.extension or not self.destination:
            return
        
        # Validate destination
        dest_path = Path(self.destination).expanduser().resolve()
        if not dest_path.exists():
            preview_widget = self.query_one("#preview-text", Static)
            preview_widget.update(
                f"\n[red]✗ Destination does not exist: {self.destination}[/red]\n"
            )
            return
        
        if dest_path == self.organizer.path:
            preview_widget = self.query_one("#preview-text", Static)
            preview_widget.update(
                "\n[red]✗ Cannot move files to the same folder[/red]\n"
            )
            return
        
        try:
            result = self.organizer.move_files(
                self.extension,
                str(dest_path),
                dry_run=True
            )
            
            if result.files_affected == 0:
                preview_widget = self.query_one("#preview-text", Static)
                preview_widget.update(
                    f"\n[yellow]No files found with extension '{self.extension}'[/yellow]\n"
                )
                confirm_btn = self.query_one("#btn-confirm", Button)
                confirm_btn.disabled = True
                return
            
            # Show preview
            lines = [
                f"\n[cyan]Found {result.files_affected} file(s) to move:[/cyan]\n"
            ]
            
            for file in result.files_list[:20]:
                lines.append(f"  • {file}")
            
            if len(result.files_list) > 20:
                lines.append(f"\n  [dim]... and {len(result.files_list) - 20} more files[/dim]")
            
            lines.append(f"\n[green]→ Destination: {dest_path}[/green]\n")
            
            preview_text = "\n".join(lines)
            preview_widget = self.query_one("#preview-text", Static)
            preview_widget.update(preview_text)
            
            # Enable confirm button
            confirm_btn = self.query_one("#btn-confirm", Button)
            confirm_btn.disabled = False
            
        except Exception as e:
            preview_widget = self.query_one("#preview-text", Static)
            preview_widget.update(f"\n[red]Error: {e}[/red]\n")

    def do_move(self) -> None:
        """Execute the move operation."""
        if not self.extension or not self.destination:
            return
        
        dest_path = Path(self.destination).expanduser().resolve()
        
        self.app.notify("Moving files...", severity="information")
        
        try:
            result = self.organizer.move_files(
                self.extension,
                str(dest_path),
                dry_run=False
            )
            
            if result.success:
                self.app.notify(
                    f"✅ {result.message}",
                    severity="information",
                    timeout=5
                )
                self.app.pop_screen()
            else:
                error_msg = "Move completed with errors:\n" + "\n".join(result.errors[:3])
                self.app.notify(error_msg, severity="warning", timeout=10)
                
        except Exception as e:
            self.app.notify(f"Error: {e}", severity="error", timeout=5)
