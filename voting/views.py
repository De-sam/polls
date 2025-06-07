import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from telegram import Update
from asgiref.sync import async_to_sync
from .telegram_app import app  # 🔁 Your bot is initialized here

# Set up logging (optional but helpful)
logger = logging.getLogger(__name__)

@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            logger.info(f"📥 Received update: {data}")

            update = Update.de_json(data, app.bot)

            # ✅ Use async_to_sync to avoid 'event loop is closed' error
            async_to_sync(app.process_update)(update)

            return JsonResponse({"status": "ok"})
        except Exception as e:
            logger.error(f"❌ Error processing update: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST allowed"}, status=405)
