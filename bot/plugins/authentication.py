import logging

from pyrogram import filters
from pyrogram.types import Message
from ..youtube import GoogleAuth
from ..config import Config
from ..translations import Messages as tr
from ..utubebot import UtubeBot

log = logging.getLogger(__name__)

@UtubeBot.on_message(
    filters.private &
    filters.incoming &
    filters.command("authorise") &
    filters.user(Config.AUTH_USERS)
)
async def _auth(client: UtubeBot, message: Message) -> None:
    if len(message.command) == 1:
        await message.reply_text(tr.NO_AUTH_CODE_MSG, True)
        return

    code = message.command[1]

    try:
        auth = GoogleAuth(Config.CLIENT_ID, Config.CLIENT_SECRET)
        auth.Auth(code)
        auth.SaveCredentialsFile(Config.CRED_FILE)

        await message.reply_text(tr.AUTH_SUCCESS_MSG, True)

        with open(Config.CRED_FILE, "r") as f:
            cred_data = f.read()

        log.debug(f"Authentication success, auth data saved to {Config.CRED_FILE}")

        await message.reply_text(
            f"This is your authorization data: {cred_data}\n\n"
            "Save this for later use. Reply /save_auth_data to save the authorization "
            "data again (helpful if you use Heroku)."
        )

    except Exception as e:
        log.error(f"Authentication failed: {e}", exc_info=True)
        await message.reply_text(tr.AUTH_FAILED_MSG.format(e), True)

@UtubeBot.on_message(
    filters.private &
    filters.incoming &
    filters.command("save_auth_data") &
    filters.reply &
    filters.user(Config.AUTH_USERS)
)
async def _save_auth_data(client: UtubeBot, message: Message) -> None:
    auth_data = message.reply_to_message.text

    try:
        with open(Config.CRED_FILE, "w") as f:
            f.write(auth_data)

        auth = GoogleAuth(Config.CLIENT_ID, Config.CLIENT_SECRET)
        auth.LoadCredentialsFile(Config.CRED_FILE)
        auth.authorize()

        await message.reply_text(tr.AUTH_DATA_SAVE_SUCCESS, True)
        log.debug(f"Authorization data saved successfully to {Config.CRED_FILE}")

    except Exception as e:
        log.error(f"Failed to save authorization data: {e}", exc_info=True)
        await message.reply_text(tr.AUTH_FAILED_MSG.format(e), True)
