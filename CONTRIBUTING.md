# Qtcord Contributor Agreement and Guidelines

By contributing to this repository, you agree that I (mak448a) have the rights to use the code contributed to this repository however I want, under any license.
If you disagree with this, you can ask for me to make this a little less ridiculous.
DISCLAIMER: I am just doing this in case if I have to copy and paste from this repository.

## Reverse Engineering
I highly recommend [this tutorial](https://www.youtube.com/watch?v=xh28F6f-Cds) for getting started with reverse engineering the Discord API.
More notes are in `projects_notes.txt`.
For API testing on Linux, I recommend [this app.](https://github.com/CleoMenezesJr/escambo)
If you're on Windows, just stick with Python requests.

## Coding Guidelines
Try to follow PEP-8 (the squiggly underlines in Pycharm) standards. If you can't, that's perfectly fine.
You can use a code formatter called Ruff if needed.

To edit the user interface, use QT designer and put the UI files under `src/ui`. To apply the UI, run `src/regenerate.py`.
