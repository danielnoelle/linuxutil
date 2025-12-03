#!/usr/bin/env python3
"""
Linux App Installer - A beautiful TUI for installing applications by category
Supports apt, dnf, pacman package managers
"""

import subprocess
import sys
from typing import Dict, List, Set
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.widgets import (
    Header,
    Footer,
    Button,
    Checkbox,
    Static,
    Label,
    ProgressBar,
    RichLog,
)
from textual.binding import Binding
from textual.screen import Screen
from rich.text import Text
from rich.panel import Panel
from rich.align import Align


class AppData:
    """Database of applications organized by category"""
    
    APPS = {
        "Development": [
            {"name": "git", "desc": "Distributed version control system", "pkg": "git"},
            {"name": "vim", "desc": "Advanced text editor", "pkg": "vim"},
            {"name": "neovim", "desc": "Hyperextensible Vim-based text editor", "pkg": "neovim"},
            {"name": "VSCode", "desc": "Visual Studio Code editor", "pkg": "code"},
            {"name": "Python3", "desc": "Python programming language", "pkg": "python3"},
            {"name": "Node.js", "desc": "JavaScript runtime", "pkg": "nodejs"},
            {"name": "Docker", "desc": "Container platform", "pkg": "docker.io"},
            {"name": "Build Essential", "desc": "Compilers and build tools", "pkg": "build-essential"},
            {"name": "GCC", "desc": "GNU Compiler Collection", "pkg": "gcc"},
            {"name": "Make", "desc": "Build automation tool", "pkg": "make"},
        ],
        "Multimedia": [
            {"name": "VLC", "desc": "Versatile media player", "pkg": "vlc"},
            {"name": "GIMP", "desc": "Image manipulation program", "pkg": "gimp"},
            {"name": "Inkscape", "desc": "Vector graphics editor", "pkg": "inkscape"},
            {"name": "Audacity", "desc": "Audio editor and recorder", "pkg": "audacity"},
            {"name": "OBS Studio", "desc": "Video recording and streaming", "pkg": "obs-studio"},
            {"name": "Blender", "desc": "3D creation suite", "pkg": "blender"},
            {"name": "Kdenlive", "desc": "Video editing suite", "pkg": "kdenlive"},
            {"name": "FFmpeg", "desc": "Multimedia framework", "pkg": "ffmpeg"},
        ],
        "Internet & Communication": [
            {"name": "Firefox", "desc": "Web browser", "pkg": "firefox"},
            {"name": "Chromium", "desc": "Open-source web browser", "pkg": "chromium-browser"},
            {"name": "Thunderbird", "desc": "Email client", "pkg": "thunderbird"},
            {"name": "Telegram", "desc": "Cloud-based messaging app", "pkg": "telegram-desktop"},
            {"name": "Discord", "desc": "Voice and text chat platform", "pkg": "discord"},
            {"name": "FileZilla", "desc": "FTP client", "pkg": "filezilla"},
            {"name": "qBittorrent", "desc": "BitTorrent client", "pkg": "qbittorrent"},
            {"name": "Curl", "desc": "Command line tool for transfers", "pkg": "curl"},
            {"name": "Wget", "desc": "Network downloader", "pkg": "wget"},
        ],
        "System Tools": [
            {"name": "htop", "desc": "Interactive process viewer", "pkg": "htop"},
            {"name": "ncdu", "desc": "Disk usage analyzer", "pkg": "ncdu"},
            {"name": "tmux", "desc": "Terminal multiplexer", "pkg": "tmux"},
            {"name": "screen", "desc": "Terminal multiplexer", "pkg": "screen"},
            {"name": "GParted", "desc": "Partition editor", "pkg": "gparted"},
            {"name": "Synaptic", "desc": "Package manager GUI", "pkg": "synaptic"},
            {"name": "Bleachbit", "desc": "System cleaner", "pkg": "bleachbit"},
            {"name": "Timeshift", "desc": "System restore utility", "pkg": "timeshift"},
            {"name": "KeePassXC", "desc": "Password manager", "pkg": "keepassxc"},
        ],
        "Productivity": [
            {"name": "LibreOffice", "desc": "Office suite", "pkg": "libreoffice"},
            {"name": "Okular", "desc": "Document viewer", "pkg": "okular"},
            {"name": "Evince", "desc": "PDF viewer", "pkg": "evince"},
            {"name": "Calibre", "desc": "E-book management", "pkg": "calibre"},
            {"name": "Notion (unofficial)", "desc": "Note-taking app", "pkg": "notion-app"},
            {"name": "Obsidian", "desc": "Knowledge base", "pkg": "obsidian"},
            {"name": "Joplin", "desc": "Note taking app", "pkg": "joplin"},
        ],
        "Gaming": [
            {"name": "Steam", "desc": "Gaming platform", "pkg": "steam"},
            {"name": "Lutris", "desc": "Gaming platform", "pkg": "lutris"},
            {"name": "Wine", "desc": "Windows compatibility layer", "pkg": "wine"},
            {"name": "GameMode", "desc": "Gaming optimizations", "pkg": "gamemode"},
        ],
    }


