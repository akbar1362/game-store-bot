"""
Admin panel main handler
"""
from telegram import Update
from telegram.ext import ContextTypes

from bot.database import async_session
from bot.services.admin_service import AdminService
from bot.keyboards.admin_kb import get_admin_panel_keyboard
from bot.config.messages import get_admin_panel_message, get_admin_stats_message


async def admin_panel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle admin panel"""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    from bot.config.settings import Config

    if user_id not in Config.ADMIN_IDS:
        await query.answer("❌ دسترسی غیرمجاز", show_alert=True)
        return

    await query.edit_message_text(
        text=get_admin_panel_message(),
        reply_markup=get_admin_panel_keyboard(),
        parse_mode="HTML",
    )


async def exit_admin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle exit admin panel"""
    query = update.callback_query
    await query.answer()

    from bot.keyboards.user_kb import get_main_menu_keyboard
    from bot.config.messages import get_main_menu_message

    await query.edit_message_text(
        text=get_main_menu_message(),
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )


async def admin_stats_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle admin statistics"""
    query = update.callback_query
    await query.answer()

    async with async_session() as session:
        service = AdminService(session)
        stats = await service.get_stats()

    text = get_admin_stats_message(
        users=stats["users"],
        orders=stats["orders"],
        today_income=stats["today_income"],
        month_income=stats["month_income"],
        top_game=stats["top_game"],
        online_users=stats["online_users"],
    )

    from bot.keyboards.user_kb import get_back_keyboard
    await query.edit_message_text(
        text=text,
        reply_markup=get_back_keyboard("admin_panel"),
        parse_mode="HTML",
    )
