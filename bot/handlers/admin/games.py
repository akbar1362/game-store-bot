"""
Admin game management handlers
"""
from telegram import Update
from telegram.ext import ContextTypes

from bot.database import async_session
from bot.services.game_service import GameService
from bot.keyboards.admin_kb import (
    get_admin_panel_keyboard,
    get_admin_games_keyboard,
    get_admin_game_edit_keyboard,
    get_admin_confirm_keyboard,
)
from bot.keyboards.user_kb import get_back_keyboard


async def admin_games_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle admin games menu"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text="🎮 <b>مدیریت بازی‌ها</b>\n\nعملیات مورد نظر را انتخاب کنید:",
        reply_markup=get_admin_games_keyboard(),
        parse_mode="HTML",
    )


async def admin_add_game_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle add game - start flow"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text=(
            "➕ <b>افزودن بازی جدید</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "نام بازی را وارد کنید:"
        ),
        reply_markup=get_back_keyboard("admin_games"),
        parse_mode="HTML",
    )
    context.user_data["admin_state"] = "add_game_name"


async def admin_list_games_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle list games for admin"""
    query = update.callback_query
    await query.answer()

    async with async_session() as session:
        service = GameService(session)
        games = await service.get_all_games(limit=20, is_active=True)

    text = "📋 <b>لیست بازی‌ها</b>\n━━━━━━━━━━━━━━━━━━━━━━\n\n"

    if not games:
        text += "بازی‌ای ثبت نشده است."
    else:
        for game in games:
            stock = "✅" if game.stock_status == "in_stock" else "❌"
            text += f"{stock} #{game.id} | {game.name}\n💰 {game.price:,} تومان | 📦 {game.stock_display}\n\n"

    await query.edit_message_text(
        text=text,
        reply_markup=get_admin_games_keyboard(),
        parse_mode="HTML",
    )


async def admin_edit_game_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle edit game"""
    query = update.callback_query
    await query.answer()

    # Extract game ID from callback data
    parts = query.data.split("_")
    game_id = int(parts[-1])

    async with async_session() as session:
        service = GameService(session)
        game = await service.get_game(game_id)

    if not game:
        await query.answer("❌ بازی یافت نشد", show_alert=True)
        return

    text = (
        f"📝 <b>ویرایش بازی: {game.name}</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"💰 قیمت: {game.price:,} تومان\n"
        f"📦 موجودی: {game.stock_display}\n"
        f"🔥 تخفیف: {game.discount_percent}%\n"
    )

    await query.edit_message_text(
        text=text,
        reply_markup=get_admin_game_edit_keyboard(game_id),
        parse_mode="HTML",
    )


async def admin_delete_game_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle delete game"""
    query = update.callback_query
    await query.answer()

    game_id = int(query.data.split("_")[-1])

    await query.edit_message_text(
        text=f"⚠️ آیا از حذف بازی #{game_id} مطمئن هستید؟",
        reply_markup=get_admin_confirm_keyboard(f"delete_game_{game_id}"),
        parse_mode="HTML",
    )


async def admin_confirm_delete_game_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Confirm delete game"""
    query = update.callback_query
    await query.answer()

    game_id = int(query.data.split("_")[-1])

    async with async_session() as session:
        service = GameService(session)
        deleted = await service.delete_game(game_id)

    if deleted:
        await query.edit_message_text(
            text=f"✅ بازی #{game_id} حذف شد.",
            reply_markup=get_admin_games_keyboard(),
        )
    else:
        await query.edit_message_text(
            text="❌ خطا در حذف بازی.",
            reply_markup=get_admin_games_keyboard(),
        )


async def admin_game_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, name: str) -> None:
    """Handle game name input"""
    context.user_data["new_game"] = {"name": name}

    await update.message.reply_text(
        text="💰 قیمت بازی (تومان) را وارد کنید:",
        reply_markup=get_back_keyboard("admin_games"),
    )
    context.user_data["admin_state"] = "add_game_price"


async def admin_game_price_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, price: str) -> None:
    """Handle game price input"""
    try:
        context.user_data["new_game"]["price"] = int(price.replace(",", ""))
    except ValueError:
        await update.message.reply_text("❌ لطفاً یک عدد صحیح وارد کنید.")
        return

    await update.message.reply_text(
        text="📝 توضیحات بازی را وارد کنید:",
        reply_markup=get_back_keyboard("admin_games"),
    )
    context.user_data["admin_state"] = "add_game_desc"


async def admin_game_desc_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, desc: str) -> None:
    """Handle game description input"""
    context.user_data["new_game"]["description"] = desc

    from bot.config.constants import GameCategory
    categories = [c.value for c in GameCategory]

    text = "🎭 ژانر بازی را انتخاب کنید:\n\n"
    for i, cat in enumerate(categories, 1):
        text += f"{i}. {cat}\n"

    await update.message.reply_text(text=text, reply_markup=get_back_keyboard("admin_games"))
    context.user_data["admin_state"] = "add_game_category"


