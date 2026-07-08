"""
Search handler
"""
from telegram import Update
from telegram.ext import ContextTypes

from bot.database import async_session
from bot.services.game_service import GameService
from bot.keyboards.user_kb import get_search_keyboard, get_main_menu_keyboard
from bot.config.messages import get_search_message, get_no_results_message


async def search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle search"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text=get_search_message(),
        reply_markup=get_search_keyboard(),
        parse_mode="HTML",
    )


async def search_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle search text input"""
    if context.user_data.get("waiting_for") != "search":
        return

    search_query = update.message.text
    context.user_data["waiting_for"] = None

    async with async_session() as session:
        service = GameService(session)
        games = await service.search_games(search_query)

    if not games:
        await update.message.reply_text(
            text=get_no_results_message(),
            reply_markup=get_main_menu_keyboard(),
        )
        return

    buttons = []
    for game in games[:10]:
        buttons.append([{"text": f"🎮 {game.name} | {game.effective_price:,} تومان", "callback_data": f"game_{game.id}"}])
    buttons.append([{"text": "🔙 بازگشت", "callback_data": "main_menu"}])

    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(b["text"], callback_data=b["callback_data"]) for b in row]
        for row in buttons
    ])

    await update.message.reply_text(
        text=f"🔍 <b>نتایج جستجو برای: {search_query}</b>\n\n{len(games)} نتیجه یافت شد:",
        reply_markup=markup,
        parse_mode="HTML",
    )
