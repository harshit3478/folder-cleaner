# 🗂️ Folder Organizer v2.0

[![forthebadge](https://forthebadge.com/images/badges/check-it-out.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/built-with-swag.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

A beautiful, modern terminal-based folder organizer with an interactive TUI (Text User Interface) and powerful CLI capabilities. Clean and organize your folders in seconds with style! ✨

**New in v2.0:** Complete rewrite using Textual for a stunning terminal UI, global command-line access, and improved organization features.

## ✨ Features

- 🎨 **Beautiful TUI** - Modern terminal interface with smooth navigation
- ⚡ **Global Command** - Run `clean-folder` from anywhere on your system
- 📊 **Folder Stats** - Comprehensive folder analysis and statistics
- 🗂️ **Auto-Organize** - Intelligently categorize files by type
- 🔍 **Smart Search** - Search and count files by extension or name
- 📤 **File Moving** - Bulk move files by extension to any destination
- 🗑️ **Safe Deletion** - Delete files by extension with confirmation
- ⌨️ **Keyboard Shortcuts** - Navigate efficiently with keyboard
- 🎯 **Interactive & CLI Modes** - Use interactively or in scripts
- 🔒 **Safe Operations** - Preview before execution, confirmations for dangerous actions

## 📸 Screenshots

### Interactive TUI Mode
```
┌─────────────────────────────────────────────────┐
│  🗂️  Folder Organizer                          │
├─────────────────────────────────────────────────┤
│  📁 /Users/harshit/Downloads                    │
│  Press 'o' to change folder                     │
├─────────────────────────────────────────────────┤
│  📊 Folder Stats                                │
│  ├─ 💾 Size: 2.34 GB                            │
│  ├─ 📄 Files: 1,234                             │
│  ├─ 📂 Subfolders: 56                           │
│  └─ 🕐 Created: Nov 10, 2025                    │
├─────────────────────────────────────────────────┤
│  [1] 📦 Organize Files                          │
│  [2] 🔍 Search/Count Files                      │
│  [3] 📤 Move Files by Extension                 │
│  [4] 🗑️  Delete Files by Extension              │
│  [s] ⚙️  Settings                               │
└─────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Installation

1. **Clone or download the repository**
```bash
cd ~/dev
git clone https://github.com/harshit3478/folder-cleaner.git folder-organiser
cd folder-organiser
```

2. **Run the installation script**
```bash
chmod +x install.sh
./install.sh
```

3. **You're done!** The `clean-folder` command is now available globally.

### First Use

```bash
# Interactive mode for current directory
clean-folder

# Interactive mode for specific folder
clean-folder ~/Downloads

# Show folder information
clean-folder --info

# Quick organize with preview
clean-folder --organize

# Count PDF files
clean-folder --count .pdf
```

## 📖 Usage Guide

### Interactive TUI Mode (Default)

Simply run `clean-folder` to launch the beautiful terminal interface:

```bash
clean-folder                 # Current directory
clean-folder ~/Downloads     # Specific directory
```

**Keyboard Shortcuts:**
- `1` - Organize files
- `2` - Search/count files
- `3` - Move files by extension
- `4` - Delete files by extension
- `s` - Settings
- `o` - Change folder
- `q` or `Ctrl+C` - Quit
- `Esc` - Go back

### Command-Line Interface

For quick operations or scripting:

```bash
# Show folder information
clean-folder --info
clean-folder --path ~/Documents --info

# Organize files (with confirmation)
clean-folder --organize

# Auto-organize without confirmation
clean-folder --organize --yes

# Count files by extension
clean-folder --count .pdf
clean-folder --count .jpg

# Count files by name pattern
clean-folder --count "screenshot"

# Preview organization (dry run)
clean-folder --organize --dry-run

# Move all PDFs to a folder
clean-folder move .pdf ~/Documents/PDFs

# Delete all .tmp files (use with caution!)
clean-folder delete .tmp
```

### Use from Any Directory

The `clean-folder` command works from anywhere:

```bash
cd ~/Desktop
clean-folder              # Organizes Desktop

cd ~/Documents
clean-folder --organize   # Organizes Documents

# Or specify a path
clean-folder ~/Downloads --organize
```

## 🗂️ File Categories

Files are automatically organized into these categories:

| Category | Extensions |
|----------|-----------|
| **IMAGES** | .jpeg, .jpg, .tiff, .gif, .bmp, .png, .svg, .heic |
| **VIDEOS** | .avi, .flv, .wmv, .mkv, .mp4, .webm, .mpeg, .3gp |
| **AUDIOS** | .aac, .m4a, .m4p, .mp3, .ogg, .wav, .wma |
| **DOCS** | .doc, .docx, .odt, .wpd, .epub |
| **PDFS** | .pdf |
| **EXCEL** | .xls, .xlsx, .ods |
| **PPTs** | .ppt, .pptx |
| **PLAINTEXT** | .txt, .in, .out, .rtf, .md |
| **PROGRAMMING** | .java, .c, .cpp, .go, .pl, .rb, .bat, .py, .pyw |
| **WEB** | .html, .htm, .xhtml, .css, .js, .php, .jsx, .tsx, .ts |
| **DATAFILES** | .xml, .json, .csv, .dat |
| **ARCHIVES** | .iso, .tar, .gz, .7z, .rar, .zip |
| **EXE** | .exe, .deb, .dmg, .pkg, .msi, .apk |
| **SHELL** | .sh |

You can customize these categories in `data/filetypes.json`.

## 🔧 Advanced Usage

### Custom Configuration

Edit `~/.config/folder-organizer/config.json` to customize behavior:

```json
{
  "exclude_patterns": [".git", "node_modules", "__pycache__"],
  "auto_confirm": false,
  "theme": "dark"
}
```

### Integration with Scripts

```bash
#!/bin/bash
# Organize all project folders

for dir in ~/projects/*/; do
    echo "Organizing $dir"
    clean-folder "$dir" --organize --yes
done
```

## ⚠️ Safety Features

- **Confirmations** - Destructive operations require confirmation
- **Preview Mode** - See what will happen before executing
- **No Recycle Bin** - Deleted files are permanently removed (use with caution!)
- **Error Handling** - Graceful handling of permission errors and edge cases

## 🛠️ Development

### Project Structure

```
folder-organiser/
├── src/folder_organizer/
│   ├── __init__.py
│   ├── __main__.py          # Entry point
│   ├── app.py               # Main Textual app
│   ├── cli.py               # CLI interface
│   ├── organizer.py         # Core logic
│   ├── config.py            # Configuration
│   ├── screens/             # TUI screens
│   └── widgets/             # Custom widgets
├── data/
│   └── filetypes.json       # File type mappings
├── tests/
├── pyproject.toml
└── install.sh
```

### Running from Source

```bash
# Activate virtual environment
source venv/bin/activate

# Run directly
python -m folder_organizer

# Or use the installed command
clean-folder
```

### Running Tests

```bash
source venv/bin/activate
pytest tests/
```

## 🔄 Migration from v1.0

The old Tkinter GUI (`application.py`) is still available for backward compatibility. The new TUI version offers:

- ✅ Better performance
- ✅ Keyboard-driven navigation
- ✅ Works over SSH
- ✅ Global command access
- ✅ Scriptable CLI interface
- ✅ Modern, beautiful interface

## 📋 Requirements

- Python 3.8 or higher
- macOS, Linux, or WSL (Windows Subsystem for Linux)
- Terminal with Unicode support

Dependencies (automatically installed):
- `textual` - TUI framework
- `click` - CLI framework
- `rich` - Beautiful terminal output

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [Textual](https://textual.textualize.io/) - Amazing TUI framework
- Icons and styling inspired by modern terminal apps
- Original v1.0 GUI version inspired by folder organization needs

## 🐛 Known Issues & Roadmap

### Known Issues
- None currently reported

### Planned Features
- [ ] Undo functionality
- [ ] Custom organization rules
- [ ] Duplicate file detection
- [ ] Cloud storage integration
- [ ] Configuration GUI within TUI
- [ ] Multi-folder batch processing
- [ ] File preview in TUI

---

**Made with ❤️ by [harshit3478](https://github.com/harshit3478)**

*If you find this tool useful, please star ⭐ the repository!*