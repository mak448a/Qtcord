# Qtcord Contributor Agreement and Guidelines

By contributing to this repository, you agree that I (mak448a) have the rights to use the code contributed to this repository however I want, under any license.
If you disagree with this, you can ask for me to make this a little less ridiculous.
DISCLAIMER: I am just doing this in case if I have to copy and paste from this repository or relicense the code.

## Discord API Usage
Try [this tutorial](https://www.youtube.com/watch?v=xh28F6f-Cds) for getting started with the Discord API.
More notes are in `projects_notes.txt`.
For API testing on Linux, I recommend [this app.](https://github.com/CleoMenezesJr/escambo)
If you're on Windows, just stick with Python requests.
You can use following resources for API docs.

- https://discord.com/developers/docs/
- https://luna.gitlab.io/discord-unofficial-docs/
- https://www.youtube.com/channel/UC8PPJFudLUM1eJlM4BiJ40A

## Coding Guidelines
I prefer no LLM-generated code, but if you use AI, review the code it outputs for mistakes. Clean the code if needed, and remove the unnecessary comments.

Try to follow PEP-8 (the squiggly underlines in Pycharm) standards. If you can't, that's perfectly fine.

If possible, use Ruff to format your code.

If you add a dependency, make sure to add it to `requirements.txt` and `no_pyside_requirements.txt`.
Don't forget to add the appropriate license to the licenses folder and UI!

To edit the user interface, use Qt designer and put the UI files under `src/ui`. To apply the UI, run `src/regenerate.py`.

GitHub actions will build and release automatically when a tag is created.

## Packaging
Build scripts are in `helper_scripts/` and `.github/`.

- If you want to package for Linux, take a look at `linux.spec`, `ci.yml`, and [Qtcord's Flathub manifest](https://github.com/flathub/io.github.mak448a.QTCord).
- If you want to package for Windows, run package_windows.py.
- If you want to package for macOS, run package_macos.py.
