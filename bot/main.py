"""
Main application entry point
Supports both polling mode and web server integration
"""
import asyncio
import logging
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from bot.config.settings import Config
from bot.database import init_db, close_db
from bot.utils import setup_logging
from bot.middlewares import rate_limit_middleware, logging_middleware

# User handlers
from bot.handlers.user.start import start_handler, enter_store_handler
from bot.handlers.user.menu import main_menu_handler
from bot.handlers.user.games import (
    games_xbox_handler,
    games_ps_handler,
    game_detail_handler,
    games_list_handler,
    category_handler,
    platform_handler,
    new_games_handler,
    bestsellers_handler,
    special_offers_handler,
    discount_games_handler,
)
from bot.handlers.user.cart import (
    cart_handler,
    add_to_cart_handler,
    remove_from_cart_handler,
    increase_cart_handler,
    decrease_cart_handler,
    clear_cart_handler,
    checkout_handler,
    pay_wallet_handler,
    pay_card_handler,
    cancel_order_handler,
)
from bot.handlers.user.profile import (
    profile_handler,
    wallet_handler,
    wallet_topup_handler,
    wallet_amount_handler,
    wallet_history_handler,
    wallet_custom_amount_handler,
)
from bot.handlers.user.orders import orders_handler
from bot.handlers.user.favorites import (
    favorites_handler,
    add_favorite_handler,
    remove_favorite_handler,
)
from bot.handlers.user.search import search_handler, search_text_handler
from bot.handlers.user.support import (
    support_handler,
    new_ticket_handler,
    ticket_message_handler,
    ticket_history_handler,
)
from bot.handlers.user.misc import (
    contact_handler,
    about_handler,
    discount_code_handler,
    discount_code_text_handler,
    review_handler,
    rate_handler,
    share_handler,
)

# Admin handlers
from bot.handlers.admin.panel import (
    admin_panel_handler,
    exit_admin_handler,
    admin_stats_handler,
)
from bot.handlers.admin.games import (
    admin_games_handler,
    admin_add_game_handler,
    admin_list_games_handler,
    admin_edit_game_handler,
    admin_delete_game_handler,
    admin_confirm_delete_game_handler,
    admin_game_name_handler,
    admin_game_price_handler,
    admin_game_desc_handler,
    admin_game_category_handler,
    admin_game_platform_handler,
    admin_game_version_handler,
    admin_game_image_handler,
    admin_game_discount_handler,
    admin_game_age_handler,
    admin_game_date_handler,
    admin_edit_game_price_handler,
    admin_edit_game_stock_handler,
    admin_set_stock_handler,
)
from bot.handlers.admin.users import (
    admin_users_handler,
    admin_list_users_handler,
    admin_search_user_handler,
    admin_search_user_text_handler,
    admin_broadcast_handler,
    admin_broadcast_text_handler,
    admin_broadcast_text_input_handler,
    admin_confirm_broadcast_handler,
)
from bot.handlers.admin.orders import (
    admin_orders_handler,
    admin_orders_list_handler,
    admin_order_detail_handler,
    admin_order_action_handler,
)
from bot.handlers.admin.discount import (
    admin_discounts_handler,
    admin_add_discount_handler,
    admin_add_discount_code_handler,
    admin_add_discount_type_handler,
    admin_add_discount_value_handler,
    admin_add_discount_min_handler,
    admin_add_discount_max_handler,
    admin_add_discount_expiry_handler,
    admin_list_discounts_handler,
)
from bot.handlers.admin.reports import admin_reports_handler, report_handler
from bot.handlers.admin.settings import (
    admin_settings_handler,
    admin_set_name_handler,
    admin_set_name_text_handler,
    admin_set_card_handler,
    admin_set_card_text_handler,
    admin_toggle_handler,
)

logger = logging.getLogger(__name__)

# Global application reference
_application: Application | None = None


