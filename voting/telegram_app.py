# voting/telegram_app.py
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
)
from decouple import config
from .bot import start, vote, handle_vote_selection

BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")

# Create the app only once
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Register handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("vote", vote))
app.add_handler(CallbackQueryHandler(handle_vote_selection))
