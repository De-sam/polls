from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
)
from decouple import config
from .bot import start, vote, handle_vote_selection
import asyncio

BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")

# Global bot application
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Register handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("vote", vote))
app.add_handler(CallbackQueryHandler(handle_vote_selection))


async def setup_bot():
    await app.initialize()
    await app.start()  # 🔥 This fixes the first-run issue
    # DO NOT call idle() since we’re using Django webhook mode
    print("✅ Telegram bot initialized and ready via webhook")


# Properly launch setup
asyncio.run(setup_bot())
