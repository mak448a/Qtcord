import re
from discord_integration import get_user_from_id  # Ensure this module is accessible

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

def convert_discord_emojis(content):
    """
    Converts Discord emoji shortcodes like :smile: into Unicode emojis.
    """
    emoji_dict = {
        "smile": "😄",
        "heart": "❤️",
        "thumbsup": "👍",
        "fire": "🔥",
        "100": "💯",
        "clap": "👏",
        "thinking": "🤔",
        "laugh": "😂",
        "cry": "😢",
        "grin": "😁",
        "angry": "😠",
        "surprised": "😲",
        "cool": "😎",
        "sweat": "😅",
        "joy": "🤣",
        "sad": "😞",
        "wink": "😉",
        "star": "⭐",
        "check": "✔️",
        "cross": "❌",
        "question": "❓",
        "exclamation": "❗",
        "wave": "👋",
        "pray": "🙏",
        "ok": "👌",
        "eyes": "👀",
        "rocket": "🚀",
        "tada": "🎉",
        "party": "🥳",
        "gift": "🎁",
        "facepalm": "🤦",
        "shrug": "🤷",
        "skull": "💀",
        "poop": "💩",
        "robot": "🤖",
        "alien": "👽",
        "ghost": "👻",
        "money": "🤑",
        "zany": "🤪",
        "nerd": "🤓",
        "smirk": "😏",
        "hug": "🤗",
        "love": "😍",
        "sleepy": "😴",
        "yawn": "🥱",
        "pensive": "😔",
        "confused": "😕",
        "neutral": "😐",
        "zipper": "🤐",
        "nauseated": "🤢",
        "mask": "😷",
        "scream": "😱",
        "dizzy": "😵",
        "relieved": "😌",
        "halo": "😇",
        "devil": "😈",
        "clown": "🤡",
        "muscle": "💪",
        "coffee": "☕",
        "pizza": "🍕",
        "cake": "🍰",
        "chocolate": "🍫",
        "apple": "🍎",
        "banana": "🍌",
        "carrot": "🥕",
        "burger": "🍔",
        "fries": "🍟",
        "hotdog": "🌭",
        "beers": "🍻",
        "wine": "🍷",
        "cheers": "🥂",
        "soccer": "⚽",
        "basketball": "🏀",
        "football": "🏈",
        "tennis": "🎾",
        "bowling": "🎳",
        "bike": "🚴",
        "train": "🚆",
        "car": "🚗",
        "airplane": "✈️",
        "globe": "🌍",
        "sun": "☀️",
        "moon": "🌙",
        "rainbow": "🌈",
        "snowflake": "❄️",
        "fireworks": "🎆",
        "medal": "🏅",
        "trophy": "🏆",
        "flag": "🚩",
        "hourglass": "⌛",
        "lightbulb": "💡",
        "bell": "🔔",
        "megaphone": "📣",
        "bomb": "💣",
        "moneybag": "💰",
        "credit": "💳",
        "email": "✉️",
        "link": "🔗",
        "pen": "🖊️",
        "book": "📖",
        "radio": "📻",
        "tv": "📺",
        "camera": "📷",
        "video": "🎥",
        "headphones": "🎧",
        "cd": "💿",
        "key": "🔑",
        "lock": "🔒",
        "unlock": "🔓",
        "clipboard": "📋",
        "paperclip": "📎",
        "bar_chart": "📊",
        "notepad": "🗒️",
        "newspaper": "📰",
        "calendar": "📅",
        "hourglass_done": "⏳",
    }

    for shortcode, emoji_unicode in emoji_dict.items():
        content = content.replace(f":{shortcode}:", emoji_unicode)

    return content

