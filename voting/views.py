import json
import asyncio
import logging
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

            # ✅ Ensure bot is initialized
            async def handle_update():
                await app.initialize()  # <--- required to bootstrap async processing
                await app.process_update(update)

            asyncio.ensure_future(handle_update())

            return JsonResponse({"status": "ok"})
        except Exception as e:
            logger.exception("🔥 Webhook error")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST allowed"}, status=405)
