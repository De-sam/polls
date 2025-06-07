from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
)
from telegram.ext import ApplicationHandlerStop  # Optional but good for advanced handling
import logging
from decouple import config
from .bot import start, vote, handle_vote_selection

BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")

app = None

# Define the error handler
async def error_handler(update, context: CallbackContext):
    logging.exception(f"❌ Error occurred: {context.error}")

def get_bot_app():
    global app
    if app is None:
        app = ApplicationBuilder().token(BOT_TOKEN).build()

        # Register command + callback handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("vote", vote))
        app.add_handler(CallbackQueryHandler(handle_vote_selection))

        # Register the error handler 🛡️
        app.add_error_handler(error_handler)

    return app
