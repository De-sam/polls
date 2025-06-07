import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from telegram import Update
from telegram.ext import ApplicationBuilder
from decouple import config

# Get your token securely
BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")

# Import your handlers from the bot file
from .bot import start, vote, handle_vote_selection

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
)

# Build the app once and reuse it
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("vote", vote))
app.add_handler(CallbackQueryHandler(handle_vote_selection))

@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            update = Update.de_json(data, app.bot)
            app.update_queue.put_nowait(update)
            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Only POST allowed"}, status=405)
from django.shortcuts import render

