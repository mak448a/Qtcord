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
        return cls(
            id = user["id"],
            avatar = user["avatar"],
            user_name = user["username"],
            global_name = user["global_name"],
        )

    def get_user_name(self) -> str:
        return self.global_name if self.global_name else self.user_name

    def get_avatar_url(self, size: int = 128) -> str:
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
        return cls(
            user = DiscordUser.from_dict(friend["user"]),
            nickname = friend["nickname"],
        )

    def get_friend_name(self) -> str:
        return self.nickname if self.nickname else self.user.get_user_name()

@dataclass
class DiscordMessage:
    id: int
    author: DiscordUser
    content: str
    timestamp: datetime

    @classmethod
    def from_dict(cls, message: dict) -> Self:
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
        return cls(
            id = channel["id"],
            type = channel["type"],
            name = channel.get("name"),
            recipients = [DiscordUser.from_dict(user) for user in channel.get("recipients", [])],
        )

    def get_channel_name(self) -> str:
        if self.type in (1, 3): # DM or GROUP_DM types, respectively
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
        return cls(
            id = guild["id"],
            name = guild["name"],
            icon = guild["icon"]
        )

    def get_icon_url(self, size: int = 128) -> str:
        icon_url = ""
        if self.icon:
            icon_url = f"https://cdn.discordapp.com/icons/{self.id}/{self.icon}?size={size}"
        return icon_url
