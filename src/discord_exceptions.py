"""
Custom exceptions for Discord API operations.
"""


class DiscordAPIError(Exception):
    """Base exception for Discord API-related errors."""

    pass


class ChannelAccessError(DiscordAPIError):
    """Raised when unable to access or retrieve a channel."""

    pass


class InvalidResponseError(DiscordAPIError):
    """Raised when Discord API returns an invalid response."""

    pass


class RateLimitError(DiscordAPIError):
    """Raised when Discord API ratelimits."""

    def __init__(self, message, retry_after) -> None:
        super().__init__(message)
        self.retry_after = retry_after
