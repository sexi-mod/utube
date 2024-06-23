from pyrogram import Client

from .config import Config


class UtubeBot(Client):
    def __init__(self):
        name = Config.SESSION_NAME
        super().__init__(
            name,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            plugins=dict(root="bot.plugins"),
            workers=6,
        )
        self.DOWNLOAD_WORKERS = 6
        modify to was