class AppCheckbox(Horizontal):
    """Custom checkbox widget for apps"""
    
    def __init__(self, app_info: Dict[str, str], category: str) -> None:
        super().__init__()
        self.app_info = app_info
        self.category = category
        
    def compose(self) -> ComposeResult:
        yield Checkbox(
            f"[bold cyan]{self.app_info['name']}[/] - {self.app_info['desc']}",
            id=f"app_{self.category}_{self.app_info['pkg']}"
        )


class CategorySection(Vertical):
    """Widget for displaying a category of apps"""
    
    def __init__(self, category: str, apps: List[Dict[str, str]]) -> None:
        super().__init__()
        self.category = category
        self.apps = apps
        
    def compose(self) -> ComposeResult:
        yield Label(f"[bold magenta]━━━ {self.category} ━━━[/]", classes="category-header")
        for app in self.apps:
            yield AppCheckbox(app, self.category)
        yield Label("")  # Spacer


class InstallationScreen(Screen):
    """Screen showing installation progress"""
    
    def __init__(self, selected_apps: List[Dict], pkg_manager: str, dry_run: bool = False) -> None:
        super().__init__()
        self.selected_apps = selected_apps
        self.pkg_manager = pkg_manager
        self.dry_run = dry_run
        
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("[bold cyan]Installing Applications[/]", id="install-title"),
            RichLog(id="install-log", highlight=True, markup=True),
            Button("Close", variant="primary", id="close-btn"),
            id="install-container"
        )
        yield Footer()
        
    def on_mount(self) -> None:
        """Start installation when screen mounts"""
        self.install_apps()
        
    async def install_apps(self) -> None:
        """Install selected applications"""
        log = self.query_one("#install-log", RichLog)
        
        mode_text = "[bold yellow]DRY RUN MODE[/]" if self.dry_run else "[bold green]INSTALLATION MODE[/]"
        log.write(Panel(
            f"{mode_text}\nStarting installation of {len(self.selected_apps)} application(s)",
            border_style="yellow" if self.dry_run else "green"
        ))
        
        if self.dry_run:
            log.write("[dim]Note: Running in dry-run mode. No actual installations will occur.[/]\n")
        
        for i, app in enumerate(self.selected_apps, 1):
            log.write(f"\n[bold yellow]({i}/{len(self.selected_apps)})[/] Installing [bold cyan]{app['name']}[/]...")
            
            try:
                # Build install command based on package manager
                if self.pkg_manager == "apt":
                    cmd = ["sudo", "apt", "install", "-y", app["pkg"]]
                elif self.pkg_manager == "dnf":
                    cmd = ["sudo", "dnf", "install", "-y", app["pkg"]]
                elif self.pkg_manager == "pacman":
                    cmd = ["sudo", "pacman", "-S", "--noconfirm", app["pkg"]]
                else:
                    log.write(f"[bold red]✗[/] Unknown package manager")
                    continue
                
                log.write(f"  [dim]Command: {' '.join(cmd)}[/]")
                
                if self.dry_run:
                    # Dry run mode - just show what would happen
                    log.write(f"[bold cyan]ℹ[/] Would execute command (dry-run mode)")
                    log.write(f"[dim]  → Dependencies would be auto-downloaded by {self.pkg_manager}[/]")
                else:
                    # ACTUAL INSTALLATION - automatically handles dependencies
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    if result.returncode == 0:
                        log.write(f"[bold green]✓[/] {app['name']} installed successfully")
                        log.write(f"[dim]  → All dependencies automatically installed[/]")
                    else:
                        log.write(f"[bold red]✗[/] Failed to install {app['name']}")
                        if result.stderr:
                            log.write(f"[dim red]{result.stderr[:200]}[/]")
                
            except Exception as e:
                log.write(f"[bold red]✗[/] Error: {str(e)}")
        
        log.write(Panel(
            "[bold green]Installation process completed![/]",
            border_style="green"
        ))
        
