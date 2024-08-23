from telegram import Update
from telegram.ext import CallbackContext


async def start(update: Update, context: CallbackContext) -> None:
    """Обработка команды `/start`."""
    tg_user = update.effective_user
    tg_chat = update.effective_chat
    await context.bot.send_message(
        tg_chat.id,
        f'Welcome, {tg_user.full_name}!',
    )
