from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
)
from decouple import config
from .bot import start, vote, handle_vote_selection
import asyncio

BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")

# Build bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Register handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("vote", vote))
app.add_handler(CallbackQueryHandler(handle_vote_selection))

# ✅ Properly initialize bot for webhook mode
asyncio.run(app.initialize())
