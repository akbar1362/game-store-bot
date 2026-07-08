"""
Admin order management handlers
"""
from telegram import Update
from telegram.ext import ContextTypes

from bot.database import async_session
from bot.services.order_service import OrderService
from bot.keyboards.admin_kb import (
    get_admin_panel_keyboard,
    get_admin_orders_keyboard,
    get_admin_order_detail_keyboard,
)
from bot.keyboards.user_kb import get_back_keyboard
from bot.config.constants import OrderStatus


async def admin_orders_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle admin orders menu"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text="📦 <b>مدیریت سفارش‌ها</b>\n\nوضعیت سفارش را انتخاب کنید:",
        reply_markup=get_admin_orders_keyboard(),
        parse_mode="HTML",
    )


async def admin_orders_list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle orders list by status"""
    query = update.callback_query
    await query.answer()

    status = query.data.replace("admin_orders_", "")

    async with async_session() as session:
        service = OrderService(session)
        orders = await service.get_orders_by_status(status, limit=20)

    status_name = OrderStatus(status).display_name if status in ["pending", "checking", "shipped", "delivered", "cancelled"] else status

    text = f"📦 <b>سفارش‌ها ({status_name})</b>\n━━━━━━━━━━━━━━━━━━━━━━\n\n"

    if not orders:
        text += "سفارشی یافت نشد."
    else:
        for order in orders:
            text += (
                f"📦 سفارش #{order.id}\n"
                f"👤 کاربر: {order.user_id}\n"
                f"💰 مبلغ: {order.final_amount:,} تومان\n"
                f"📅 {order.created_at.strftime('%Y/%m/%d') if order.created_at else ''}\n\n"
            )

    buttons = []
    for order in orders[:10]:
        buttons.append([{"text": f"📦 سفارش #{order.id}", "callback_data": f"admin_order_{order.id}"}])
    buttons.append([{"text": "🔙 بازگشت", "callback_data": "admin_orders"}])

    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(b["text"], callback_data=b["callback_data"]) for b in row]
        for row in buttons
    ])

    await query.edit_message_text(
        text=text,
        reply_markup=markup,
        parse_mode="HTML",
    )


async def admin_order_detail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle order detail view"""
    query = update.callback_query
    await query.answer()

    order_id = int(query.data.split("_")[-1])

    async with async_session() as session:
        service = OrderService(session)
        order = await service.get_order(order_id)

    if not order:
        await query.answer("❌ سفارش یافت نشد", show_alert=True)
        return

    status = OrderStatus(order.status).display_name

    text = (
        f"📦 <b>جزئیات سفارش #{order.id}</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 کاربر: {order.user_id}\n"
        f"💰 جمع کل: {order.total_amount:,} تومان\n"
        f"📊 مالیات: {order.tax_amount:,} تومان\n"
        f"🔥 تخفیف: {order.discount_amount:,} تومان\n"
        f"💳 مبلغ نهایی: {order.final_amount:,} تومان\n"
        f"📌 وضعیت: {status}\n"
        f"📅 تاریخ: {order.created_at.strftime('%Y/%m/%d %H:%M') if order.created_at else ''}\n\n"
    )

    if order.items:
        text += "<b>اقلام سفارش:</b>\n"
        for item in order.items:
            text += f"  🎮 بازی #{item.game_id} x{item.quantity} | {item.price:,} تومان\n"

    await query.edit_message_text(
        text=text,
        reply_markup=get_admin_order_detail_keyboard(order.id),
        parse_mode="HTML",
    )


async def admin_order_action_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle order status change"""
    query = update.callback_query
    await query.answer()

    parts = query.data.split("_")
    action = parts[3]  # confirm, ship, deliver, cancel
    order_id = int(parts[4])

    status_map = {
        "confirm": "checking",
        "ship": "shipped",
        "deliver": "delivered",
        "cancel": "cancelled",
    }

    new_status = status_map.get(action)
    if not new_status:
        return

    async with async_session() as session:
        service = OrderService(session)
        await service.update_order_status(order_id, new_status)

    # Send notification to user
    order = await service.get_order(order_id)
    if order:
        from bot.config.messages import (
            get_order_confirmed_message,
            get_order_shipped_message,
            get_order_delivered_message,
            get_order_cancelled_message,
        )

        notification_map = {
            "checking": get_order_confirmed_message(order_id),
            "shipped": get_order_shipped_message(order_id),
            "delivered": get_order_delivered_message(order_id),
            "cancelled": get_order_cancelled_message(order_id),
        }

        try:
            await context.bot.send_message(
                chat_id=order.user_id,
                text=notification_map.get(new_status, ""),
                parse_mode="HTML",
            )
        except Exception:
            pass

    from bot.config.constants import OrderStatus
    status_name = OrderStatus(new_status).display_name
    await query.edit_message_text(
        text=f"✅ وضعیت سفارش #{order_id} به «{status_name}» تغییر کرد.",
        reply_markup=get_admin_orders_keyboard(),
    )
