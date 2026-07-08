"""
Favorites handler
"""
from telegram import Update
from telegram.ext import ContextTypes

from bot.database import async_session
from bot.services.favorite_service import FavoriteService
from bot.keyboards.user_kb import get_main_menu_keyboard
from bot.config.messages import get_favorites_message


async def favorites_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle favorites list"""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id

    async with async_session() as session:
        service = FavoriteService(session)
        games = await service.get_favorites(user_id)

    text = get_favorites_message() + "\n\n"

    if not games:
        text += "لیست علاقه‌مندی‌های شما خالی است."
        buttons = [[{"text": "🔙 بازگشت", "callback_data": "main_menu"}]]
    else:
        buttons = []
        for game in games:
            buttons.append([{"text": f"❤️ {game.name} | {game.effective_price:,} تومان", "callback_data": f"game_{game.id}"}])
        buttons.append([{"text": "🔙 بازگشت", "callback_data": "main_menu"}])

    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(b["text"], callback_data=b["callback_data"]) for b in row]
        for row in buttons
    ])

    await query.edit_message_text(
        text=text,
        reply_markup=markup,
        parse_mode="HTML",
    )


async def add_favorite_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle add to favorites"""
    query = update.callback_query

    game_id = int(query.data.split("_")[2])
    user_id = update.effective_user.id

    async with async_session() as session:
        service = FavoriteService(session)
        added = await service.add_favorite(user_id, game_id)

    if added:
        await query.answer("✅ به علاقه‌مندی‌ها اضافه شد", show_alert=True)
    else:
        await query.answer("قبلاً اضافه شده است", show_alert=True)


async def remove_favorite_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle remove from favorites"""
    query = update.callback_query

    game_id = int(query.data.split("_")[2])
    user_id = update.effective_user.id

    async with async_session() as session:
        service = FavoriteService(session)
        await service.remove_favorite(user_id, game_id)

    await query.answer("💔 از علاقه‌مندی‌ها حذف شد", show_alert=True)
