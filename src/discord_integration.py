import requests
import platformdirs
import os
import keyring # Added for secure token storage
from datetime import datetime
from discord_objects import (
    DiscordUser,
    DiscordMessage,
    DiscordFriend,
    DiscordChannel,
    DiscordGuild,
    users_cache_data,
)
from discord_exceptions import ChannelAccessError, InvalidResponseError


api_base = "https://discord.com/api/v9"
auth = ""  # Will be overridden when load_token is called
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.63 Chrome/124.0.6367.243 Electron/30.2.0 Safari/537.36"
}


def load_token() -> None:
    """
    SECURITY UPDATE: Loads the token from system keyring (primary) 
    or discordauth.txt (legacy fallback).
    """

    global auth, headers

    # First, try to get the token from the OS secure storage
    secure_token = keyring.get_password("Qtcord", "discord_token")
    
    if secure_token:
        auth = secure_token
    else:
        # Fallback to the old plaintext file if keyring is empty
        auth_path = os.path.join(platformdirs.user_config_dir("Qtcord"), "discordauth.txt")
        if os.path.isfile(auth_path):
            with open(auth_path) as f:
                auth = f.read().strip()
    
    if auth:
        headers["authorization"] = auth


def validate_token() -> bool:
    """
    Checks for a valid token.

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

# If token is invalid, delete it from all storage locations to force re-login.
if not validate_token():
    auth_path = os.path.join(platformdirs.user_config_dir("Qtcord"), "discordauth.txt")
    if os.path.exists(auth_path) or keyring.get_password("Qtcord", "discord_token"):
        print("TOKEN INVALID - Clearing storage")
        
        # Remove legacy file
        if os.path.exists(auth_path):
            os.remove(auth_path)
            
        # Remove from keyring
        try:
            keyring.delete_password("Qtcord", "discord_token")
        except keyring.errors.PasswordDeleteError:
            pass


def get_messages(channel_id: int, limit: int = 100) -> dict[int, list]:
    """
    Retrives messages from the specified channel.

    Args:
        channel_id (int): A channel ID.
        limit (int, optional): The maximum messages to request. Default is 100. May not go higher.

    Returns:
        dict[int, DiscordMessage]: A dictionary with the channel ID as only key, and a list with
          the channel's messages as its value.
    """
    # TODO: Add the ability to get messages before a message, like
    # https://discord.com/api/v9/channels/%7Bchannel_id%7D/messages?before={message}&limit={message_limit}

    r = requests.get(
        f"{api_base}/channels/{channel_id}/messages?limit={limit}", headers=headers
    )

    messages_list = []

    if r.status_code != 200:
        messages_list.append(
            DiscordMessage(
                id=0,
                author=DiscordUser(0, "", "", "System"),
                content="Error. This may be a forum channel, or you're not allowed to view the content.",
                # attachments=[],
                timestamp=datetime.utcfromtimestamp(0),
                # referenced_message=None,
            )
        )
        return {channel_id: messages_list}

    for message in r.json():
        messages_list.append(DiscordMessage.from_dict(message))

    # Reverse the list of messages
    messages_list.reverse()
    return {channel_id: messages_list}


def send_message(msg, channel) -> None:
    """
    Sends a message to the specified channel.

    Args:
        msg (str): The message to send.
        channel (int): The channel to which send the message.

    Returns:
        None
    """

    requests.post(
        f"{api_base}/channels/{channel}/messages",
        headers=headers,
        json={"content": msg},
    )


def get_friends() -> list[DiscordFriend]:
    """
    Returns the current user's friends.

    Returns:
        list: The current user's friends.
    """

    r = requests.get(f"{api_base}/users/@me/relationships", headers=headers)

    return [DiscordFriend.from_dict(friend) for friend in r.json()]


def get_channel_from_id(user_id: int) -> DiscordChannel:
    """
    Get the DM channel for a user.

    Args:
        user_id (int): The user's ID.

    Returns:
        DiscordChannel: The user's DM channel.
    """

    r = requests.post(
        f"{api_base}/users/@me/channels",
        headers=headers,
        json={"recipient_id": user_id},
    )
    
    # Check if the request was successful
    if r.status_code != 200:
        raise ChannelAccessError(f"Failed to get channel for user {user_id}: {r.status_code} - {r.text}")
    
    response_data = r.json()
    
    # Verify the response has the required 'id' field
    if "id" not in response_data:
        raise InvalidResponseError(f"Invalid channel response for user {user_id}: missing 'id' field. Response: {response_data}")
    
    return DiscordChannel.from_dict(response_data)


def get_guilds() -> list[DiscordGuild]:
    """
    Returns all the guilds (aka servers) the current user is in.

    Returns:
        list[DiscordGuild]: The user's guilds.
    """

    r = requests.get(f"{api_base}/users/@me/guilds", headers=headers)

    return [DiscordGuild.from_dict(guild) for guild in r.json()]


def get_guild_channels(guild_id: int) -> list[DiscordChannel]:
    """
    Returns all channels in a guild.

    Args:
        guild_id (int): The guild's ID.

    Returns:
        list[DiscordChannel]: The channels in the guild.
    """

    r = requests.get(f"{api_base}/guilds/{guild_id}/channels", headers=headers)

    return [DiscordChannel.from_dict(channel) for channel in r.json()]


def login(email: str, password: str, totp_code: str = "") -> str | None:
    """
    Takes in an email and a password, logs in, and spits out a token.

    Args:
        email (str): The email address for an account.
        password (str): The password for the account.

    Returns:
        str | None: A user token if login was successful, None otherwise.
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


def send_typing(channel: int) -> None:
    """
    Sends a typing indicator to a channel.

    Args:
        channel (int): The channel to send the typing indicator

    Returns:
        None
    """

    requests.post(f"{api_base}/channels/{channel}/typing", headers=headers)


def get_user_from_id(user_id: int, friend: bool = False) -> DiscordUser | DiscordFriend:
    # users_cache_data is mutable! It can and will be modified!
    """
    Returns the user with the specified ID.

    Args:
        user_id (int): A user's ID.
        friend (bool): Whether to instantiate a DiscordFriend or DiscordUser.

    Returns:
        DiscordUser | DiscordFriend: The user with the specified ID.
    """

    # Keep data in a cache so users don't get ratelimited
    if users_cache_data.get(user_id, False):
        return users_cache_data[user_id]

    # Wasn't cached.
    response = requests.get(f"{api_base}/users/{user_id}", headers=headers)

    if friend:
        user = DiscordFriend.from_dict(response.json())
    else:
        user = DiscordUser.from_dict(response.json())

    # Cache it for later.
    users_cache_data[user_id] = user

    return user
