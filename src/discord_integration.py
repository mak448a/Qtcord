import requests
import platformdirs
import os
from datetime import datetime


api_base = "https://discord.com/api/v9"
auth = ""  # Will be overridden when load_token is called
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.63 Chrome/124.0.6367.243 Electron/30.2.0 Safari/537.36"
}


def load_token() -> None:
    """
    Loads the token from discordauth.txt.
    """

    global auth, headers

    if os.path.isfile(platformdirs.user_config_dir("Qtcord") + "/discordauth.txt"):
        with open(platformdirs.user_config_dir("Qtcord") + "/discordauth.txt") as f:
            auth = f.read()
        headers["authorization"] = auth.strip()


def validate_token() -> bool:
    """
    Checks whether the token is valid or not.

    Returns:
        bool: True if the token is valid, False otherwise.
    """

    try:
        r = requests.get(f"{api_base}/users/@me/relationships", headers=headers)
    except requests.exceptions.ConnectionError:
        # Just assume that the token is valid, since there's no internet or Discord is down.
        return True

    # It's valid
    if r.status_code == 200:
        return True
    # 401 means "unauthorized," which means it's invalid.
    elif r.status_code == 401:
        return False
    # This shouldn't happen, but it's here anyway for safety.
    else:
        return False


# Load token
load_token()

# If token is invalid, delete it and log us out.
# Inside validate_token is a function that checks for internet, too.
if not validate_token():
    # If there is a token and it's invalid
    if os.path.exists(platformdirs.user_config_dir("Qtcord") + "/discordauth.txt"):
        print("TOKEN INVALID")
        os.remove(platformdirs.user_config_dir("Qtcord") + "/discordauth.txt")


def get_messages(channel_id: int, limit: int = 100) -> list:
    """
    Retrives messages from a specified channel.

    Args:
        channel_id (int): The channel ID to request from
        limit (int, optional): The maximum messages to request. Default is 100. May not go higher.

    Returns:
        list: The messages from the channel.
    """

    r = requests.get(
        f"{api_base}/channels/{channel_id}/messages?limit={limit}", headers=headers
    )

    new_list = []

    if r.status_code != 200:
        new_list.append(
            {
                "timestamp": datetime.now(),
                "username": "System",
                "content": "Error. This may be a forum channel, or you're not allowed to view the content.",
                "id": 0,
            }
        )
        return new_list

    for message in r.json():
        # TODO: You can get the author's profile picture ID from message["avatar"].
        # TODO: Then, https://cdn.discordapp.com/avatars/user_id/avatar_id.webp?size={size} (size can equal 64, 128, 256, etc.)
        # TODO: Make sure to add error handling for no profile picture.
        if not message["author"].get("global_name", False):
            author = message["author"]["username"]
        else:
            author = message["author"]["global_name"]

        if not message["content"]:
            content = "[(call/image/other)]"
        else:
            content = message["content"]

        # Code for displaying timestamps
        # For some reason, messages can use two, slightly different, timestamp formats.
        time_str = message["timestamp"]
        if len(time_str) == 32:
            timestamp = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%f%z")
        else:
            timestamp = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S%z")

        new_list.append(
            {
                "timestamp": timestamp.astimezone(),
                "username": author,
                "content": content,
                "id": message["id"],
            }
        )

    # Reverse the list of messages
    new_list.reverse()
    return new_list


def send_message(msg, channel) -> None:
    """
    Sends a message to a given channel.

    Args:
        msg (str): The message to send.
        channel (int): The channel to send the message in.

    Returns:
        None: No return value is needed.
    """

    requests.post(
        f"{api_base}/channels/{channel}/messages",
        headers=headers,
        json={"content": msg},
    )


def get_friends() -> dict:
    """
    Returns a list of friends for the current account.

    Returns:
        dict: The friends of the current account.
    """

    r = requests.get(f"{api_base}/users/@me/relationships", headers=headers)

    # for friend in r.json():
    #     print(friend["user"]["global_name"])

    return r.json()


def get_channel_from_id(user_id: int) -> int:
    """
    Converts a user ID into a channel ID.

    Args:
        user_id (int): The user's ID.

    Returns:
        int: The user's channel from which they can be reached.
    """

    r = requests.post(
        f"{api_base}/users/@me/channels",
        headers=headers,
        json={"recipient_id": user_id},
    )
    return r.json()["id"]


def get_guilds() -> dict:
    """
    Returns all guilds (aka servers) that the current user is in. Also downloads the icons of the servers.

    Returns:
        dict: Guilds that the current account is in.
    """

    r = requests.get(f"{api_base}/users/@me/guilds", headers=headers)

    # TODO: You can get the icon of the server by: https://cdn.discordapp.com/icons/{id}/{icon_name}.
    # Icon name and id is in the icon.
    # Make sure to handle blank icons!!!! they are set to none
    # You get the rest of the info from this function.
    for server in r.json():
        if os.path.exists(
            f"{platformdirs.user_cache_dir('Qtcord')}/servers/{server['id']}.png"
        ):
            continue

        # print(f"https://cdn.discordapp.com/icons/{server['id']}/{server['icon']}")
        server_icon = requests.get(
            f"https://cdn.discordapp.com/icons/{server['id']}/{server['icon']}"
        )

        # Handle no image servers
        if server_icon.status_code == 404:
            continue

        if not os.path.exists(f"{platformdirs.user_cache_dir('Qtcord')}/servers"):
            os.makedirs(f"{platformdirs.user_cache_dir('Qtcord')}/servers")

        with open(
            f"{platformdirs.user_cache_dir('Qtcord')}/servers/{server['id']}.png", "wb"
        ) as f:
            for chunk in server_icon.iter_content():
                f.write(chunk)

    # print(f"https://cdn.discordapp.com/icons/{r.json()[1]["id"]}/{r.json()[1]["icon"]}")
    return r.json()


def get_guild_channels(guild_id: int) -> dict:
    """
    Returns all channels in a guild.

    Args:
        guild_id (int): Any guild that the current user is in.

    Returns:
        dict: The channels in the guild.
    """

    r = requests.get(f"{api_base}/guilds/{guild_id}/channels", headers=headers)

    return r.json()


def login(email: str, password: str, totp_code: str = ""):
    """
    Takes in an email and a password, logs in, and spits out a token.

    Args:
        email (str): Your email, e.g., example@example.com
        password (str): Your password for that account.

    Returns:
        str: Your token.
    """
    payload = {
        "login": email,
        "password": password,
        "undelete": False,
        "login_source": None,
        "gift_code_sku_id": None,
    }

    r = requests.post(f"{api_base}/auth/login", json=payload)

    # Check for errors
    if r.json().get("errors", False):
        return None

    # Return token if it succeeds, otherwise, return nothing.
    if r.json().get("token", False):
        return r.json()["token"]
    else:
        # If we have 2fa with totp
        if r.json().get("totp", False):
            totp_payload = {"ticket": r.json()["ticket"], "code": totp_code}

            res = requests.post(f"{api_base}/auth/mfa/totp", json=totp_payload)

            if res.status_code == 400:
                # If authentication was a failure
                return None
            else:
                # Else, we have our token!
                return res.json()["token"]
        else:
            print(
                "Error. You probably entered in your credentials wrong.\n"
                + "Or maybe you have SMS 2FA? SMS 2FA is not supported currently.\n"
                + "Ask for it at https://github.com/mak448a/Qtcord/issues"
            )
            return None


def send_typing(channel: int):
    """
    Sends a typing indicator to a channel.

    Args:
        channel (int): The discord channel to send the typing indicator to

    Returns:
        None
    """

    requests.post(f"{api_base}/channels/{channel}/typing", headers=headers)
