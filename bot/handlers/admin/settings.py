"""
Admin settings handlers
"""
from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards.admin_kb import get_admin_panel_keyboard, get_admin_settings_keyboard
from bot.keyboards.user_kb import get_back_keyboard


async def admin_settings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle admin settings"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text="<b>تنظیمات فروشگاه</b>\n\nبخش مورد نظر را انتخاب کنید:",
        reply_markup=get_admin_settings_keyboard(),
        parse_mode="HTML",
    )


async def admin_set_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle set store name"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text="نام جدید فروشگاه را وارد کنید:",
        reply_markup=get_back_keyboard("admin_settings"),
    )
    context.user_data["admin_state"] = "set_store_name"


async def admin_set_name_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, name: str) -> None:
    """Handle set store name text"""
    context.user_data["admin_state"] = None
    await update.message.reply_text(
        text=f"نام فروشگاه به {name} تغيير كرد.",
        reply_markup=get_admin_settings_keyboard(),
    )


async def admin_set_card_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle set card number"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text="شماره كارت جديد را وارد كنيد:",
        reply_markup=get_back_keyboard("admin_settings"),
    )
    context.user_data["admin_state"] = "set_card_number"


async def admin_set_card_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, card: str) -> None:
    """Handle set card number text"""
    context.user_data["admin_state"] = None
    await update.message.reply_text(
        text=f"شماره كارت به {card} تغيير كرد.",
        reply_markup=get_admin_settings_keyboard(),
    )


async def admin_toggle_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle toggle features"""
    query = update.callback_query
    await query.answer()

    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 بازنشاني تنظيمات", callback_data="admin_reset_settings")],
        [InlineKeyboardButton(".Back", callback_data="admin_panel")],
    ])

    await query.edit_message_text(
        text="Toggle features panel",
        reply_markup=markup,
    )
