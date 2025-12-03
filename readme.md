# ✨ Linux App Installer

A beautiful, intuitive TUI (Text User Interface) application for installing Linux software organized by category. Features a modern, aesthetic design inspired by Gemini CLI with rich colors, smooth interactions, and an elegant interface.

![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue?style=for-the-badge&logo=python)
![Textual](https://img.shields.io/badge/Powered%20by-Textual-purple?style=for-the-badge)

## 🎯 Features

- **📦 Multi-Category Organization**: Apps organized into Development, Multimedia, Internet & Communication, System Tools, Productivity, and Gaming
- **🎨 Beautiful TUI**: Modern, colorful interface inspired by Gemini CLI aesthetics
- **🔄 Auto Package Manager Detection**: Automatically detects and uses apt, dnf, or pacman
- **✅ Batch Installation**: Select multiple apps and install them all at once
- **⚡ Keyboard Shortcuts**: Efficient navigation with vim-inspired keybindings
- **📊 Real-time Progress**: Live installation logs and progress updates
- **🎯 Smart Selection**: Quick select all, clear selection, and individual toggles

## 📸 Interface Preview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ✨ Linux App Installer ✨                        │
│    Select applications to install | Package Manager: apt            │
├─────────────────────────────────────────────────────────────────────┤
│ ━━━ Development ━━━                                                 │
│   ☐ git - Distributed version control system                       │
│   ☐ vim - Advanced text editor                                     │
│   ☐ neovim - Hyperextensible Vim-based text editor                 │
│   ☐ VSCode - Visual Studio Code editor                             │
│                                                                      │
│ ━━━ Multimedia ━━━                                                  │
│   ☐ VLC - Versatile media player                                   │
│   ☐ GIMP - Image manipulation program                              │
│   ☐ Blender - 3D creation suite                                    │
│                                                                      │
│  [Select All]  [Clear Selection]  [Install Selected]  [Quit]       │
└─────────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.7+**
- **pip3** (Python package installer)
- **Linux** (Ubuntu, Debian, Fedora, Arch, or derivatives)
- **sudo privileges** (for installing packages)

### Installation

1. **Clone or download the files:**
   ```bash
   git clone <your-repo-url>
   cd util
   ```

2. **Run the installation script:**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

   Or install dependencies manually:
   ```bash
   pip3 install --user textual rich
   ```

3. **Make the app executable:**
   ```bash
   chmod +x app_installer.py
   ```

### Usage

**Run the application:**
```bash
./app_installer.py
```

Or:
```bash
python3 app_installer.py
```

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `↑` `↓` | Navigate through apps |
| `Space` | Toggle app selection |
| `Enter` | Activate focused button |
| `a` | Select all apps |
| `n` | Clear all selections |
| `i` | Install selected apps |
| `q` | Quit application |
| `Tab` | Move between elements |

## 📦 Application Categories

### 🛠️ Development
- Git, Vim, Neovim, VSCode
- Python3, Node.js, Docker
- Build Essential, GCC, Make

### 🎬 Multimedia
- VLC, GIMP, Inkscape
- Audacity, OBS Studio, Blender
- Kdenlive, FFmpeg

### 🌐 Internet & Communication
- Firefox, Chromium
- Thunderbird, Telegram, Discord
- FileZilla, qBittorrent
- Curl, Wget

### ⚙️ System Tools
- htop, ncdu, tmux, screen
- GParted, Synaptic
- Bleachbit, Timeshift, KeePassXC

### 📝 Productivity
- LibreOffice, Okular, Evince
- Calibre, Joplin, Obsidian

### 🎮 Gaming
- Steam, Lutris
- Wine, GameMode

## 🔧 Configuration

### Enabling Real Installation Mode

**By default, the app runs in DRY RUN mode** (safe testing mode). To enable actual installations:

1. Open `app_installer.py`
2. Find line ~203: `DRY_RUN_MODE = True`
3. Change it to: `DRY_RUN_MODE = False`
4. Save and run the app

**What happens when you install apps:**

✅ **Fully Automated Process:**
- You select apps → Click "Install Selected"
- App automatically runs: `sudo apt install -y <package-name>`
- The `-y` flag **auto-accepts all prompts**
- **Dependencies are automatically downloaded** by your package manager
- No manual intervention needed!

**Example for installing Git:**
```bash
# The app runs this command automatically:
sudo apt install -y git

# This auto-downloads:
# - git (main package)
# - git-man (documentation)
# - liberror-perl (dependency)
# - git-core (dependency)
# ... and all other required dependencies
```

**Package Manager Details:**
- **apt** (Ubuntu/Debian): Uses `apt install -y` → auto-handles dependencies
- **dnf** (Fedora): Uses `dnf install -y` → auto-handles dependencies  
- **pacman** (Arch): Uses `pacman -S --noconfirm` → auto-handles dependencies

All package managers **automatically resolve and install dependencies** without any user input!

### Adding More Applications

Edit `app_installer.py` and modify the `AppData.APPS` dictionary:

```python
class AppData:
    APPS = {
        "Your Category": [
            {
                "name": "App Name",
                "desc": "Short description",
                "pkg": "package-name"
            },
            # Add more apps...
        ],
    }
```

### Customizing Colors

The app uses Textual's theming system. Modify the `CSS` section in the `AppInstallerApp` class to customize colors and styles.

## 🔒 Safety Features

- **Dry-run mode by default**: Shows commands without executing (change `DRY_RUN_MODE = False` to enable)
- **Sudo prompt**: System asks for password when needed (one-time per session)
- **Error handling**: Graceful handling of failed installations with error messages
- **Package verification**: Checks package manager availability before proceeding
- **Automatic dependency resolution**: Package managers handle all dependencies automatically

### Mode Indicator

The app shows current mode in the title bar:
- **DRY RUN** (Yellow) - Safe testing mode, no actual installations
- **LIVE** (Green) - Real installation mode, packages will be installed

## 🐛 Troubleshooting

**"Package manager not detected"**
- Ensure you're running on a Linux system with apt, dnf, or pacman
- The app auto-detects your package manager

**"Permission denied"**
- Make sure you have sudo privileges
- Run: `sudo -v` to verify

**"Module not found: textual"**
- Install dependencies: `pip3 install --user textual rich`
- Or run: `./install.sh`

## 🤝 Contributing

Feel free to:
- Add more applications to the database
- Improve the UI/UX
- Add support for more package managers (yum, zypper, etc.)
- Enhance error handling
- Create custom themes

## 📝 License

This project is open source and available for personal and educational use.

## 🎨 Design Philosophy

This tool was created with a focus on:
- **Aesthetic beauty**: Inspired by modern CLI tools like Gemini CLI
- **User experience**: Intuitive navigation and clear visual feedback
- **Efficiency**: Quick batch installations without repetitive commands
- **Accessibility**: Works in any terminal with rich color support

## 💡 Tips

1. **First-time users**: Start by installing just a few apps to test
2. **Power users**: Use keyboard shortcuts for faster navigation
3. **Customization**: Fork and modify the app database for your needs
4. **Automation**: Can be extended to read from JSON/YAML config files

---

**Made with ❤️ for the Linux community**

*Bringing beauty and efficiency to package management*
