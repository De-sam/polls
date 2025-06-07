import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from telegram import Update
from .telegram_app import app  # 👈 import from the new file

@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            update = Update.de_json(data, app.bot)

            # ⚠️ Required for webhook mode
            app.process_update(update)
            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Only POST allowed"}, status=405)
