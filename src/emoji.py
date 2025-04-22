import json
import os
import re
from discord_integration import get_user_from_id  # Ensure this module is accessible

# Load emoji.json file dynamically
EMOJI_FILE = os.path.join(os.path.dirname(__file__), "emoji.json")

with open(EMOJI_FILE, "r", encoding="utf-8") as file:
    EMOJI_MAP = json.load(file)

def convert_discord_emojis(content):
    """
    Converts Discord emoji shortcodes like :smile: into Unicode emojis.
    """
    def replace_match(match):
        emoji_name = match.group(1)
        return EMOJI_MAP.get(emoji_name, match.group(0))  # Replace if found, else keep original text

    return re.sub(r":([a-zA-Z0-9_+-]+):", replace_match, content)

def process_message_content(content):
    """
    Process Discord message content:
    - Convert user mentions (<@123456789>) into formatted names.
    - Convert emoji shortcodes into their Unicode equivalents.
    """
    # Convert mentions
    if "<@" in content:
        matches = re.findall(r"<@(\d+)>", content)
        for id_mentioned in matches:
            user = get_user_from_id(id_mentioned)
            if user:
                content = re.sub(
                    f"<@{id_mentioned}>",
                    f"<em>@{user.get_user_name()}</em>",
                    content,
                )

    # Convert emojis
    content = convert_discord_emojis(content)

    return content

