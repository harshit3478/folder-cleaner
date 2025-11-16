"""Delete files screen."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button, Input, Label
from textual.containers import Container, Vertical, Horizontal


class DeleteScreen(Screen):
    """Screen for deleting files by extension (with warnings!)."""

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("q", "app.pop_screen", "Back"),
    ]

    def __init__(self, organizer):
        super().__init__()
        self.organizer = organizer
        self.extension = None

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        
        with Container(id="delete-container"):
            yield Static("🗑️  Delete Files by Extension", classes="screen-title")
            yield Static(
                "[red b]⚠️  WARNING: This will PERMANENTLY delete files![/red b]",
                classes="warning"
            )
            yield Static(
                "[dim]Files will not go to trash - they will be gone forever![/dim]",
                classes="description"
            )
            
            yield Label("Extension (with dot, e.g., .tmp):")
            yield Input(placeholder=".tmp", id="extension-input")
            
            yield Static("", id="preview-text")
            
            with Horizontal(id="button-row"):
                yield Button("← Back", id="btn-back", variant="default")
                yield Button("Preview", id="btn-preview", variant="primary")
                yield Button("⚠️  Delete Files", id="btn-confirm", variant="error", disabled=True)
        
        yield Footer()

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes."""
        if event.input.id == "extension-input":
            self.extension = event.value
            
            # Enable preview if extension entered
            preview_btn = self.query_one("#btn-preview", Button)
            preview_btn.disabled = not self.extension

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-back":
            self.app.pop_screen()
        elif event.button.id == "btn-preview":
            self.do_preview()
        elif event.button.id == "btn-confirm":
            self.confirm_delete()

    def do_preview(self) -> None:
        """Preview the delete operation."""
        if not self.extension:
            return
        
        try:
            result = self.organizer.delete_files(self.extension, dry_run=True)
            
            if result.files_affected == 0:
                preview_widget = self.query_one("#preview-text", Static)
                preview_widget.update(
                    f"\n[yellow]No files found with extension '{self.extension}'[/yellow]\n"
                )
                confirm_btn = self.query_one("#btn-confirm", Button)
                confirm_btn.disabled = True
                return
            
            # Show preview with big warning
            lines = [
                f"\n[red b]⚠️  {result.files_affected} file(s) will be PERMANENTLY DELETED:[/red b]\n"
            ]
            
            for file in result.files_list[:30]:
                lines.append(f"  [red]✗[/red] {file}")
            
            if len(result.files_list) > 30:
                lines.append(f"\n  [dim]... and {len(result.files_list) - 30} more files[/dim]")
            
            lines.append("\n[yellow]⚠️  This action cannot be undone![/yellow]\n")
            
            preview_text = "\n".join(lines)
            preview_widget = self.query_one("#preview-text", Static)
            preview_widget.update(preview_text)
            
            # Enable confirm button
            confirm_btn = self.query_one("#btn-confirm", Button)
            confirm_btn.disabled = False
            
        except Exception as e:
            preview_widget = self.query_one("#preview-text", Static)
            preview_widget.update(f"\n[red]Error: {e}[/red]\n")

    def confirm_delete(self) -> None:
        """Show final confirmation before deletion."""
        if not self.extension:
            return
        
        # Use Textual's built-in notification for final confirmation
        def do_actual_delete():
            self.app.notify("Deleting files...", severity="warning")
            
            try:
                result = self.organizer.delete_files(self.extension, dry_run=False)
                
                if result.success:
                    self.app.notify(
                        f"✅ {result.message}",
                        severity="information",
                        timeout=5
                    )
                    self.app.pop_screen()
                else:
                    error_msg = "Deletion completed with errors:\n" + "\n".join(result.errors[:3])
                    self.app.notify(error_msg, severity="error", timeout=10)
                    
            except Exception as e:
                self.app.notify(f"Error: {e}", severity="error", timeout=5)
        
        # For now, just warn and do it - ideally we'd have a modal dialog
        self.app.notify(
            "⚠️  Deleting files permanently!",
            severity="warning",
            timeout=2
        )
        
        # Small delay then delete
        self.set_timer(2.0, do_actual_delete)
