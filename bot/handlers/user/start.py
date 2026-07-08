"""
Start and welcome handlers
"""
from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.database import async_session
from bot.services.user_service import UserService
from bot.keyboards.user_kb import get_welcome_keyboard, get_main_menu_keyboard
from bot.config.messages import get_welcome_message, get_main_menu_message


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user = update.effective_user
    if not user:
        return

    async with async_session() as session:
        service = UserService(session)
        await service.get_or_create_user(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )

    await update.message.reply_text(
        text=get_welcome_message(),
        reply_markup=get_welcome_keyboard(),
        parse_mode="HTML",
    )


async def enter_store_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle enter store button"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text=get_main_menu_message(),
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )
