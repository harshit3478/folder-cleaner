#!/bin/bash

# Folder Organizer Installation Script
# This script sets up the folder organizer with a virtual environment

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🗂️  Installing Folder Organizer..."
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Found Python $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "  Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    echo "  ✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "  ✓ Pip upgraded"

# Install package in editable mode
echo ""
echo "📦 Installing folder-organizer and dependencies..."
pip install -e . 
echo "  ✓ Package installed"

# Create ~/bin directory if it doesn't exist
echo ""
echo "🔗 Setting up global command..."
mkdir -p ~/bin

# Create the clean-folder wrapper script
cat > ~/bin/clean-folder << 'EOF'
#!/bin/bash

# Folder Organizer CLI Wrapper
INSTALL_DIR="$HOME/dev/folder-organiser"

# Activate virtual environment and run the app
source "$INSTALL_DIR/venv/bin/activate"
python -m folder_organizer "$@"
EOF

# Make it executable
chmod +x ~/bin/clean-folder
echo "  ✓ Created ~/bin/clean-folder"

# Check if ~/bin is in PATH
if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
    echo ""
    echo "⚠️  Warning: ~/bin is not in your PATH"
    echo ""
    echo "Add this line to your ~/.zshrc:"
    echo "  export PATH=\"\$HOME/bin:\$PATH\""
    echo ""
    echo "Then run: source ~/.zshrc"
else
    echo "  ✓ ~/bin is already in PATH"
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "📚 Usage:"
echo "  clean-folder              # Interactive TUI for current folder"
echo "  clean-folder /path        # Interactive TUI for specific folder"
echo "  clean-folder --info       # Show folder information"
echo "  clean-folder --organize   # Quick organize"
echo "  clean-folder --count .pdf # Count PDF files"
echo ""
echo "Run 'clean-folder --help' for more options"
echo ""
