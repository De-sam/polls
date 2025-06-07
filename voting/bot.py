import os
import logging
import uuid
import asyncio  # ✅ Needed for delay between messages
from decouple import config
from asgiref.sync import sync_to_async

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Django setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

from django.conf import settings
from django.utils.timezone import now
from voting.models import VotingCode

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")

# ---------- Voting Deadline Check ----------

def is_voting_expired():
    return now() > settings.VOTING_END_TIME

# ---------- Database Functions ----------

@sync_to_async
def get_or_create_voter(telegram_id):
    code = f"TGC-{telegram_id}-{uuid.uuid4().hex[:4].upper()}"
    try:
        voter, created = VotingCode.objects.get_or_create(
            telegram_user_id=telegram_id,
            defaults={"is_used": False, "code": code}
        )
        return voter, created
    except Exception as e:
        logger.error(f"🔥 Failed to create/get voter: {e}")
        raise

@sync_to_async
def get_voter(telegram_id):
    return VotingCode.objects.filter(telegram_user_id=telegram_id).first()

@sync_to_async
def get_positions_with_candidates():
    from candidates.models import Position
    positions = Position.objects.prefetch_related('candidates').all()
    result = []
    for pos in positions:
        candidates = list(pos.candidates.all())
        if candidates:
            result.append((str(pos.id), pos.name, candidates))
    return result

@sync_to_async
def get_total_positions_count():
    from candidates.models import Position
    return Position.objects.filter(candidates__isnull=False).distinct().count()

@sync_to_async
def save_votes(telegram_id, selections):
    from candidates.models import Candidate
    voter = VotingCode.objects.filter(telegram_user_id=telegram_id).first()
    if voter is None or voter.is_used:
        return False
    for candidate_id in selections.values():
        candidate = Candidate.objects.get(id=candidate_id)
        candidate.votes += 1
        candidate.save()
    voter.is_used = True
    voter.save()
    return True

# ---------- Handlers ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_voting_expired():
        await update.message.reply_text("⏳ Voting has ended. Thank you for your interest!")
        return
    telegram_id = str(update.effective_user.id)
    voter, _ = await get_or_create_voter(telegram_id)
    if voter.is_used:
        await update.message.reply_text("❌ Sorry you cannot vote more than once.")
    else:
        await update.message.reply_text(
            "👋🏽 Hello and welcome to the *2025/2026 Perfectship Elections*!\n\n"
            "This is ECCOLab's official Voting Bot 🧠🗳️—your digital ballot box.\n\n"
            "Ready to make your vote count? Send /vote to begin!",
            parse_mode="Markdown"
        )

async def vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_voting_expired():
        await update.message.reply_text("⏳ Voting has closed. We appreciate your enthusiasm!")
        return

    telegram_id = str(update.effective_user.id)
    voter = await get_voter(telegram_id)
    if not voter:
        await update.message.reply_text("🔐 You’re not registered. Please send /start first.")
        return
    if voter.is_used:
        await update.message.reply_text("🛑 You have already voted.")
        return

    if "selections" not in context.user_data:
        context.user_data["selections"] = {}

    positions_with_candidates = await get_positions_with_candidates()

    for position_id, position_name, candidates in positions_with_candidates:
        keyboard = [
            [InlineKeyboardButton(
                f"{c.surname} {c.first_name} ({c.student_class})",
                callback_data=f"{position_id}:{c.id}"
            )] for c in candidates
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"*{position_name}*\nPlease choose your candidate:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        await asyncio.sleep(0.4)  # ✅ Prevent Telegram from skipping messages

    submit_button = [[InlineKeyboardButton("📨 Submit Vote", callback_data="SUBMIT_VOTE")]]
    await update.message.reply_text(
        "✅ After selecting one candidate per position, click below to submit your vote.",
        reply_markup=InlineKeyboardMarkup(submit_button)
    )

async def handle_vote_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    telegram_id = str(query.from_user.id)
    data = query.data

    if "selections" not in context.user_data:
        context.user_data["selections"] = {}

    if data == "SUBMIT_VOTE":
        if is_voting_expired():
            await query.edit_message_text("⏳ Voting has ended. Submissions are no longer accepted.")
            return
        selections = context.user_data.get("selections", {})
        total_required = await get_total_positions_count()
        if not selections:
            await query.edit_message_text("⚠️ You haven’t selected any candidates. Please vote for at least one.")
            return
        success = await save_votes(telegram_id, selections)
        if success:
            context.user_data.clear()
            if len(selections) < total_required:
                await query.edit_message_text(
                    "✅ Your vote has been submitted successfully.\n"
                    "☑️ Note: You didn’t vote in all positions."
                )
            else:
                await query.edit_message_text("✅ Your vote has been submitted successfully. Thank you!")
        else:
            await query.edit_message_text("🛑 You already voted or something went wrong.")
        return

    try:
        position_id, candidate_id = data.split(":")
        context.user_data["selections"][position_id] = candidate_id
        await query.edit_message_text("✅ Selection saved. Continue voting or click 'Submit Vote' below.")
    except Exception as e:
        logger.error(f"Vote selection error: {e}")
        await query.edit_message_text("❌ Something went wrong while saving your selection.")

# ---------- Main ----------

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("vote", vote))
    app.add_handler(CallbackQueryHandler(handle_vote_selection))
    print("🚀 Bot is live! Listening for commands...")
    await app.run_polling()

# ---------- Entry Point ----------

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    import asyncio
    asyncio.run(main())
