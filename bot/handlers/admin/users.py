"""
Admin user management handlers
"""
from telegram import Update
from telegram.ext import ContextTypes

from bot.database import async_session
from bot.services.user_service import UserService
from bot.keyboards.admin_kb import (
    get_admin_panel_keyboard,
    get_admin_users_keyboard,
    get_admin_broadcast_keyboard,
)


async def admin_users_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle admin users menu"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text="👥 <b>مدیریت کاربران</b>\n\nعملیات مورد نظر را انتخاب کنید:",
        reply_markup=get_admin_users_keyboard(),
        parse_mode="HTML",
    )


async def admin_list_users_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle list users"""
    query = update.callback_query
    await query.answer()

    async with async_session() as session:
        service = UserService(session)
        users = await service.get_all_users(limit=20)

    text = "📋 <b>لیست کاربران</b>\n━━━━━━━━━━━━━━━━━━━━━━\n\n"

    if not users:
        text += "کاربری یافت نشد."
    else:
        for user in users:
            status = "🟢" if user.is_active else "🔴"
            text += (
                f"{status} {user.first_name or user.username or 'نامشخص'}\n"
                f"🆔 {user.telegram_id} | 📱 {user.phone or 'بدون شماره'}\n"
                f"🛒 خرید: {user.purchase_count} | 💰 کیف پول: {user.wallet_balance:,}\n\n"
            )

    await query.edit_message_text(
        text=text,
        reply_markup=get_admin_users_keyboard(),
        parse_mode="HTML",
    )


async def admin_search_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle search user"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text="🔍 نام کاربری یا آیدی تلگرام را وارد کنید:",
        reply_markup=get_admin_users_keyboard(),
    )
    context.user_data["admin_state"] = "search_user"


async def admin_search_user_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, query_text: str) -> None:
    """Handle search user text"""
    async with async_session() as session:
        service = UserService(session)

        # Try searching by telegram ID
        try:
            tid = int(query_text)
            user = await service.get_user(tid)
            if user:
                text = (
                    f"👤 <b>کاربر یافت شده:</b>\n\n"
                    f"📛 نام: {user.first_name or user.username or 'نامشخص'}\n"
                    f"🆔 آیدی: {user.telegram_id}\n"
                    f"📱 موبایل: {user.phone or 'ثبت نشده'}\n"
                    f"🛒 خرید: {user.purchase_count}\n"
                    f"💰 کیف پول: {user.wallet_balance:,} تومان\n"
                    f"⭐ امتیاز: {user.points}\n"
                )
                await update.message.reply_text(text=text, parse_mode="HTML")
                return
        except ValueError:
            pass

        users = await service.search_users(query_text)

    if not users:
        await update.message.reply_text("کاربری یافت نشد.")
        return

    text = f"🔍 <b>نتایج جستجو ({len(users)} نتیجه):</b>\n\n"
    for user in users[:10]:
        text += (
            f"👤 {user.first_name or user.username or 'نامشخص'}\n"
            f"🆔 {user.telegram_id}\n\n"
        )

    await update.message.reply_text(text=text, parse_mode="HTML")


async def admin_broadcast_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle broadcast"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text="📢 <b>ارسال همگانی</b>\n\nنوع پیام را انتخاب کنید:",
        reply_markup=get_admin_broadcast_keyboard(),
        parse_mode="HTML",
    )


async def admin_broadcast_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle broadcast text"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text="📝 متن پیام همگانی را وارد کنید:",
        reply_markup=get_admin_broadcast_keyboard(),
    )
    context.user_data["admin_state"] = "broadcast_text"


async def admin_broadcast_text_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str) -> None:
    """Handle broadcast text input"""
    context.user_data["admin_state"] = None
    context.user_data["broadcast_text"] = text

    from bot.keyboards.admin_kb import get_admin_confirm_keyboard
    await update.message.reply_text(
        text=f"📢 <b>پیش‌نمایش پیام:</b>\n\n{text}\n\nآیا مطمئن هستید؟",
        reply_markup=get_admin_confirm_keyboard("broadcast"),
        parse_mode="HTML",
    )


async def admin_confirm_broadcast_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Confirm and send broadcast"""
    query = update.callback_query
    await query.answer()

    text = context.user_data.get("broadcast_text", "")
    context.user_data["broadcast_text"] = None

    async with async_session() as session:
        service = UserService(session)
        users = await service.get_all_users(limit=10000)

    sent = 0
    for user in users:
        try:
            from bot.config.settings import Config
            bot = context.bot
            await bot.send_message(chat_id=user.telegram_id, text=text, parse_mode="HTML")
            sent += 1
        except Exception:
            continue

    from bot.config.messages import get_broadcast_success_message
    await query.edit_message_text(
        text=get_broadcast_success_message(sent),
        reply_markup=get_admin_panel_keyboard(),
    )
