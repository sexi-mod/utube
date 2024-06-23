from pyrogram import Client  # Import Client from pyrogram
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
        self.counter = 0
        self.download_controller = {}

    async def start(self):
        await super().start()
        # Additional startup code if needed

    async def stop(self):
        await super().stop()
        # Additional cleanup code if needed

    async def on_message(self, message):
        # Handle incoming messages
        pass

    def example_function(self):
        print("Example function called.")

# This part of the code should not be in the utubebot.py file
if __name__ == "__main__":
    from pyrogram import Client