class AppInstallerApp(App):
    """Main application class"""
    
    # Set to False to enable REAL installations (will actually install packages)
    # Set to True for dry-run mode (just shows what would be installed)
    DRY_RUN_MODE = True
    
    CSS = """elf.app.pop_screen()


class AppInstallerApp(App):
    """Main application class"""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    Header {
        background: $primary;
        color: $text;
        text-style: bold;
    }
    
    Footer {
        background: $panel;
    }
    
    #main-container {
        height: 100%;
        padding: 1;
    }
    
    #title-container {
        height: auto;
        padding: 1;
        background: $primary-darken-1;
        border: heavy $primary;
        margin-bottom: 1;
    }
    
    #title {
        text-align: center;
        text-style: bold;
        color: $accent;
    }
    
    #subtitle {
        text-align: center;
        color: $text-muted;
        margin-top: 1;
    }
    
    #app-scroll {
        height: 1fr;
        border: solid $primary;
        background: $surface-darken-1;
        padding: 1;
        margin-bottom: 1;
    }
    
    .category-header {
        text-style: bold;
        margin-top: 1;
        margin-bottom: 1;
    }
    
    #button-container {
        height: auto;
        align: center middle;
    }
    
    Button {
        margin: 1 2;
    }
    
    Checkbox {
        margin: 0 2;
        padding: 0 1;
    }
    
    Checkbox:hover {
        background: $primary-darken-2;
    }
    
    #install-container {
        padding: 2;
        height: 100%;
    }
    
    #install-title {
        text-align: center;
        text-style: bold;
        padding: 1;
        margin-bottom: 1;
    }
    
    #install-log {
        height: 1fr;
        border: solid $primary;
        margin-bottom: 1;
    }
    
    #close-btn {
        width: 20;
        align: center middle;
    }
    """
    
    TITLE = "Linux App Installer"
    SUB_TITLE = "Beautiful package management made easy"
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("i", "install", "Install Selected"),
        Binding("a", "select_all", "Select All"),
        Binding("n", "select_none", "Clear Selection"),
    ]
    
    def __init__(self):
        super().__init__()
        self.pkg_manager = self.detect_package_manager()
        
    def compose(self) -> ComposeResult:
            with Container(id="title-container"):
                yield Static("[bold cyan]✨ Linux App Installer ✨[/]", id="title")
                mode = "[bold yellow]DRY RUN[/]" if self.DRY_RUN_MODE else "[bold green]LIVE[/]"
                yield Static(
                    f"Select applications to install | Package Manager: [bold yellow]{self.pkg_manager}[/] | Mode: {mode}",
                    id="subtitle"
                )ield Static("[bold cyan]✨ Linux App Installer ✨[/]", id="title")
                yield Static(
                    f"Select applications to install | Package Manager: [bold yellow]{self.pkg_manager}[/]",
                    id="subtitle"
                )
            
            with VerticalScroll(id="app-scroll"):
                for category, apps in AppData.APPS.items():
                    yield CategorySection(category, apps)
            
            with Horizontal(id="button-container"):
                yield Button("Select All", variant="success", id="select-all-btn")
                yield Button("Clear Selection", variant="warning", id="clear-btn")
                yield Button("Install Selected", variant="primary", id="install-btn")
                yield Button("Quit", variant="error", id="quit-btn")
        
        yield Footer()
    
    def detect_package_manager(self) -> str:
        """Detect which package manager is available"""
        managers = {
            "apt": ["apt", "--version"],
            "dnf": ["dnf", "--version"],
            "pacman": ["pacman", "--version"],
        }
        
        for manager, cmd in managers.items():
            try:
                subprocess.run(cmd, capture_output=True, check=True)
                return manager
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        return "unknown"
    
    def get_selected_apps(self) -> List[Dict[str, str]]:
        """Get list of selected applications"""
        selected = []
        for checkbox in self.query(Checkbox):
            if checkbox.value:
                # Extract package info from checkbox id
                parts = checkbox.id.split("_")
                if len(parts) >= 3:
                    pkg_name = "_".join(parts[2:])
                    # Find the app info
                    for category, apps in AppData.APPS.items():
                        for app in apps:
                            if app["pkg"] == pkg_name:
                                selected.append(app)
                                break
        return selected
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "quit-btn":
            self.exit()
        elif event.button.id == "select-all-btn":
            self.action_select_all()
        elif event.button.id == "clear-btn":
            self.action_select_none()
        elif event.button.id == "install-btn":
            self.action_install()
    
    def action_select_all(self) -> None:
        """Select all checkboxes"""
        for checkbox in self.query(Checkbox):
            checkbox.value = True
    
    def action_select_none(self) -> None:
        """Deselect all checkboxes"""
        for checkbox in self.query(Checkbox):
            checkbox.value = False
    
    def action_install(self) -> None:
        """Install selected applications"""
        selected = self.get_selected_apps()
        
        if not selected:
            self.notify("No applications selected!", severity="warning", timeout=3)
            return
        
        if self.pkg_manager == "unknown":
            self.notify(
                "Package manager not detected! Please install apt, dnf, or pacman.",
                severity="error",
                timeout=5
            )
            return
        # Push installation screen
        self.push_screen(InstallationScreen(selected, self.pkg_manager, self.DRY_RUN_MODE))
        self.push_screen(InstallationScreen(selected, self.pkg_manager))


def main():
    """Main entry point"""
    app = AppInstallerApp()
    app.run()


if __name__ == "__main__":
    main()
