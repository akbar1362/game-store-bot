"""
Main menu handler
"""
from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards.user_kb import get_main_menu_keyboard
from bot.config.messages import get_main_menu_message


async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle main menu"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text=get_main_menu_message(),
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )
