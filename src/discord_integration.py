import requests
import platformdirs
import keyring
import keyring.errors
import os
import sys
import time

from datetime import datetime
from discord_objects import (
    DiscordUser,
    DiscordMessage,
    DiscordFriend,
    DiscordChannel,
    DiscordGuild,
    users_cache_data,
)
from discord_exceptions import ChannelAccessError, InvalidResponseError, RateLimitError


api_base = "https://discord.com/api/v10"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.63 Chrome/124.0.6367.243 Electron/30.2.0 Safari/537.36"
}

# Will be set in load_token
keyring_available: bool = False


def load_token() -> None:
    """
    Loads the token from system keyring, otherwise falls back to checking discordauth.txt.
    """

    global headers, keyring_available

    try:
        auth = keyring.get_password("Qtcord", "token")
    except keyring.errors.NoKeyringError:
        print("WARNING: Keyring is not available! Falling back to plaintext storage!")
        keyring_available = False
        auth = ""

    # Check if keyring is writable if keyring doesn't have token
    if not auth:
        print("Checking if keyring is writable")
        keyring.set_password("Qtcord", "token", "test")
        if keyring.get_password("Qtcord", "token"):
            print("Keyring is available.")
            keyring_available = True
        else:
            print("Keyring is not available! Falling back to plaintext storage!")
            keyring_available = False
    else:
        # Since the keyring was available if auth exists
        keyring_available = True
        
    
    if keyring_available:
        if os.path.isfile(platformdirs.user_config_dir("Qtcord") + "/discordauth.txt"):
            print("Found discordauth.txt! Loading from discordauth.txt instead of system keychain!")
            with open(platformdirs.user_config_dir("Qtcord") + "/discordauth.txt") as f:
                auth = f.read().strip()
            
            print("Copying token to keyring!")
            keyring.set_password("Qtcord", "token", auth)

            token_path = os.path.join(platformdirs.user_config_dir("Qtcord"), "discordauth.txt")
            if os.path.exists(token_path):
                print("Deleting token from discordauth.txt!")
                os.remove(token_path)

        if auth:
            headers["authorization"] = auth
        else:
            print("Nothing is stored in keyring. ")
    else:
        if os.path.isfile(platformdirs.user_config_dir("Qtcord") + "/discordauth.txt"):
            with open(platformdirs.user_config_dir("Qtcord") + "/discordauth.txt") as f:
                auth = f.read()
            headers["authorization"] = auth.strip()


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

# If token is invalid, delete it and log us out.
# Inside validate_token is a function that checks for internet, too.
if not validate_token():
    # If there is a token and it's invalid
    print("TOKEN INVALID")

    # This will either run without erroring, so we don't need to check if it exists first.
    keyring.delete_password("Qtcord", "token")

    # Delete plaintext auth if it exists
    if os.path.exists(platformdirs.user_config_dir("Qtcord") + "/discordauth.txt"):
        os.remove(platformdirs.user_config_dir("Qtcord") + "/discordauth.txt")


def _check_ratelimit(response) -> None:
    if response.status_code == 429:
        if response.json()["global"]:
            print("Discord is ratelimiting us globally! We haven't handled this, so exiting!")
            sys.exit(0)
        
        print(f"We are being ratelimited! Retry after {response.json()["retry_after"]}")
        raise RateLimitError("Ratelimited by Discord API!", response.json()["retry_after"])


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

    r = requests.get(f"{api_base}/channels/{channel_id}/messages?limit={limit}", headers=headers)

    _check_ratelimit(r)

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
    
    r = requests.post(
        f"{api_base}/channels/{channel}/messages",
        headers=headers,
        json={"content": msg},
    )
    try:
        _check_ratelimit(r)
    except RateLimitError as e:
        print("We were ratelimited for sending the message! Cool off.")
        time.sleep(e.retry_after)
        print("Sending message again.")
        r = requests.post(
            f"{api_base}/channels/{channel}/messages",
            headers=headers,
            json={"content": msg},
        )
        # The error shouldn't happen at this point. If it does, it probably deserves to crash the program.
        _check_ratelimit(r)



def get_friends() -> list[DiscordFriend]:
    """
    Returns the current user's friends.

    Returns:
        list: The current user's friends.
    """

    r = requests.get(f"{api_base}/users/@me/relationships", headers=headers)
    _check_ratelimit(r)

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

    response_data = r.json()
    print(response_data)

    # Check if the request was successful
    _check_ratelimit(r)

    if r.status_code != 200:
        raise ChannelAccessError(f"Failed to get channel for user {user_id}: {r.status_code} - {r.text}")
    
    
    # Verify the response has the required 'id' field
    if "id" not in response_data:
        raise InvalidResponseError(
            f"Invalid channel response for user {user_id}: missing 'id' field. Response: {response_data}"
        )

    return DiscordChannel.from_dict(response_data)


def get_guilds() -> list[DiscordGuild]:
    """
    Returns all the guilds (aka servers) the current user is in.

    Returns:
        list[DiscordGuild]: The user's guilds.
    """

    r = requests.get(f"{api_base}/users/@me/guilds", headers=headers)
    _check_ratelimit(r)

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
    _check_ratelimit(r)

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


def get_user_from_id(user_id: int, friend: bool = False) -> DiscordUser | DiscordFriend | None:
    # users_cache_data is mutable! It can and will be modified!
    """
    Returns the user with the specified ID.

    Args:
        user_id (int): A user's ID.
        friend (bool): Whether to instantiate a DiscordFriend or DiscordUser.

    Returns:
        DiscordUser | DiscordFriend | None: The user with the specified ID or None, if the request doesn't succeed.
    """

    # Keep data in a cache so users don't get ratelimited
    if users_cache_data.get(user_id, False):
        return users_cache_data[user_id]

    # Wasn't cached.
    response = requests.get(f"{api_base}/users/{user_id}", headers=headers)
    _check_ratelimit(response)

    # If 403 - Forbidden code is returned
    if response.status_code == 403:
        return None
    
    if friend:
        user = DiscordFriend.from_dict(response.json())
    else:
        user = DiscordUser.from_dict(response.json())

    # Cache it for later.
    users_cache_data[user_id] = user

    return user
