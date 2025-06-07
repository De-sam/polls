from django.apps import AppConfig
import asyncio
import logging

class VotingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'voting'

    def ready(self):
        from .telegram_app import initialize_bot

        try:
            asyncio.run(initialize_bot())
            logging.info("✅ Telegram bot initialized at startup")
        except Exception as e:
            logging.exception("❌ Failed to initialize Telegram bot")
