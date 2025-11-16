"""Core folder organization logic - framework agnostic."""

import os
import time
import json
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass


@dataclass
class OperationResult:
    """Result of a file operation."""
    success: bool
    files_affected: int
    files_list: List[str]
    errors: List[str]
    message: str


class FolderOrganizer:
    """Handles all folder organization operations."""

    def __init__(self, path: str, filetypes_path: Optional[str] = None):
        """
        Initialize the folder organizer.
        
        Args:
            path: Path to the folder to organize
            filetypes_path: Path to filetypes.json (optional)
        """
        self.path = Path(path).resolve()
        
        if not self.path.exists():
            raise ValueError(f"Path does not exist: {path}")
        if not self.path.is_dir():
            raise ValueError(f"Path is not a directory: {path}")
        
        # Load file types mapping
        if filetypes_path is None:
            # Default to data/filetypes.json relative to package
            package_dir = Path(__file__).parent.parent.parent
            filetypes_path = str(package_dir / "data" / "filetypes.json")
        
        with open(filetypes_path) as f:
            self.filetypes = json.load(f)

    def get_meta(self) -> Dict[str, Any]:
        """
        Get metadata about the folder.
        
        Returns:
            Dictionary containing folder metadata
        """
        folder_list = []
        filecount = 0
        total_size = self.path.stat().st_size

        for dirpath, dirnames, filenames in os.walk(self.path):
            for dirname in dirnames:
                if dirname not in folder_list:
                    folder_list.append(dirname)
            
            for filename in filenames:
                fp = Path(dirpath) / filename
                # Skip if it is symbolic link
                if not fp.is_symlink():
                    try:
                        filecount += 1
                        total_size += fp.stat().st_size
                    except (OSError, PermissionError):
                        # Skip files we can't access
                        pass

        # Format size
        size_mb = total_size / (1024 * 1024)
        if size_mb < 1000:
            size_str = f"{size_mb:.2f} MB"
        else:
            size_str = f"{size_mb / 1024:.2f} GB"

        # Format creation time
        creation_time = time.ctime(self.path.stat().st_ctime)
        creation_time_formatted = (
            creation_time[4:10] + ' ' + creation_time[-4:] + ', ' + creation_time[11:16]
        )

        return {
            'size': size_str,
            'size_bytes': total_size,
            'folder_count': len(folder_list),
            'file_count': filecount,
            'creation_time': creation_time_formatted,
            'path': str(self.path)
        }

    def get_filecount(self, term: str) -> int:
        """
        Count files matching a search term.
        
        Args:
            term: Search term (substring or extension)
            
        Returns:
            Number of matching files
        """
        filecount = 0
        try:
            for item in self.path.iterdir():
                if item.is_file() and term.lower() in item.name.lower():
                    filecount += 1
        except PermissionError:
            pass
        
        return filecount

    def search_files(self, term: str) -> List[Dict[str, Any]]:
        """
        Search for files matching a term and return detailed info.
        
        Args:
            term: Search term (substring or extension)
            
        Returns:
            List of file information dictionaries
        """
        files = []
        try:
            for item in self.path.iterdir():
                if item.is_file() and term.lower() in item.name.lower():
                    try:
                        size = item.stat().st_size
                        files.append({
                            'name': item.name,
                            'size': size,
                            'size_formatted': self._format_size(size),
                            'modified': time.ctime(item.stat().st_mtime),
                            'path': str(item)
                        })
                    except (OSError, PermissionError):
                        pass
        except PermissionError:
            pass
        
        return files

    def move_files(self, extension: str, destination: str, dry_run: bool = False) -> OperationResult:
        """
        Move files with a specific extension to a destination.
        
        Args:
            extension: File extension (with or without dot)
            destination: Destination directory path
            dry_run: If True, only preview without actually moving
            
        Returns:
            OperationResult with operation details
        """
        # Normalize extension
        if not extension.startswith('.'):
            extension = '.' + extension
        
        dest_path = Path(destination).resolve()
        if not dest_path.exists():
            return OperationResult(
                success=False,
                files_affected=0,
                files_list=[],
                errors=[f"Destination does not exist: {destination}"],
                message="Destination path does not exist"
            )
        
        if dest_path == self.path:
            return OperationResult(
                success=False,
                files_affected=0,
                files_list=[],
                errors=["Cannot move files to the same folder"],
                message="Source and destination are the same"
            )

        moved_files = []
        errors = []
        
        try:
            for item in self.path.iterdir():
                if item.is_file() and item.suffix.lower() == extension.lower():
                    if not dry_run:
                        try:
                            dest_file = dest_path / item.name
                            shutil.move(str(item), str(dest_file))
                            moved_files.append(item.name)
                        except Exception as e:
                            errors.append(f"{item.name}: {str(e)}")
                    else:
                        moved_files.append(item.name)
        except PermissionError as e:
            errors.append(f"Permission denied: {str(e)}")

        count = len(moved_files)
        message = f"{count} file{'s' if count != 1 else ''} {'would be' if dry_run else ''} moved"
        
        return OperationResult(
            success=len(errors) == 0,
            files_affected=count,
            files_list=moved_files,
            errors=errors,
            message=message
        )

    def delete_files(self, extension: str, dry_run: bool = False) -> OperationResult:
        """
        Delete files with a specific extension.
        
        Args:
            extension: File extension (with or without dot)
            dry_run: If True, only preview without actually deleting
            
        Returns:
            OperationResult with operation details
        """
        # Normalize extension
        if not extension.startswith('.'):
            extension = '.' + extension

        deleted_files = []
        errors = []
        
        try:
            for item in self.path.iterdir():
                if item.is_file() and item.suffix.lower() == extension.lower():
                    if not dry_run:
                        try:
                            item.unlink()
                            deleted_files.append(item.name)
                        except Exception as e:
                            errors.append(f"{item.name}: {str(e)}")
                    else:
                        deleted_files.append(item.name)
        except PermissionError as e:
            errors.append(f"Permission denied: {str(e)}")

        count = len(deleted_files)
        message = (
            f"{count} file{'s' if count != 1 else ''} "
            f"{'would be' if dry_run else ''} deleted permanently"
        )
        
        return OperationResult(
            success=len(errors) == 0,
            files_affected=count,
            files_list=deleted_files,
            errors=errors,
            message=message
        )

    def organize_files(self, dry_run: bool = False) -> OperationResult:
        """
        Organize files into category folders based on file types.
        
        Args:
            dry_run: If True, only preview without actually organizing
            
        Returns:
            OperationResult with operation details
        """
        organized_files = []
        errors = []
        categories_used = set()

        try:
            for item in self.path.iterdir():
                if not item.is_file():
                    continue
                
                extension = item.suffix.lower()
                category = None
                
                # Find matching category
                for cat, extensions in self.filetypes.items():
                    if extension in extensions:
                        category = cat
                        break
                
                if category is None:
                    continue  # Skip unknown file types
                
                categories_used.add(category)
                category_folder = self.path / category
                
                if not dry_run:
                    try:
                        # Create category folder if it doesn't exist
                        category_folder.mkdir(exist_ok=True)
                        
                        # Move file
                        dest_file = category_folder / item.name
                        shutil.move(str(item), str(dest_file))
                        organized_files.append(item.name)
                    except Exception as e:
                        errors.append(f"{item.name}: {str(e)}")
                else:
                    organized_files.append(item.name)
                    
        except PermissionError as e:
            errors.append(f"Permission denied: {str(e)}")

        count = len(organized_files)
        cat_count = len(categories_used)
        message = (
            f"{count} file{'s' if count != 1 else ''} "
            f"{'would be' if dry_run else ''} organized into {cat_count} "
            f"categor{'ies' if cat_count != 1 else 'y'}"
        )
        
        return OperationResult(
            success=len(errors) == 0,
            files_affected=count,
            files_list=organized_files,
            errors=errors,
            message=message
        )

    def preview_organization(self) -> Dict[str, List[str]]:
        """
        Preview how files would be organized without actually moving them.
        
        Returns:
            Dictionary mapping category names to lists of file names
        """
        preview = {}
        
        try:
            for item in self.path.iterdir():
                if not item.is_file():
                    continue
                
                extension = item.suffix.lower()
                
                # Find matching category
                for category, extensions in self.filetypes.items():
                    if extension in extensions:
                        if category not in preview:
                            preview[category] = []
                        preview[category].append(item.name)
                        break
        except PermissionError:
            pass
        
        return preview

    @staticmethod
    def _format_size(size_bytes: Union[int, float]) -> str:
        """Format size in bytes to human-readable string."""
        size = float(size_bytes)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"
