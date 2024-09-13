from dataclasses import dataclass
from datetime import datetime
from typing import Self


@dataclass
class DiscordUser:
    id: int
    avatar: str
    user_name: str
    global_name: str

    @classmethod
    def from_dict(cls, user: dict) -> Self:
        """
        Creates an instance of DiscordUser from a dictionary.

        Args:
            user (dict): A dictionary with user data from the Discord API.

        Returns:
            Self: A DiscordUser instance.
        """
        return cls(
            id=user["id"],
            avatar=user["avatar"],
            user_name=user["username"],
            global_name=user["global_name"],
        )

    def get_user_name(self) -> str:
        """
        Get the user's display name if possible. Otherwise, return the raw username.

        Returns:
            str: The user's username
        """
        return self.global_name if self.global_name else self.user_name

    def get_avatar_url(self, size: int = 128) -> str:
        """
        Returns a url containing the avatar for this user.

        Args:
            size (int): The length and width of the image. Must be something like 128, 256, 512...

        Returns:
            str: The avatar url.
        """
        avatar_url = ""
        if self.avatar:
            avatar_url = f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar}.webp?size={size}"
        return avatar_url


@dataclass
class DiscordFriend:
    user: DiscordUser
    nickname: str

    @classmethod
    def from_dict(cls, friend: dict) -> Self:
        """
        Creates an instance of DiscordUser from a dictionary.

        Args:
            friend (dict): A dictionary with user data from the Discord API.

        Returns:
            Self: A DiscordFriend instance.
        """
        return cls(
            user=DiscordUser.from_dict(friend["user"]),
            nickname=friend["nickname"],
        )

    def get_friend_name(self) -> str:
        """
        Returns the friend's nickname if it exists, otherwise the username.

        Returns:
            str: A username or nickname.
        """
        return self.nickname if self.nickname else self.user.get_user_name()


@dataclass
class DiscordMessage:
    # TODO: referenced_message may need to be added in a future release.
    # This allows for loading more messages above this one.
    # That is to say,
    # https://discord.com/api/v9/channels/%7Bchannel_id%7D/messages?before={message}&limit={message_limit}
    id: int
    author: DiscordUser
    content: str
    timestamp: datetime

    @classmethod
    def from_dict(cls, message: dict) -> Self:
        """
        Creates an instance of DiscordMessage from a dictionary.

        Args:
            message (dict): A dictionary with message data from the Discord API.

        Returns:
            Self: A DiscordMessage instance.
        """
        # := is called the walrus operator.
        # Basically, this code between the parentheses would be
        # content = message["content"]
        # if content: ...

        # TODO: WORK ON THIS. Make a difference between images and other stuff.
        if not (content := message["content"]):
            content = "[(call/image/other)]"

        # For some reason, messages can use two, slightly different, timestamp formats.
        time_str = message["timestamp"]
        if len(time_str) == 32:
            timestamp = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%f%z")
        else:
            timestamp = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S%z")

        return cls(
            id=message["id"],
            author=DiscordUser.from_dict(message["author"]),
            content=content,
            timestamp=timestamp.astimezone(),
        )


@dataclass
class DiscordChannel:
    id: int
    type: int
    name: str | None
    recipients: list[DiscordUser]

    @classmethod
    def from_dict(cls, channel: dict) -> Self:
        """
        Creates an instance of DiscordChannel from a dictionary.

        Args:
            channel (dict): A dictionary with channel data from the Discord API.

        Returns:
            Self: A DiscordChannel instance.
        """
        return cls(
            id=channel["id"],
            type=channel["type"],
            name=channel.get("name"),
            recipients=[
                DiscordUser.from_dict(user) for user in channel.get("recipients", [])
            ],
        )

    def get_channel_name(self) -> str | None:
        if self.type in (1, 3):  # DM or GROUP_DM types, respectively
            return self.get_dm_name()
        else:
            return self.name

    def get_dm_name(self) -> str:
        return "+".join(recipient.get_user_name() for recipient in self.recipients)


@dataclass
class DiscordGuild:
    id: int
    name: str
    icon: str

    @classmethod
    def from_dict(cls, guild: dict) -> Self:
        """
        Creates an instance of DiscordGuild from a dictionary.

        Args:
            guild (dict): A dictionary with guild data from the Discord API.

        Returns:
            Self: A DiscordGuild instance.
        """
        return cls(id=guild["id"], name=guild["name"], icon=guild["icon"])

    def get_icon_url(self, size: int = 128) -> str:
        """
        Returns the guild's icon url.

        Arguments:
            size (int): The length and width of the image. Must be something like 128, 256, 512...

        Returns:
            str: The guild's icon url.
        """
        icon_url = ""
        if self.icon:
            icon_url = (
                f"https://cdn.discordapp.com/icons/{self.id}/{self.icon}?size={size}"
            )
        return icon_url