def build_application() -> Application:
    """Build and configure the telegram application"""
    global _application

    if _application is not None:
        return _application

    setup_logging()
    logger.info("Building Game Store Bot application...")

    application = Application.builder().token(Config.BOT_TOKEN).build()

    # ============ Command Handlers ============
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("admin", admin_panel_handler))

    # ============ Callback Query Handlers ============

    # Welcome / Store entry
    application.add_handler(CallbackQueryHandler(enter_store_handler, pattern=r"^enter_store$"))

    # Main menu
    application.add_handler(CallbackQueryHandler(main_menu_handler, pattern=r"^main_menu$"))

    # Games - Xbox / PlayStation
    application.add_handler(CallbackQueryHandler(games_xbox_handler, pattern=r"^games_xbox$"))
    application.add_handler(CallbackQueryHandler(games_ps_handler, pattern=r"^games_ps$"))
    application.add_handler(CallbackQueryHandler(new_games_handler, pattern=r"^new_games$"))
    application.add_handler(CallbackQueryHandler(bestsellers_handler, pattern=r"^bestsellers$"))
    application.add_handler(CallbackQueryHandler(special_offers_handler, pattern=r"^special_offers$"))
    application.add_handler(CallbackQueryHandler(discount_games_handler, pattern=r"^discount_games$"))

    # Game detail
    application.add_handler(CallbackQueryHandler(game_detail_handler, pattern=r"^game_\d+$"))

    # Games list pagination
    application.add_handler(CallbackQueryHandler(games_list_handler, pattern=r"^games_page_"))

    # Category / Platform filters
    application.add_handler(CallbackQueryHandler(category_handler, pattern=r"^cat_\w+$"))
    application.add_handler(CallbackQueryHandler(platform_handler, pattern=r"^platform_\w+$"))

    # Cart
    application.add_handler(CallbackQueryHandler(cart_handler, pattern=r"^cart$"))
    application.add_handler(CallbackQueryHandler(add_to_cart_handler, pattern=r"^buy_\d+$"))
    application.add_handler(CallbackQueryHandler(remove_from_cart_handler, pattern=r"^cart_remove_\d+$"))
    application.add_handler(CallbackQueryHandler(increase_cart_handler, pattern=r"^cart_increase_\d+$"))
    application.add_handler(CallbackQueryHandler(decrease_cart_handler, pattern=r"^cart_decrease_\d+$"))
    application.add_handler(CallbackQueryHandler(clear_cart_handler, pattern=r"^clear_cart$"))
    application.add_handler(CallbackQueryHandler(checkout_handler, pattern=r"^checkout$"))

    # Payment
    application.add_handler(CallbackQueryHandler(pay_wallet_handler, pattern=r"^pay_wallet_\d+$"))
    application.add_handler(CallbackQueryHandler(pay_card_handler, pattern=r"^pay_card_\d+$"))
    application.add_handler(CallbackQueryHandler(cancel_order_handler, pattern=r"^cancel_order_\d+$"))

    # Profile / Wallet
    application.add_handler(CallbackQueryHandler(profile_handler, pattern=r"^profile$"))
    application.add_handler(CallbackQueryHandler(wallet_handler, pattern=r"^wallet$"))
    application.add_handler(CallbackQueryHandler(wallet_topup_handler, pattern=r"^wallet_topup$"))
    application.add_handler(CallbackQueryHandler(wallet_amount_handler, pattern=r"^wallet_amount_"))
    application.add_handler(CallbackQueryHandler(wallet_history_handler, pattern=r"^wallet_history$"))

    # Orders
    application.add_handler(CallbackQueryHandler(orders_handler, pattern=r"^orders$"))

    # Favorites
    application.add_handler(CallbackQueryHandler(favorites_handler, pattern=r"^favorites$"))
    application.add_handler(CallbackQueryHandler(add_favorite_handler, pattern=r"^add_fav_\d+$"))
    application.add_handler(CallbackQueryHandler(remove_favorite_handler, pattern=r"^remove_fav_\d+$"))

    # Search
    application.add_handler(CallbackQueryHandler(search_handler, pattern=r"^search$"))

    # Support
    application.add_handler(CallbackQueryHandler(support_handler, pattern=r"^support$"))
    application.add_handler(CallbackQueryHandler(new_ticket_handler, pattern=r"^new_ticket$"))
    application.add_handler(CallbackQueryHandler(ticket_history_handler, pattern=r"^ticket_history$"))

    # Misc
    application.add_handler(CallbackQueryHandler(contact_handler, pattern=r"^contact$"))
    application.add_handler(CallbackQueryHandler(about_handler, pattern=r"^about$"))
    application.add_handler(CallbackQueryHandler(discount_code_handler, pattern=r"^discount_code$"))

    # Reviews
    application.add_handler(CallbackQueryHandler(review_handler, pattern=r"^review_\d+$"))
    application.add_handler(CallbackQueryHandler(rate_handler, pattern=r"^rate_\d+_\d+$"))
    application.add_handler(CallbackQueryHandler(share_handler, pattern=r"^share_\d+$"))

    # ============ Admin Callback Handlers ============
    application.add_handler(CallbackQueryHandler(admin_panel_handler, pattern=r"^admin_panel$"))
    application.add_handler(CallbackQueryHandler(exit_admin_handler, pattern=r"^exit_admin$"))
    application.add_handler(CallbackQueryHandler(admin_stats_handler, pattern=r"^admin_stats$"))

    # Admin Games
    application.add_handler(CallbackQueryHandler(admin_games_handler, pattern=r"^admin_games$"))
    application.add_handler(CallbackQueryHandler(admin_add_game_handler, pattern=r"^admin_add_game$"))
    application.add_handler(CallbackQueryHandler(admin_list_games_handler, pattern=r"^admin_list_games$"))
    application.add_handler(CallbackQueryHandler(admin_edit_game_handler, pattern=r"^admin_edit_game_\d+$"))
    application.add_handler(CallbackQueryHandler(admin_delete_game_handler, pattern=r"^admin_delete_game_\d+$"))
    application.add_handler(CallbackQueryHandler(admin_confirm_delete_game_handler, pattern=r"^admin_confirm_delete_game_\d+$"))
    application.add_handler(CallbackQueryHandler(admin_edit_game_price_handler, pattern=r"^admin_edit_game_price_\d+$"))
    application.add_handler(CallbackQueryHandler(admin_edit_game_stock_handler, pattern=r"^admin_edit_game_stock_\d+$"))
    application.add_handler(CallbackQueryHandler(admin_set_stock_handler, pattern=r"^set_stock_\d+_\w+$"))

    # Admin Users
    application.add_handler(CallbackQueryHandler(admin_users_handler, pattern=r"^admin_users$"))
    application.add_handler(CallbackQueryHandler(admin_list_users_handler, pattern=r"^admin_list_users$"))
    application.add_handler(CallbackQueryHandler(admin_broadcast_handler, pattern=r"^admin_broadcast$"))
    application.add_handler(CallbackQueryHandler(admin_broadcast_text_handler, pattern=r"^broadcast_text$"))
    application.add_handler(CallbackQueryHandler(admin_confirm_broadcast_handler, pattern=r"^admin_confirm_broadcast$"))

    # Admin Orders
    application.add_handler(CallbackQueryHandler(admin_orders_handler, pattern=r"^admin_orders$"))
    application.add_handler(CallbackQueryHandler(admin_orders_list_handler, pattern=r"^admin_orders_\w+$"))
    application.add_handler(CallbackQueryHandler(admin_order_detail_handler, pattern=r"^admin_order_\d+$"))
    application.add_handler(CallbackQueryHandler(admin_order_action_handler, pattern=r"^admin_order_(confirm|ship|deliver|cancel)_\d+$"))

    # Admin Discounts
    application.add_handler(CallbackQueryHandler(admin_discounts_handler, pattern=r"^admin_discounts$"))
    application.add_handler(CallbackQueryHandler(admin_add_discount_handler, pattern=r"^admin_add_discount$"))
    application.add_handler(CallbackQueryHandler(admin_list_discounts_handler, pattern=r"^admin_list_discounts$"))

    # Admin Reports
    application.add_handler(CallbackQueryHandler(admin_reports_handler, pattern=r"^admin_reports$"))
    application.add_handler(CallbackQueryHandler(report_handler, pattern=r"^report_\w+$"))

    # Admin Settings
    application.add_handler(CallbackQueryHandler(admin_settings_handler, pattern=r"^admin_settings$"))
    application.add_handler(CallbackQueryHandler(admin_set_name_handler, pattern=r"^admin_set_name$"))
    application.add_handler(CallbackQueryHandler(admin_set_card_handler, pattern=r"^admin_set_card$"))
    application.add_handler(CallbackQueryHandler(admin_toggle_handler, pattern=r"^admin_toggle$"))

    # Admin other sections (placeholder)
    application.add_handler(CallbackQueryHandler(
        lambda u, c: u.callback_query.answer("Coming soon", show_alert=True),
        pattern=r"^admin_(messages|banners|notifications|reviews|inventory|wallet|logs)$"
    ))

    # ============ Message Router (must be last) ============
    async def text_router(update, context):
        if not update.message or not update.message.text:
            return
        state = context.user_data.get("waiting_for") or context.user_data.get("admin_state")
        if not await rate_limit_middleware(update, context):
            return
        await logging_middleware(update, context)

        # Admin states
        admin_state_map = {
            "add_game_name": lambda: admin_game_name_handler(update, context, update.message.text),
            "add_game_price": lambda: admin_game_price_handler(update, context, update.message.text),
            "add_game_desc": lambda: admin_game_desc_handler(update, context, update.message.text),
            "add_game_category": lambda: admin_game_category_handler(update, context, update.message.text),
            "add_game_platform": lambda: admin_game_platform_handler(update, context, update.message.text),
            "add_game_version": lambda: admin_game_version_handler(update, context, update.message.text),
            "add_game_image": lambda: admin_game_image_handler(update, context, update.message.text),
            "add_game_discount": lambda: admin_game_discount_handler(update, context, update.message.text),
            "add_game_age": lambda: admin_game_age_handler(update, context, update.message.text),
            "add_game_date": lambda: admin_game_date_handler(update, context, update.message.text),
            "set_store_name": lambda: admin_set_name_text_handler(update, context, update.message.text),
            "set_card_number": lambda: admin_set_card_text_handler(update, context, update.message.text),
            "search_user": lambda: admin_search_user_text_handler(update, context, update.message.text),
            "broadcast_text": lambda: admin_broadcast_text_input_handler(update, context, update.message.text),
        }

        user_state_map = {
            "search": lambda: search_text_handler(update, context),
            "ticket_message": lambda: ticket_message_handler(update, context),
            "discount_code": lambda: discount_code_text_handler(update, context),
            "wallet_custom_amount": lambda: wallet_custom_amount_handler(update, context),
        }

        if state in admin_state_map:
            if state == "edit_game_price":
                from bot.database import async_session
                from bot.services.game_service import GameService
                game_id = context.user_data.get("editing_game_id")
                if game_id:
                    try:
                        price = int(update.message.text.replace(",", ""))
                        async with async_session() as session:
                            svc = GameService(session)
                            await svc.update_game(game_id, price=price)
                        await update.message.reply_text(f"قیمت بازی #{game_id} به {price:,} تومان تغییر کرد.")
                    except ValueError:
                        await update.message.reply_text("لطفاً یک عدد صحیح وارد کنید.")
                context.user_data["admin_state"] = None
            else:
                await admin_state_map[state]()
        elif state in user_state_map:
            await user_state_map[state]()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_router))

    # Error handler
    async def error_handler(update, context):
        logger.error(f"Exception while handling an update: {context.error}")

    application.add_error_handler(error_handler)

    _application = application
    return application


async def init_database():
    """Initialize the database"""
    await init_db()


def main() -> None:
    """Main function to run the bot in polling mode"""
    setup_logging()
    logger.info("Starting Game Store Bot in polling mode...")

    application = build_application()

    # Initialize database
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(init_database())

    # Run the bot
    logger.info("Bot is running in polling mode...")
    application.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
