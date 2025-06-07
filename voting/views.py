import json
import logging
import asyncio
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from telegram import Update
from .telegram_app import app

logger = logging.getLogger(__name__)

@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            logger.info(f"📥 Received update: {data}")
            update = Update.de_json(data, app.bot)

            # ✅ Don't run and close the loop every time — just schedule it
            asyncio.ensure_future(app.process_update(update))

            return JsonResponse({"status": "ok"})
        except Exception as e:
            logger.exception("🔥 Webhook error")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST allowed"}, status=405)
