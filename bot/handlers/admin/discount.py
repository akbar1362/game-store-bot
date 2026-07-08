"""
Admin discount management handlers
"""
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes

from bot.database import async_session
from bot.services.discount_service import DiscountService
from bot.keyboards.admin_kb import (
    get_admin_panel_keyboard,
    get_admin_discount_keyboard,
)
from bot.keyboards.user_kb import get_back_keyboard


async def admin_discounts_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle admin discounts menu"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text="🎁 <b>مدیریت تخفیف‌ها</b>\n\nعملیات مورد نظر را انتخاب کنید:",
        reply_markup=get_admin_discount_keyboard(),
        parse_mode="HTML",
    )


async def admin_add_discount_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle add discount code"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text=(
            "➕ <b>افزودن کد تخفیف</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "کد تخفیف را وارد کنید:"
        ),
        reply_markup=get_back_keyboard("admin_discounts"),
        parse_mode="HTML",
    )
    context.user_data["admin_state"] = "add_discount_code"


async def admin_add_discount_code_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, code: str) -> None:
    """Handle discount code input"""
    context.user_data["new_discount"] = {"code": code.upper()}

    await update.message.reply_text(
        text="📝 نوع تخفیف را انتخاب کنید:\n1. درصدی\n2. مبلغ ثابت",
        reply_markup=get_back_keyboard("admin_discounts"),
    )
    context.user_data["admin_state"] = "add_discount_type"


async def admin_add_discount_type_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, type_val: str) -> None:
    """Handle discount type input"""
    if type_val == "1":
        context.user_data["new_discount"]["discount_type"] = "percentage"
        await update.message.reply_text("📝 درصد تخفیف را وارد کنید:")
    elif type_val == "2":
        context.user_data["new_discount"]["discount_type"] = "fixed"
        await update.message.reply_text("📝 مبلغ تخفیف (تومان) را وارد کنید:")
    else:
        await update.message.reply_text("❌ لطفاً 1 یا 2 را وارد کنید.")
        return

    context.user_data["admin_state"] = "add_discount_value"


async def admin_add_discount_value_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, value: str) -> None:
    """Handle discount value input"""
    try:
        context.user_data["new_discount"]["discount_value"] = int(value)
    except ValueError:
        await update.message.reply_text("❌ لطفاً یک عدد صحیح وارد کنید.")
        return

    await update.message.reply_text(
        text="💰 حداقل مبلغ سفارش (تومان) را وارد کنید (0 برای بدون محدودیت):",
        reply_markup=get_back_keyboard("admin_discounts"),
    )
    context.user_data["admin_state"] = "add_discount_min"


async def admin_add_discount_min_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, min_val: str) -> None:
    """Handle discount min amount input"""
    try:
        context.user_data["new_discount"]["min_order_amount"] = int(min_val)
    except ValueError:
        await update.message.reply_text("❌ لطفاً یک عدد صحیح وارد کنید.")
        return

    await update.message.reply_text(
        text="🔢 حداکثر تعداد استفاده را وارد کنید (-1 برای نامحدود):",
        reply_markup=get_back_keyboard("admin_discounts"),
    )
    context.user_data["admin_state"] = "add_discount_max"


async def admin_add_discount_max_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, max_val: str) -> None:
    """Handle discount max uses input"""
    try:
        context.user_data["new_discount"]["max_uses"] = int(max_val)
    except ValueError:
        await update.message.reply_text("❌ لطفاً یک عدد صحیح وارد کنید.")
        return

    await update.message.reply_text(
        text="📅 تاریخ انقضا (YYYY-MM-DD) را وارد کنید (یا /skip):",
        reply_markup=get_back_keyboard("admin_discounts"),
    )
    context.user_data["admin_state"] = "add_discount_expiry"


async def admin_add_discount_expiry_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, expiry: str) -> None:
    """Handle discount expiry input"""
    discount_data = context.user_data.pop("new_discount", {})

    if expiry != "/skip":
        try:
            discount_data["expires_at"] = datetime.strptime(expiry, "%Y-%m-%d")
        except ValueError:
            await update.message.reply_text("❌ فرمت تاریخ نادرست است.")
            return

    context.user_data["admin_state"] = None

    async with async_session() as session:
        service = DiscountService(session)
        discount = await service.create_discount(**discount_data)

    await update.message.reply_text(
        text=(
            f"✅ کد تخفیف «{discount.code}» ایجاد شد.\n\n"
            f"📝 نوع: {discount.discount_type}\n"
            f"💰 مقدار: {discount.discount_value}\n"
            f"📦 حداقل مبلغ: {discount.min_order_amount:,} تومان\n"
            f"🔢 حداکثر استفاده: {discount.max_uses}"
        ),
        reply_markup=get_admin_discount_keyboard(),
        parse_mode="HTML",
    )


async def admin_list_discounts_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle list discount codes"""
    query = update.callback_query
    await query.answer()

    async with async_session() as session:
        service = DiscountService(session)
        discounts = await service.get_all_discounts()

    text = "📋 <b>لیست کدهای تخفیف</b>\n━━━━━━━━━━━━━━━━━━━━━━\n\n"

    if not discounts:
        text += "کد تخفیفی ثبت نشده."
    else:
        for d in discounts:
            status = "🟢" if d.is_valid else "🔴"
            text += (
                f"{status} <code>{d.code}</code>\n"
                f"📝 نوع: {d.discount_type} | 💰 مقدار: {d.discount_value}\n"
                f"🔢 استفاده: {d.current_uses}/{d.max_uses if d.max_uses != -1 else '∞'}\n\n"
            )

    await query.edit_message_text(
        text=text,
        reply_markup=get_admin_discount_keyboard(),
        parse_mode="HTML",
    )
