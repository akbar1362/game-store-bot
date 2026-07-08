"""
User handlers package
"""
from bot.handlers.user.start import start_handler, enter_store_handler
from bot.handlers.user.menu import main_menu_handler
from bot.handlers.user.games import (
    games_xbox_handler,
    games_ps_handler,
    game_detail_handler,
    games_list_handler,
)
from bot.handlers.user.cart import (
    cart_handler,
    add_to_cart_handler,
    remove_from_cart_handler,
    increase_cart_handler,
    decrease_cart_handler,
    clear_cart_handler,
    checkout_handler,
)
from bot.handlers.user.profile import profile_handler, wallet_handler
from bot.handlers.user.orders import orders_handler
from bot.handlers.user.favorites import favorites_handler
from bot.handlers.user.search import search_handler
from bot.handlers.user.support import support_handler
from bot.handlers.user.misc import contact_handler, about_handler, discount_code_handler
