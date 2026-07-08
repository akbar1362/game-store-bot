"""
Orders handler
"""
from telegram import Update
from telegram.ext import ContextTypes

from bot.database import async_session
from bot.services.order_service import OrderService
from bot.keyboards.user_kb import get_main_menu_keyboard
from bot.config.messages import get_orders_message
from bot.config.constants import OrderStatus


async def orders_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle orders list"""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id

    async with async_session() as session:
        service = OrderService(session)
        orders = await service.get_user_orders(user_id, limit=20)

    orders_data = []
    for order in orders:
        status = OrderStatus(order.status).display_name
        orders_data.append({
            "id": order.id,
            "date": order.created_at.strftime("%Y/%m/%d") if order.created_at else "نامشخص",
            "total": order.final_amount,
            "status": status,
        })

    text = get_orders_message(orders_data)

    await query.edit_message_text(
        text=text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )
