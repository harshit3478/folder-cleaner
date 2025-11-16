"""Command-line interface for folder organizer."""

import sys
import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from folder_organizer.organizer import FolderOrganizer
from folder_organizer.config import Config


console = Console()


@click.group(invoke_without_command=True)
@click.option('--path', '-p', type=click.Path(exists=True), help='Folder to organize')
@click.option('--info', is_flag=True, help='Show folder information')
@click.option('--organize', is_flag=True, help='Organize files by type')
@click.option('--count', type=str, help='Count files by extension or search term')
@click.option('--yes', '-y', is_flag=True, help='Auto-confirm actions')
@click.option('--dry-run', is_flag=True, help='Preview changes without executing')
@click.pass_context
def cli(ctx, path, info, organize, count, yes, dry_run):
    """
    🗂️  Folder Organizer - Beautiful terminal-based folder management
    
    Run without options for interactive TUI mode.
    """
    # If no command and no flags, launch TUI
    if ctx.invoked_subcommand is None and not any([info, organize, count]):
        from folder_organizer.app import FolderOrganizerApp
        
        target_path = path or '.'
        app = FolderOrganizerApp(target_path)
        app.run()
        return

    # CLI mode
    target_path = Path(path or '.').resolve()
    
    try:
        organizer = FolderOrganizer(str(target_path))
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

    # Handle --info flag
    if info:
        show_info(organizer)
        return

    # Handle --count flag
    if count:
        show_count(organizer, count)
        return

    # Handle --organize flag
    if organize:
        organize_files(organizer, yes, dry_run)
        return


def show_info(organizer: FolderOrganizer):
    """Display folder information."""
    meta = organizer.get_meta()
    
    table = Table(title=f"📊 Folder Information", show_header=False, box=None)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("📁 Path", meta['path'])
    table.add_row("💾 Size", meta['size'])
    table.add_row("📄 Files", str(meta['file_count']))
    table.add_row("📂 Subfolders", str(meta['folder_count']))
    table.add_row("🕐 Created", meta['creation_time'])
    
    console.print(table)


def show_count(organizer: FolderOrganizer, term: str):
    """Show file count for a search term."""
    count = organizer.get_filecount(term)
    files = organizer.search_files(term)
    
    if count == 0:
        console.print(f"[yellow]No files found matching '[bold]{term}[/bold]'[/yellow]")
        return
    
    console.print(f"\n[green]Found {count} file(s) matching '[bold]{term}[/bold]'[/green]\n")
    
    if files:
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("File Name", style="white")
        table.add_column("Size", justify="right", style="yellow")
        table.add_column("Modified", style="dim")
        
        for file in files[:20]:  # Show first 20
            table.add_row(
                file['name'],
                file['size_formatted'],
                file['modified'][4:16]  # Shortened date
            )
        
        console.print(table)
        
        if len(files) > 20:
            console.print(f"\n[dim]... and {len(files) - 20} more files[/dim]")


def organize_files(organizer: FolderOrganizer, auto_confirm: bool, dry_run: bool):
    """Organize files into category folders."""
    # Preview organization
    preview = organizer.preview_organization()
    
    if not preview:
        console.print("[yellow]No files to organize (all files are already categorized or unknown types)[/yellow]")
        return
    
    # Show preview
    console.print("\n[bold cyan]📋 Organization Preview:[/bold cyan]\n")
    
    table = Table(show_header=True, header_style="bold green")
    table.add_column("Category", style="cyan")
    table.add_column("Files", justify="right", style="yellow")
    table.add_column("Examples", style="dim")
    
    total_files = 0
    for category, files in sorted(preview.items()):
        count = len(files)
        total_files += count
        examples = ", ".join(files[:3])
        if len(files) > 3:
            examples += f" ... (+{len(files) - 3} more)"
        table.add_row(category, str(count), examples)
    
    console.print(table)
    console.print(f"\n[bold]Total: {total_files} files across {len(preview)} categories[/bold]\n")
    
    # Confirm
    if dry_run:
        console.print("[yellow]🔍 Dry run mode - no files will be moved[/yellow]")
        return
    
    if not auto_confirm:
        if not click.confirm("Proceed with organization?"):
            console.print("[yellow]Operation cancelled[/yellow]")
            return
    
    # Execute organization
    with console.status("[bold green]Organizing files...", spinner="dots"):
        result = organizer.organize_files(dry_run=False)
    
    if result.success:
        console.print(f"\n[bold green]✅ {result.message}[/bold green]")
    else:
        console.print(f"\n[bold red]❌ Organization completed with errors[/bold red]")
        for error in result.errors:
            console.print(f"[red]  • {error}[/red]")


@cli.command()
@click.argument('path', type=click.Path(exists=True), required=False, default='.')
def tui(path):
    """Launch interactive TUI mode."""
    from folder_organizer.app import FolderOrganizerApp
    
    app = FolderOrganizerApp(path)
    app.run()


@cli.command()
def config():
    """Open configuration editor."""
    from folder_organizer.config import Config
    
    cfg = Config()
    console.print(f"\n[cyan]Configuration file:[/cyan] {cfg.config_path}\n")
    
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Setting", style="yellow")
    table.add_column("Value", style="green")
    
    for key, value in cfg.config.items():
        table.add_row(key, str(value))
    
    console.print(table)
    console.print(f"\n[dim]Edit the file directly to modify settings[/dim]\n")


@cli.command()
@click.argument('path', type=click.Path(exists=True), required=False, default='.')
@click.argument('extension', type=str)
@click.argument('destination', type=click.Path(exists=True))
@click.option('--yes', '-y', is_flag=True, help='Auto-confirm action')
@click.option('--dry-run', is_flag=True, help='Preview without moving')
def move(path, extension, destination, yes, dry_run):
    """Move files with EXTENSION to DESTINATION."""
    organizer = FolderOrganizer(path)
    
    result = organizer.move_files(extension, destination, dry_run=True)
    
    if result.files_affected == 0:
        console.print(f"[yellow]No files found with extension '{extension}'[/yellow]")
        return
    
    console.print(f"\n[cyan]Found {result.files_affected} file(s) to move:[/cyan]")
    for file in result.files_list[:10]:
        console.print(f"  • {file}")
    if len(result.files_list) > 10:
        console.print(f"  [dim]... and {len(result.files_list) - 10} more[/dim]")
    
    if dry_run:
        console.print(f"\n[yellow]🔍 Dry run mode - no files will be moved[/yellow]")
        return
    
    if not yes:
        if not click.confirm(f"\nMove these files to {destination}?"):
            console.print("[yellow]Operation cancelled[/yellow]")
            return
    
    result = organizer.move_files(extension, destination, dry_run=False)
    
    if result.success:
        console.print(f"\n[green]✅ {result.message}[/green]")
    else:
        console.print(f"\n[red]❌ Move completed with errors[/red]")
        for error in result.errors:
            console.print(f"[red]  • {error}[/red]")


@cli.command()
@click.argument('path', type=click.Path(exists=True), required=False, default='.')
@click.argument('extension', type=str)
@click.option('--yes', '-y', is_flag=True, help='Auto-confirm action')
@click.option('--dry-run', is_flag=True, help='Preview without deleting')
def delete(path, extension, yes, dry_run):
    """Delete files with EXTENSION (DANGEROUS!)."""
    organizer = FolderOrganizer(path)
    
    result = organizer.delete_files(extension, dry_run=True)
    
    if result.files_affected == 0:
        console.print(f"[yellow]No files found with extension '{extension}'[/yellow]")
        return
    
    console.print(f"\n[red]⚠️  WARNING: This will permanently delete {result.files_affected} file(s)![/red]\n")
    for file in result.files_list[:10]:
        console.print(f"  • {file}")
    if len(result.files_list) > 10:
        console.print(f"  [dim]... and {len(result.files_list) - 10} more[/dim]")
    
    if dry_run:
        console.print(f"\n[yellow]🔍 Dry run mode - no files will be deleted[/yellow]")
        return
    
    if not yes:
        if not click.confirm(f"\n[bold red]Are you absolutely sure?[/bold red]", default=False):
            console.print("[yellow]Operation cancelled[/yellow]")
            return
    
    result = organizer.delete_files(extension, dry_run=False)
    
    if result.success:
        console.print(f"\n[green]✅ {result.message}[/green]")
    else:
        console.print(f"\n[red]❌ Delete completed with errors[/red]")
        for error in result.errors:
            console.print(f"[red]  • {error}[/red]")


def main():
    """Main entry point."""
    cli()


if __name__ == '__main__':
    main()
