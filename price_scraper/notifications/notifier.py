import logging

import discord

logger = logging.getLogger(__name__)


class Notifier:
    """
    Discord notification object.

    Attributes:
    webhook_url = Discord webhook url

    """

    def __init__(
        self,
        webhook_url: str | None = None
    ):

        if webhook_url:
            self.webhook_url = webhook_url
            self.dn = discord.SyncWebhook.from_url(self.webhook_url)
        else:
            logger.warning("No discord webhook url set."
                           "Discord notifications will not work.")

    def __repr__(self) -> str:
        return (f"Notifier(webhook_url={self.webhook_url!r})")

    def __str__(self) -> str:
        return f"Notifier; Discord webhook url: {self.webhook_url}"

    def discord_message(self, message):
        if self.webhook_url:
            try:
                self.dn.send(message)
            except Exception as e:
                logger.exception(f"Error sending discord message: {e}")
