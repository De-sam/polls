from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
)
from decouple import config
from .bot import start, vote, handle_vote_selection
import asyncio

BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")

# 🔧 Build the app once and use it everywhere
app = ApplicationBuilder().token(BOT_TOKEN).build()

# 📌 Register handlers just once
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("vote", vote))
app.add_handler(CallbackQueryHandler(handle_vote_selection))

# ✅ Initialize the app (REQUIRED for webhook mode)
loop = asyncio.get_event_loop()
loop.run_until_complete(app.initialize())
