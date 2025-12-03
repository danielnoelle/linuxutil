#!/bin/bash
# Installation script for Linux App Installer

echo "╔══════════════════════════════════════════╗"
echo "║   Linux App Installer - Setup Script    ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Installing pip..."
    sudo apt install python3-pip -y || sudo dnf install python3-pip -y || sudo pacman -S python-pip --noconfirm
fi

echo "✓ pip3 found"
echo ""

# Install required Python packages
echo "📦 Installing required Python packages..."
pip3 install --user -r requirements.txt

echo ""
echo "✓ Installation complete!"
echo ""
echo "To run the app installer:"
echo "  python3 app_installer.py"
echo ""
echo "Or make it executable:"
echo "  chmod +x app_installer.py"
echo "  ./app_installer.py"
echo ""
