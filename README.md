# QTCord
QTCord is a lightweight Discord client aiming to bring a native look and feel chat experience. I am not responsible if you get your account banned from this project.

<a href='https://flathub.org/apps/io.github.mak448a.QTCord'>
  <img width='150' alt='Download on Flathub' src='https://dl.flathub.org/assets/badges/flathub-badge-en.png'/>
</a>

Join our Discord:<br>
[![Discord Invite](https://dcbadge.limes.pink/api/server/https://discord.gg/e4UxaEEYdu?style=flat)](https://discord.gg/e4UxaEEYdu)

[Download for Windows](https://github.com/mak448a/QTCord/releases)
<br>

![Screenshot of QTCord](demo1.png)

## Setup

Do the standard Python procedure:
`python3 -m venv venv`
`source venv/bin/activate`
`pip install -r requirements.txt`

Cd into src
`cd src/`

Afterwards, just run main.py.
```shell
python3 main.py
```

## Notes for developers
The code is a mess, since I'm just working on this for fun. Have fun! And if you're feeling very helpful, maybe even clean it up for me! 😅

When you need to regenerate the ui files, create the file `~/Documents/regenerate_ui_files_indicator.txt`.
More notes are in `projects_notes.txt`.
