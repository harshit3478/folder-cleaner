# 🗂️ Folder Organizer - Complete Usage Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Interactive TUI Mode](#interactive-tui-mode)
3. [Command-Line Mode](#command-line-mode)
4. [Common Workflows](#common-workflows)
5. [Tips & Tricks](#tips--tricks)
6. [Troubleshooting](#troubleshooting)

## Getting Started

### Installation Verification

After running `install.sh`, verify the installation:

```bash
# Check if command is available
which clean-folder
# Should output: /Users/harshit/bin/clean-folder

# Check version
clean-folder --help
```

### First Run

The easiest way to start is with interactive mode:

```bash
cd ~/Downloads
clean-folder
```

This launches the TUI (Text User Interface) for the current directory.

## Interactive TUI Mode

### Launching TUI

```bash
# Current directory
clean-folder

# Specific directory
clean-folder ~/Documents

# Or with --path flag
clean-folder --path ~/Desktop
```

### Navigation

**Main Menu:**
- `1` or Click - Organize Files
- `2` or Click - Search/Count Files
- `3` or Click - Move Files
- `4` or Click - Delete Files
- `s` or Click - Settings
- `o` - Change target folder
- `q` or `Ctrl+C` - Quit

**In Screens:**
- `Esc` - Go back to main menu
- `Tab` - Navigate between elements
- `Enter` - Confirm/Select
- Arrow keys - Navigate lists

### Features in TUI

#### 1. Folder Stats (Automatic)
Displays immediately:
- Total size
- File count
- Subfolder count
- Creation date

#### 2. Organize Files
1. Press `1` or click "Organize Files"
2. Preview shows:
   - Categories that will be created
   - Files in each category
   - Total files to organize
3. Press `Enter` or click "Organize" to confirm
4. Files are moved to category folders

**Example:**
```
Before:
~/Downloads/
  photo.jpg
  document.pdf
  song.mp3

After:
~/Downloads/
  IMAGES/
    photo.jpg
  PDFS/
    document.pdf
  AUDIOS/
    song.mp3
```

#### 3. Search/Count Files
1. Press `2` or click "Search/Count Files"
2. Enter search term:
   - Extension: `.pdf`, `.jpg`
   - Pattern: `screenshot`, `invoice`
3. View results with file list

#### 4. Move Files
1. Press `3` or click "Move Files"
2. Enter file extension (e.g., `.pdf`)
3. Choose destination folder
4. Confirm to move all matching files

**Use case:** Move all PDFs to your Documents folder

#### 5. Delete Files
1. Press `4` or click "Delete Files"
2. Enter file extension (e.g., `.tmp`)
3. Preview files to be deleted
4. Confirm (requires typing "yes")

⚠️ **Warning:** This permanently deletes files!

## Command-Line Mode

Perfect for quick operations and scripts.

### Info Command

Get folder statistics without opening TUI:

```bash
# Current directory
clean-folder --info

# Specific directory
clean-folder ~/Downloads --info
```

Output:
```
📊 Folder Information
📁 Path: /Users/harshit/Downloads
💾 Size: 2.34 GB
📄 Files: 1,234
📂 Subfolders: 56
🕐 Created: Nov 10, 2025
```

### Organize Command

Auto-organize files:

```bash
# With confirmation prompt
clean-folder --organize

# Skip confirmation
clean-folder --organize --yes

# Specific directory
clean-folder ~/Downloads --organize --yes

# Preview only (dry run)
clean-folder --organize --dry-run
```

### Count Command

Count files by extension or pattern:

```bash
# Count PDFs in current directory
clean-folder --count .pdf

# Count in specific directory
clean-folder ~/Documents --count .docx

# Count by name pattern
clean-folder --count "screenshot"
clean-folder --count "IMG_"
```

### Move Command

Move files by extension:

```bash
# Move PDFs to Documents
clean-folder move .pdf ~/Documents/PDFs

# Move images to Pictures
clean-folder move .jpg ~/Pictures/FromDownloads
```

### Delete Command

⚠️ **Dangerous!** Use with caution:

```bash
# Delete all .tmp files
clean-folder delete .tmp

# With confirmation
clean-folder delete .log
```

## Common Workflows

### Workflow 1: Clean Downloads Folder

```bash
cd ~/Downloads
clean-folder
# Press 1 to organize
# Review preview
# Confirm
```

All files automatically sorted into:
- IMAGES/
- DOCS/
- PDFS/
- VIDEOS/
- etc.

### Workflow 2: Find and Move All PDFs

```bash
# Method 1: Interactive
clean-folder ~/Downloads
# Press 3
# Enter: .pdf
# Choose destination: ~/Documents/PDFs

# Method 2: CLI
clean-folder ~/Downloads move .pdf ~/Documents/PDFs
```

### Workflow 3: Clean Up Temporary Files

```bash
# Find them first
clean-folder --count .tmp

# Delete if safe
clean-folder delete .tmp
```

### Workflow 4: Regular Folder Maintenance

Create a shell alias in `~/.zshrc`:

```bash
alias clean-dl='clean-folder ~/Downloads --organize --yes'
alias clean-desk='clean-folder ~/Desktop --organize --yes'
```

Then simply:
```bash
clean-dl    # Organizes Downloads
clean-desk  # Organizes Desktop
```

### Workflow 5: Batch Processing Multiple Folders

Create a script `~/bin/clean-all`:

```bash
#!/bin/bash
# Clean all common folders

echo "🧹 Cleaning all folders..."

clean-folder ~/Downloads --organize --yes
clean-folder ~/Desktop --organize --yes
clean-folder ~/Documents --organize --yes

echo "✅ All folders cleaned!"
```

Make it executable:
```bash
chmod +x ~/bin/clean-all
```

Run anytime:
```bash
clean-all
```

## Tips & Tricks

### 1. Quick Access with Shell Functions

Add to `~/.zshrc`:

```bash
# Quick organize current folder
qo() {
    clean-folder --organize --yes
}

# Quick info
qi() {
    clean-folder --info
}

# Organize specific folder
odir() {
    clean-folder "$1" --organize --yes
}
```

Usage:
```bash
cd ~/Downloads
qo                    # Organize current folder
qi                    # Show info
odir ~/Desktop        # Organize Desktop
```

### 2. Custom File Categories

Edit `data/filetypes.json`:

```json
{
  "DESIGNS": [".fig", ".sketch", ".psd", ".ai"],
  "CODE": [".py", ".js", ".java"],
  "SCREENSHOTS": [".png"]
}
```

### 3. Exclude Patterns

Some folders should never be organized (e.g., `.git`, `node_modules`).

The organizer automatically skips:
- Hidden files/folders (starting with `.`)
- System folders
- Already organized category folders

### 4. Organize Before Cleanup

Good practice:
```bash
# 1. Organize first
clean-folder --organize

# 2. Then review and delete unwanted files
clean-folder
# Use TUI to selectively delete
```

### 5. Use with `find` for Advanced Filtering

```bash
# Find large files before organizing
find ~/Downloads -type f -size +100M

# Find old files
find ~/Downloads -type f -mtime +30
```

## Troubleshooting

### Command Not Found

```bash
-bash: clean-folder: command not found
```

**Solution:**
1. Check if `~/bin` is in PATH:
   ```bash
   echo $PATH | grep "$HOME/bin"
   ```

2. If not, add to `~/.zshrc`:
   ```bash
   export PATH="$HOME/bin:$PATH"
   ```

3. Reload:
   ```bash
   source ~/.zshrc
   ```

### Permission Errors

```
Error: Permission denied
```

**Solution:**
- Run with proper permissions
- Check folder ownership: `ls -la`
- Some system folders are protected

### Files Not Organizing

**Possible reasons:**
1. Unknown file extension (not in `filetypes.json`)
2. Files already in category folders
3. Hidden files (add `--include-hidden` flag - coming soon)

**Solution:**
- Add custom extensions to `data/filetypes.json`
- Check file extensions: `ls -la`

### TUI Not Displaying Properly

```
Characters look weird or boxes are broken
```

**Solution:**
1. Use a modern terminal (iTerm2, Alacritty, Warp)
2. Ensure UTF-8 encoding:
   ```bash
   echo $LANG
   # Should show: en_US.UTF-8
   ```

### Virtual Environment Issues

```
ModuleNotFoundError: No module named 'textual'
```

**Solution:**
1. Reinstall:
   ```bash
   cd ~/dev/folder-organiser
   ./install.sh
   ```

2. Or manually activate:
   ```bash
   source ~/dev/folder-organiser/venv/bin/activate
   python -m folder_organizer
   ```

## Advanced Examples

### Example 1: Organize Only Recent Files

```bash
# Move recent downloads to temp folder
find ~/Downloads -type f -mtime -7 -exec mv {} ~/Downloads/Recent \;

# Organize just that folder
clean-folder ~/Downloads/Recent --organize --yes
```

### Example 2: Scheduled Cleanup (with cron)

Add to crontab (`crontab -e`):

```bash
# Organize Downloads every Sunday at 2 AM
0 2 * * 0 /Users/harshit/bin/clean-folder /Users/harshit/Downloads --organize --yes
```

### Example 3: Pre-commit Hook

Organize project folder before commits:

`.git/hooks/pre-commit`:
```bash
#!/bin/bash
clean-folder . --organize --yes
git add .
```

### Example 4: Integration with Finder (macOS)

Create Automator Quick Action:
1. Open Automator
2. New Quick Action
3. Add "Run Shell Script"
4. Paste:
   ```bash
   /Users/harshit/bin/clean-folder "$1" --organize --yes
   ```
5. Save as "Organize Folder"

Now right-click any folder → Quick Actions → Organize Folder

## Getting Help

```bash
# General help
clean-folder --help

# Command-specific help
clean-folder move --help
clean-folder delete --help
```

## Keyboard Shortcuts Reference

| Key | Action |
|-----|--------|
| `1` | Organize files |
| `2` | Search/count |
| `3` | Move files |
| `4` | Delete files |
| `s` | Settings |
| `o` | Change folder |
| `q` | Quit |
| `Ctrl+C` | Quit |
| `Esc` | Go back |
| `Tab` | Next element |
| `Shift+Tab` | Previous element |
| `Enter` | Confirm/Select |
| `↑↓` | Navigate lists |

---

**Happy Organizing! 🗂️✨**
