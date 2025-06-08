from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
)
from telegram.ext import ApplicationHandlerStop
import logging
from decouple import config
from .bot import start, vote, handle_vote_selection

BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")
app = None

async def error_handler(update, context):
    logging.exception(f"❌ Error occurred: {context.error}")

async def initialize_bot():
    global app
    if app is not None:
        return app  # Already initialized

    try:
        app = ApplicationBuilder().token(BOT_TOKEN).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("vote", vote))
        app.add_handler(CallbackQueryHandler(handle_vote_selection))
        app.add_error_handler(error_handler)

        await app.initialize()
        await app.start()
        # ❌ REMOVE THIS LINE:
        # await app.post_init()

        logging.info("✅ Telegram bot initialized successfully.")
        return app

    except Exception as e:
        logging.exception("🚨 Failed to initialize Telegram bot:")
        raise RuntimeError("Bot initialization failed.") from e


def get_bot_app():
    if app is None:
        raise RuntimeError("Telegram bot app is not initialized. Call initialize_bot() first.")
    return app
