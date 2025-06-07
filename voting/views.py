import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from telegram import Update
from .telegram_app import get_bot_app  # this must return a ready-to-use, initialized app
import asyncio

logger = logging.getLogger(__name__)

@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            # ✅ Get the already-initialized app ONCE
            app = get_bot_app()
            update = Update.de_json(data, app.bot)

            logger.info(f"📥 Received update: {data}")

            # Use a new event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(app.process_update(update))
            loop.close()

            return JsonResponse({"status": "ok"})

        except Exception as e:
            logger.exception("🔥 Webhook failed")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST allowed"}, status=405)
