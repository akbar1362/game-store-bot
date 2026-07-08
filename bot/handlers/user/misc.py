"""
Misc handlers (contact, about, discount code, review)
"""
from telegram import Update
from telegram.ext import ContextTypes

from bot.database import async_session
from bot.services.discount_service import DiscountService
from bot.services.review_service import ReviewService
from bot.keyboards.user_kb import get_main_menu_keyboard, get_back_keyboard, get_review_keyboard
from bot.config.messages import get_contact_message, get_about_message, get_discount_code_message


async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle contact us"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text=get_contact_message(),
        reply_markup=get_back_keyboard("main_menu"),
        parse_mode="HTML",
    )


async def about_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle about us"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text=get_about_message(),
        reply_markup=get_back_keyboard("main_menu"),
        parse_mode="HTML",
    )


async def discount_code_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle discount code entry"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text=get_discount_code_message(),
        reply_markup=get_back_keyboard("main_menu"),
        parse_mode="HTML",
    )
    context.user_data["waiting_for"] = "discount_code"


async def discount_code_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle discount code text input"""
    if context.user_data.get("waiting_for") != "discount_code":
        return

    code = update.message.text.strip()
    context.user_data["waiting_for"] = None

    async with async_session() as session:
        service = DiscountService(session)
        valid, message = await service.validate_code(code)

    await update.message.reply_text(
        text=message,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )


async def review_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle review button"""
    query = update.callback_query
    await query.answer()

    game_id = int(query.data.split("_")[1])

    await query.edit_message_text(
        text="⭐ <b>امتیازدهی</b>\n\nیکی از امتیازات را انتخاب کنید:",
        reply_markup=get_review_keyboard(game_id),
        parse_mode="HTML",
    )


async def rate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle rating"""
    query = update.callback_query

    parts = query.data.split("_")
    game_id = int(parts[1])
    rating = int(parts[2])
    user_id = update.effective_user.id

    async with async_session() as session:
        service = ReviewService(session)
        await service.add_review(user_id, game_id, rating)

    stars = "⭐" * rating
    await query.answer(f"✅ امتیاز {stars} ثبت شد", show_alert=True)

    from bot.keyboards.user_kb import get_game_detail_keyboard
    await query.edit_message_reply_markup(
        reply_markup=get_game_detail_keyboard(game_id)
    )


async def share_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle share game"""
    query = update.callback_query
    await query.answer()

    game_id = int(query.data.split("_")[1])

    from bot.config.settings import Config

    share_text = (
        f"🎮 {Config.STORE_NAME}\n\n"
        f"بازی مورد علاقه‌تان را اینجا ببینید!\n"
        f"لینک: https://t.me/{context.bot.username}?start=game_{game_id}"
    )

    await query.message.reply_text(
        text=share_text,
        reply_markup=get_main_menu_keyboard(),
    )
