"""
Admin handlers package
"""
from bot.handlers.admin.panel import admin_panel_handler, exit_admin_handler
from bot.handlers.admin.games import (
    admin_games_handler,
    admin_add_game_handler,
    admin_list_games_handler,
    admin_edit_game_handler,
    admin_delete_game_handler,
)
from bot.handlers.admin.users import (
    admin_users_handler,
    admin_list_users_handler,
    admin_broadcast_handler,
)
from bot.handlers.admin.orders import (
    admin_orders_handler,
    admin_order_detail_handler,
    admin_order_action_handler,
)
from bot.handlers.admin.discount import (
    admin_discounts_handler,
    admin_add_discount_handler,
)
from bot.handlers.admin.reports import admin_reports_handler
from bot.handlers.admin.settings import admin_settings_handler