async def admin_game_category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str) -> None:
    """Handle game category input"""
    context.user_data["new_game"]["category"] = category

    await update.message.reply_text(
        text="🎮 پلتفرم‌ها را وارد کنید (مثال: PS5, Xbox Series X):",
        reply_markup=get_back_keyboard("admin_games"),
    )
    context.user_data["admin_state"] = "add_game_platform"


async def admin_game_platform_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, platforms: str) -> None:
    """Handle game platform input"""
    context.user_data["new_game"]["platforms"] = platforms

    from bot.config.constants import GameVersion
    versions = [v.value for v in GameVersion]

    text = "📦 نسخه بازی را انتخاب کنید:\n\n"
    for i, v in enumerate(versions, 1):
        text += f"{i}. {v}\n"

    await update.message.reply_text(text=text, reply_markup=get_back_keyboard("admin_games"))
    context.user_data["admin_state"] = "add_game_version"


async def admin_game_version_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, version: str) -> None:
    """Handle game version input"""
    context.user_data["new_game"]["version"] = version

    await update.message.reply_text(
        text="🖼️ لینک تصویر بازی را وارد کنید (یا /skip برای رد کردن):",
        reply_markup=get_back_keyboard("admin_games"),
    )
    context.user_data["admin_state"] = "add_game_image"


async def admin_game_image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, image: str) -> None:
    """Handle game image input"""
    if image != "/skip":
        context.user_data["new_game"]["image_url"] = image

    await update.message.reply_text(
        text="🔥 درصد تخفیف را وارد کنید (0 برای عدم تخفیف):",
        reply_markup=get_back_keyboard("admin_games"),
    )
    context.user_data["admin_state"] = "add_game_discount"


async def admin_game_discount_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, discount: str) -> None:
    """Handle game discount input"""
    try:
        discount_pct = int(discount)
        game_data = context.user_data["new_game"]
        game_data["discount_percent"] = discount_pct
        if discount_pct > 0:
            game_data["discount_price"] = int(game_data["price"] * (100 - discount_pct) / 100)
    except ValueError:
        await update.message.reply_text("❌ لطفاً یک عدد صحیح وارد کنید.")
        return

    await update.message.reply_text(
        text="🔢 رده سنی را وارد کنید (مثال: 18+):",
        reply_markup=get_back_keyboard("admin_games"),
    )
    context.user_data["admin_state"] = "add_game_age"


async def admin_game_age_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, age: str) -> None:
    """Handle game age rating input"""
    context.user_data["new_game"]["age_rating"] = age

    await update.message.reply_text(
        text="📅 تاریخ انتشار را وارد کنید (YYYY-MM-DD یا /skip):",
        reply_markup=get_back_keyboard("admin_games"),
    )
    context.user_data["admin_state"] = "add_game_date"


async def admin_game_date_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, date: str) -> None:
    """Handle game release date input"""
    if date != "/skip":
        context.user_data["new_game"]["release_date"] = date

    # Create the game
    game_data = context.user_data.pop("new_game", {})
    context.user_data["admin_state"] = None

    async with async_session() as session:
        service = GameService(session)
        game = await service.create_game(**game_data)

    await update.message.reply_text(
        text=f"✅ بازی «{game.name}» با موفقیت ایجاد شد.\nشناسه: #{game.id}",
        reply_markup=get_admin_games_keyboard(),
        parse_mode="HTML",
    )


async def admin_edit_game_price_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle edit game price"""
    query = update.callback_query
    await query.answer()

    game_id = int(query.data.split("_")[-1])
    context.user_data["editing_game_id"] = game_id

    await query.edit_message_text(
        text="💰 قیمت جدید را وارد کنید:",
        reply_markup=get_back_keyboard("admin_games"),
    )
    context.user_data["admin_state"] = "edit_game_price"


async def admin_edit_game_stock_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle edit game stock"""
    query = update.callback_query
    await query.answer()

    game_id = int(query.data.split("_")[-1])

    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ موجود", callback_data=f"set_stock_{game_id}_in_stock")],
        [InlineKeyboardButton("❌ ناموجود", callback_data=f"set_stock_{game_id}_out_of_stock")],
        [InlineKeyboardButton("⏳ پیش فروش", callback_data=f"set_stock_{game_id}_preorder")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_games")],
    ])

    await query.edit_message_text(
        text="📦 وضعیت موجودی را انتخاب کنید:",
        reply_markup=markup,
    )


async def admin_set_stock_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle set stock status"""
    query = update.callback_query
    await query.answer()

    parts = query.data.split("_")
    game_id = int(parts[2])
    stock = parts[3]

    async with async_session() as session:
        service = GameService(session)
        await service.update_game(game_id, stock_status=stock)

    stock_names = {"in_stock": "موجود", "out_of_stock": "ناموجود", "preorder": "پیش فروش"}
    await query.edit_message_text(
        text=f"✅ وضعیت موجودی بازی #{game_id} به «{stock_names.get(stock, stock)}» تغییر کرد.",
        reply_markup=get_admin_games_keyboard(),
    )
