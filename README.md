# Qtcord

<img src="src/assets/icon.svg" width="64" height="64" alt="Qtcord Logo">
<h3>A lightweight, native Discord client built with Python and Qt</h3>

[![Flathub](https://img.shields.io/endpoint?url=https://flathub-stats-backend.vercel.app/badges/io.github.mak448a.QTCord/shields.io.json)](https://flathub.org/apps/io.github.mak448a.QTCord)
[![Discord Invite](https://img.shields.io/badge/Discord-Join%20Server-7289da?logo=discord&logoColor=white)](https://discord.gg/gV8SjzZAXj)
[![CI Build & Release](https://github.com/mak448a/Qtcord/actions/workflows/ci.yml/badge.svg)](https://github.com/mak448a/Qtcord/actions/workflows/ci.yml)

---

Qtcord aims to provide a native, high-performance experience for Discord without Electron. 

> [!CAUTION]
> **Use at your own risk.** This is a fun side project. Using unofficial clients is technically against Discord's Terms of Service and *can* lead to your account being banned. I do not endorse or take responsibility for any account actions.

(Make sure you're getting Qtcord from the right source! The official source is [mak448a/Qtcord](https://github.com/mak448a/Qtcord)!)

---

![Screenshot of Qtcord](demos/demo4.png)

## Features
- **Lightweight & Native**: Built with PySide6 (Qt) for a snappy interface.
- **Cross-Platform**: Works on Windows, macOS, and Linux.
- **Privacy Focused**: Runs without telemetry, tracking, or bloat.
- **Work in progress**: Supports servers, direct messages, channels, profile pictures, and server icons.

## Installation
The easiest way to get Qtcord is through the official builds:

- **Linux**: Get it on [Flathub](https://flathub.org/apps/io.github.mak448a.QTCord) or download the binary from [Releases](https://github.com/mak448a/Qtcord/releases/latest).
- **Windows & macOS**: Download the latest installer/bundle from [GitHub Releases](https://github.com/mak448a/Qtcord/releases/latest).


## Development
Check out [CONTRIBUTING.md](CONTRIBUTING.md) for our coding guidelines and release instructions. 
Check out [CONTRIBUTING.md](https://github.com/mak448a/Qtcord/blob/main/CONTRIBUTING.md)!
> [!NOTE]
> You need Python 3.12 or higher!
> Also, I recommend using uv if you have it installed. It's faster than pip. (`uv pip install -r requirements.txt`)

Do the standard Python procedure:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Afterwards, just run main.py. If you're on Windows, substitute `python3` for `python`.
```shell
python3 src/main.py
```

## Credits & Documentation
- [Official Discord API Documentation](https://discord.com/developers/docs/)
- [Unofficial Discord Documentation](https://luna.gitlab.io/discord-unofficial-docs/)
- Special thanks to the community for tutorials and feedback.
