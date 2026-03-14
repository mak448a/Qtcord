# Qtcord

<div align="center">
  <img src="src/assets/icon.svg" width="128" height="128" alt="Qtcord Logo">
  <h3>A lightweight, native Discord client built with Python and Qt</h3>

  [![Flathub](https://img.shields.io/endpoint?url=https://flathub-stats-backend.vercel.app/badges/io.github.mak448a.QTCord/shields.io.json)](https://flathub.org/apps/io.github.mak448a.QTCord)
  [![Discord Invite](https://img.shields.io/badge/Discord-Join%20Server-7289da?logo=discord&logoColor=white)](https://discord.gg/gV8SjzZAXj)
  [![CI Build & Release](https://github.com/mak448a/Qtcord/actions/workflows/ci.yml/badge.svg)](https://github.com/mak448a/Qtcord/actions/workflows/ci.yml)
</div>

---

Qtcord aims to provide a native, high-performance experience for Discord without the overhead of a full web browser shell. 

> [!CAUTION]
> **Use at your own risk.** This is a fun side project. Using unofficial clients is technically against Discord's Terms of Service and *can* lead to your account being banned. I do not endorse or take responsibility for any account actions.

---

![Screenshot of Qtcord](demos/demo4.png)

## Features
- **Native & Lightweight**: Built with PySide6 (Qt) for a snappy interface.
- **Secure by Design**: Uses your system's secure credential store (GNOME Keyring, KWallet, or macOS Keychain) to store tokens.
- **Cross-Platform**: Works on Windows, macOS, and Linux.
- **Privacy Focused**: No tracking, no telemetry, no bloat.

## Getting Started

### For Users
The easiest way to get Qtcord is through our official builds:

- **Linux**: Get it on [Flathub](https://flathub.org/apps/io.github.mak448a.QTCord) or download the binary from [Releases](https://github.com/mak448a/Qtcord/releases/latest).
- **Windows & macOS**: Download the latest installer/bundle from our [GitHub Releases](https://github.com/mak448a/Qtcord/releases/latest).

### For Developers
If you want to run the source code or contribute:

1. **Requirements**: Python 3.12 or higher.
2. **Setup**:
   ```bash
   # Clone the repo
   git clone https://github.com/mak448a/Qtcord.git
   cd Qtcord

   # Create a virtual environment
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies (uv is recommended for speed!)
   pip install -r requirements.txt
   ```
3. **Run**:
   ```bash
   cd src
   python3 main.py
   ```

## Development
Check out [CONTRIBUTING.md](CONTRIBUTING.md) for our coding guidelines and release instructions. 

- We use **Ruff** for linting and formatting. 
- Build scripts for all platforms are located in `helper_scripts/`.
- Automated CI/CD handles builds and releases on every tag.

## Credits & Documentation
- [Official Discord API Documentation](https://discord.com/developers/docs/)
- [Unofficial Discord Documentation](https://luna.gitlab.io/discord-unofficial-docs/)
- Special thanks to the community for tutorials and feedback.

---
<div align="center">
  (Make sure you're getting Qtcord from the right source! The official source is <a href="https://github.com/mak448a/Qtcord">github.com/mak448a/Qtcord</a>)
</div>
