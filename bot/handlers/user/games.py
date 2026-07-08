"""
Game browsing handlers
"""
from telegram import Update, InputMediaPhoto
from telegram.ext import ContextTypes

from bot.database import async_session
from bot.services.game_service import GameService
from bot.services.favorite_service import FavoriteService
from bot.keyboards.user_kb import (
    get_games_platform_keyboard,
    get_game_detail_keyboard,
    get_pagination_keyboard,
    get_main_menu_keyboard,
)
from bot.config.messages import get_games_list_message, get_game_detail_message, get_no_results_message
from bot.config.constants import GamePlatform, GameCategory

ITEMS_PER_PAGE = 8


async def games_xbox_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle Xbox games menu"""
    query = update.callback_query
    await query.answer()

    context.user_data["game_filter"] = {"platform": "xbox"}
    await _show_games(update, context, platform="xbox", page=1)


async def games_ps_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle PlayStation games menu"""
    query = update.callback_query
    await query.answer()

    context.user_data["game_filter"] = {"platform": "playstation"}
    await _show_games(update, context, platform="playstation", page=1)


async def games_list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle games list pagination"""
    query = update.callback_query
    await query.answer()

    data = query.data
    parts = data.split("_page_")
    page = int(parts[1]) if len(parts) > 1 else 1

    filters = context.user_data.get("game_filter", {})
    platform = filters.get("platform")
    category = filters.get("category")
    search = filters.get("search")

    await _show_games(update, context, platform=platform, category=category, search=search, page=page)


async def _show_games(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    platform: str | None = None,
    category: str | None = None,
    search: str | None = None,
    page: int = 1,
) -> None:
    """Show games list"""
    query = update.callback_query

    async with async_session() as session:
        service = GameService(session)

        total = await service.get_game_count(platform=platform, category=category, search=search)
        total_pages = max(1, (total + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)
        page = min(page, total_pages)

        games = await service.get_all_games(
            offset=(page - 1) * ITEMS_PER_PAGE,
            limit=ITEMS_PER_PAGE,
            platform=platform,
            category=category,
            search=search,
        )

    if not games:
        await query.edit_message_text(
            text=get_no_results_message(),
            reply_markup=get_main_menu_keyboard(),
            parse_mode="HTML",
        )
        return

    buttons = []
    for game in games:
        stock = "✅" if game.stock_status == "in_stock" else "⏳" if game.stock_status == "preorder" else "❌"
        price_text = f"{game.effective_price:,}"
        if game.discount_percent:
            price_text += f" (-{game.discount_percent}%)"
        buttons.append([
            {
                "text": f"{stock} {game.name} | {price_text} تومان",
                "callback_data": f"game_{game.id}",
            }
        ])

    # Pagination
    nav_row = []
    if page > 1:
        nav_row.append({"text": "◀️", "callback_data": f"games_page_{page - 1}"})
    nav_row.append({"text": f"📄 {page}/{total_pages}", "callback_data": "noop"})
    if page < total_pages:
        nav_row.append({"text": "▶️", "callback_data": f"games_page_{page + 1}"})
    buttons.append(nav_row)
    buttons.append([{"text": "🔙 بازگشت", "callback_data": "main_menu"}])

    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(b["text"], callback_data=b["callback_data"]) for b in row]
        if isinstance(row, list) and len(row) == 1 and False
        else [InlineKeyboardButton(b["text"], callback_data=b["callback_data"]) for b in ([row] if isinstance(row, dict) else row)]
        for row in buttons
    ])

    await query.edit_message_text(
        text=get_games_list_message(page, total),
        reply_markup=markup,
        parse_mode="HTML",
    )


async def game_detail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle game detail view"""
    query = update.callback_query
    await query.answer()

    game_id = int(query.data.split("_")[1])

    async with async_session() as session:
        game_service = GameService(session)
        fav_service = FavoriteService(session)

        game = await game_service.get_game(game_id)
        if not game:
            await query.edit_message_text(text="بازی یافت نشد.")
            return

        await game_service.increment_views(game_id)

        is_fav = False
        user_id = update.effective_user.id if update.effective_user else None
        if user_id:
            is_fav = await fav_service.is_favorite(user_id, game_id)

    text = get_game_detail_message(
        name=game.name,
        description=game.description or "توضیحاتی ثبت نشده",
        genre=game.category,
        platforms=game.platforms,
        version=game.version,
        price=game.price,
        discount_price=game.discount_price,
        discount_percent=game.discount_percent,
        stock=game.stock_display,
        age_rating=game.age_rating or "نامشخص",
        release_date=game.release_date or "نامشخص",
        views=game.views,
        sales=game.sales,
        meta_score=game.meta_score,
    )

    keyboard = get_game_detail_keyboard(game_id, is_fav)

    if game.image_url:
        try:
            await query.edit_message_media(
                media=InputMediaPhoto(media=game.image_url, caption=text, parse_mode="HTML"),
                reply_markup=keyboard,
            )
            return
        except Exception:
            pass

    await query.edit_message_text(
        text=text,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle category selection"""
    query = update.callback_query
    await query.answer()

    category = query.data.replace("cat_", "")
    context.user_data["game_filter"] = {"category": category}
    await _show_games(update, context, category=category, page=1)


async def platform_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle platform selection"""
    query = update.callback_query
    await query.answer()

    platform = query.data.replace("platform_", "")
    if platform == "all":
        platform = None
    context.user_data["game_filter"] = {"platform": platform}
    await _show_games(update, context, platform=platform, page=1)


async def new_games_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle new games"""
    query = update.callback_query
    await query.answer()

    async with async_session() as session:
        service = GameService(session)
        games = await service.get_new_games(limit=10)

    if not games:
        await query.edit_message_text(text="بازی جدیدی یافت نشد.", parse_mode="HTML")
        return

    buttons = []
    for game in games:
        buttons.append([{"text": f"🆕 {game.name} | {game.effective_price:,} تومان", "callback_data": f"game_{game.id}"}])
    buttons.append([{"text": "🔙 بازگشت", "callback_data": "main_menu"}])

    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(b["text"], callback_data=b["callback_data"]) for b in row]
        for row in buttons
    ])

    await query.edit_message_text(
        text="🆕 <b>بازی‌های جدید</b>\n\nجدیدترین بازی‌های اضافه شده:",
        reply_markup=markup,
        parse_mode="HTML",
    )


async def bestsellers_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle bestsellers"""
    query = update.callback_query
    await query.answer()

    async with async_session() as session:
        service = GameService(session)
        games = await service.get_bestsellers(limit=10)

    if not games:
        await query.edit_message_text(text="بازی‌ای یافت نشد.", parse_mode="HTML")
        return

    buttons = []
    for i, game in enumerate(games, 1):
        buttons.append([{"text": f"⭐ {i}. {game.name} | فروش: {game.sales}", "callback_data": f"game_{game.id}"}])
    buttons.append([{"text": "🔙 بازگشت", "callback_data": "main_menu"}])

    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(b["text"], callback_data=b["callback_data"]) for b in row]
        for row in buttons
    ])

    await query.edit_message_text(
        text="⭐ <b>پرفروش‌ترین‌ها</b>\n\nمحبوب‌ترین بازی‌ها:",
        reply_markup=markup,
        parse_mode="HTML",
    )


