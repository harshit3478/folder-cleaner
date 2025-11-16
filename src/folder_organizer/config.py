"""Configuration management for folder organizer."""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional


class Config:
    """Manages user configuration."""

    DEFAULT_CONFIG = {
        "default_action": "interactive",
        "auto_confirm": False,
        "exclude_patterns": [".git", "node_modules", "__pycache__", ".DS_Store", "venv"],
        "custom_categories": {},
        "theme": "dark",
        "remember_last_folder": True,
        "enable_undo": True,
        "max_undo_history": 10,
    }

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_path: Path to config file (defaults to ~/.config/folder-organizer/config.json)
        """
        if config_path is None:
            config_dir = Path.home() / ".config" / "folder-organizer"
            config_dir.mkdir(parents=True, exist_ok=True)
            self.config_path = config_dir / "config.json"
        else:
            self.config_path = Path(config_path)

        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                # Merge with defaults to ensure all keys exist
                config = self.DEFAULT_CONFIG.copy()
                config.update(loaded_config)
                return config
            except (json.JSONDecodeError, IOError):
                # If config is corrupted, use defaults
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create default config file
            self.save()
            return self.DEFAULT_CONFIG.copy()

    def save(self) -> None:
        """Save configuration to file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value and save."""
        self.config[key] = value
        self.save()

    def reset(self) -> None:
        """Reset configuration to defaults."""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save()

    @property
    def exclude_patterns(self) -> List[str]:
        """Get list of patterns to exclude from operations."""
        return self.config.get("exclude_patterns", [])

    @property
    def custom_categories(self) -> Dict[str, List[str]]:
        """Get custom file type categories."""
        return self.config.get("custom_categories", {})

    def should_exclude(self, path: Path) -> bool:
        """
        Check if a path should be excluded based on exclude patterns.
        
        Args:
            path: Path to check
            
        Returns:
            True if path should be excluded
        """
        name = path.name
        for pattern in self.exclude_patterns:
            if pattern in name:
                return True
        return False
