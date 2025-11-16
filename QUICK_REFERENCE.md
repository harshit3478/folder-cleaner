# 🗂️ Folder Organizer - Quick Reference Card

## 🚀 Installation
```bash
cd ~/dev/folder-organiser
./install.sh
```

## ⚡ Quick Commands

### Interactive Mode (TUI)
```bash
clean-folder                    # Current directory
clean-folder ~/Downloads        # Specific directory
```

### Command Line (Fast)
```bash
clean-folder --info             # Show folder stats
clean-folder --organize         # Organize (with confirmation)
clean-folder --organize --yes   # Auto-organize (no confirmation)
clean-folder --count .pdf       # Count PDF files
clean-folder --dry-run          # Preview without doing
```

## ⌨️ Keyboard Shortcuts (TUI)

| Key | Action |
|-----|--------|
| `1` | 📦 Organize Files |
| `2` | 🔍 Search/Count |
| `3` | 📤 Move Files |
| `4` | 🗑️  Delete Files |
| `s` | ⚙️  Settings |
| `o` | 📁 Change Folder |
| `q` | 🚪 Quit |
| `Esc` | ← Back |

## 📁 File Categories

- **IMAGES**: jpg, png, gif, svg, heic
- **VIDEOS**: mp4, mkv, avi, mov
- **AUDIOS**: mp3, wav, m4a, ogg
- **DOCS**: doc, docx, odt, epub
- **PDFS**: pdf
- **EXCEL**: xls, xlsx, ods
- **PPTs**: ppt, pptx
- **PROGRAMMING**: py, js, java, cpp
- **WEB**: html, css, js, php
- **ARCHIVES**: zip, rar, tar, gz
- **And more...**

## 🎯 Common Tasks

### Clean Downloads
```bash
clean-folder ~/Downloads --organize --yes
```

### Find All PDFs
```bash
clean-folder --count .pdf
```

### Move All Screenshots
```bash
clean-folder move .png ~/Pictures/Screenshots
```

### Check Folder Size
```bash
clean-folder --info
```

## 💡 Pro Tips

### Create Aliases
Add to `~/.zshrc`:
```bash
alias clean-dl='clean-folder ~/Downloads --organize --yes'
alias clean-desk='clean-folder ~/Desktop --organize --yes'
```

### Quick Organize
```bash
cd ~/Downloads && clean-folder --organize --yes
```

### Safe Delete
```bash
# Count first
clean-folder --count .tmp

# Then delete
clean-folder delete .tmp
```

## ⚠️ Safety

- ✅ Preview before organize
- ✅ Confirmation for delete
- ✅ Dry-run mode available
- ⚠️ Delete is permanent!

## 🆘 Help

```bash
clean-folder --help              # General help
clean-folder move --help         # Command help
cat ~/dev/folder-organiser/USAGE_GUIDE.md
```

## 🔧 Files

- **Config**: `~/.config/folder-organizer/config.json`
- **Categories**: `~/dev/folder-organiser/data/filetypes.json`
- **Command**: `~/bin/clean-folder`

---

**Version**: 2.0.0 | **Docs**: README.md, USAGE_GUIDE.md
