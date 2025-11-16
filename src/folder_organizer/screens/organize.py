"""Organize files screen."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button, Label, DataTable
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer
from rich.table import Table as RichTable


class OrganizeScreen(Screen):
    """Screen for organizing files into categories."""

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("q", "app.pop_screen", "Back"),
    ]

    def __init__(self, organizer):
        super().__init__()
        self.organizer = organizer
        self.preview_data = None

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        
        with Container(id="organize-container"):
            yield Static("📦 Organize Files", classes="screen-title")
            yield Static(
                "[dim]Files will be sorted into category folders based on their type[/dim]",
                classes="description"
            )
            
            with ScrollableContainer(id="preview-container"):
                yield Static("Loading preview...", id="preview-content")
            
            with Horizontal(id="button-row"):
                yield Button("← Back", id="btn-back", variant="default")
                yield Button("✓ Organize Files", id="btn-confirm", variant="success")
        
        yield Footer()

    def on_mount(self) -> None:
        """Handle screen mount."""
        self.load_preview()

    def load_preview(self) -> None:
        """Load organization preview."""
        try:
            self.preview_data = self.organizer.preview_organization()
            
            if not self.preview_data:
                preview_widget = self.query_one("#preview-content", Static)
                preview_widget.update(
                    "[yellow]No files to organize\n\n"
                    "All files are either already categorized or are unknown file types.[/yellow]"
                )
                # Disable confirm button
                confirm_btn = self.query_one("#btn-confirm", Button)
                confirm_btn.disabled = True
                return
            
            # Build preview text
            lines = ["\n[b cyan]Organization Preview:[/b cyan]\n"]
            
            total_files = 0
            for category in sorted(self.preview_data.keys()):
                files = self.preview_data[category]
                count = len(files)
                total_files += count
                
                lines.append(f"[green]📁 {category}[/green] ({count} files)")
                
                # Show first few files
                for file in files[:5]:
                    lines.append(f"   • {file}")
                
                if len(files) > 5:
                    lines.append(f"   [dim]... and {len(files) - 5} more files[/dim]")
                
                lines.append("")
            
            lines.append(f"[b]Total: {total_files} files across {len(self.preview_data)} categories[/b]\n")
            
            preview_text = "\n".join(lines)
            preview_widget = self.query_one("#preview-content", Static)
            preview_widget.update(preview_text)
            
        except Exception as e:
            preview_widget = self.query_one("#preview-content", Static)
            preview_widget.update(f"[red]Error loading preview: {e}[/red]")
            # Disable confirm button
            confirm_btn = self.query_one("#btn-confirm", Button)
            confirm_btn.disabled = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-back":
            self.app.pop_screen()
        elif event.button.id == "btn-confirm":
            self.do_organize()

    def do_organize(self) -> None:
        """Execute the organization."""
        if not self.preview_data:
            return
        
        # Show progress notification
        self.app.notify("Organizing files...", severity="information")
        
        try:
            result = self.organizer.organize_files(dry_run=False)
            
            if result.success:
                self.app.notify(
                    f"✅ {result.message}",
                    severity="information",
                    timeout=5
                )
                self.app.pop_screen()
            else:
                error_msg = f"Organized with errors:\n" + "\n".join(result.errors[:3])
                self.app.notify(error_msg, severity="warning", timeout=10)
                
        except Exception as e:
            self.app.notify(f"Error: {e}", severity="error", timeout=5)