async def special_offers_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle special offers"""
    query = update.callback_query
    await query.answer()

    async with async_session() as session:
        service = GameService(session)
        games = await service.get_special_offers(limit=10)

    if not games:
        await query.edit_message_text(text="پیشنهاد ویژه‌ای یافت نشد.", parse_mode="HTML")
        return

    buttons = []
    for game in games:
        buttons.append([{"text": f"🔥 {game.name} | {game.discount_percent}% تخفیف | {game.effective_price:,} تومان", "callback_data": f"game_{game.id}"}])
    buttons.append([{"text": "🔙 بازگشت", "callback_data": "main_menu"}])

    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(b["text"], callback_data=b["callback_data"]) for b in row]
        for row in buttons
    ])

    await query.edit_message_text(
        text="🔥 <b>پیشنهادهای ویژه</b>\n\nبهترین تخفیف‌ها:",
        reply_markup=markup,
        parse_mode="HTML",
    )


async def discount_games_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle discount games"""
    query = update.callback_query
    await query.answer()

    async with async_session() as session:
        service = GameService(session)
        games = await service.get_special_offers(limit=10)

    if not games:
        await query.edit_message_text(text="بازی با تخفیف یافت نشد.", parse_mode="HTML")
        return

    buttons = []
    for game in games:
        buttons.append([{"text": f"💰 {game.name} | {game.discount_percent}% off | {game.effective_price:,}", "callback_data": f"game_{game.id}"}])
    buttons.append([{"text": "🔙 بازگشت", "callback_data": "main_menu"}])

    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(b["text"], callback_data=b["callback_data"]) for b in row]
        for row in buttons
    ])

    await query.edit_message_text(
        text="💰 <b>تخفیف‌ها</b>",
        reply_markup=markup,
        parse_mode="HTML",
    )
