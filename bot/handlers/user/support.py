"""
Support and ticket handlers
"""
from telegram import Update
from telegram.ext import ContextTypes

from bot.database import async_session
from bot.services.ticket_service import TicketService
from bot.keyboards.user_kb import get_support_keyboard, get_main_menu_keyboard, get_back_keyboard
from bot.config.messages import get_support_message


async def support_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle support menu"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text=get_support_message(),
        reply_markup=get_support_keyboard(),
        parse_mode="HTML",
    )


async def new_ticket_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle new ticket"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text="📝 <b>تیکت جدید</b>\n\nپیام خود را ارسال کنید:",
        reply_markup=get_back_keyboard("support"),
        parse_mode="HTML",
    )
    context.user_data["waiting_for"] = "ticket_message"


async def ticket_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle ticket message"""
    if context.user_data.get("waiting_for") != "ticket_message":
        return

    user_id = update.effective_user.id
    message = update.message.text
    context.user_data["waiting_for"] = None

    async with async_session() as session:
        service = TicketService(session)
        ticket = await service.create_ticket(user_id)
        await service.add_message(ticket.id, user_id, message)

    await update.message.reply_text(
        text=f"✅ تیکت #{ticket.id} ثبت شد.\nپشتیبانان ما به زودی پاسخ خواهند داد.",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )


async def ticket_history_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle ticket history"""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id

    async with async_session() as session:
        service = TicketService(session)
        tickets = await service.get_user_tickets(user_id)

    text = "📜 <b>تاریخچه تیکت‌ها</b>\n━━━━━━━━━━━━━━━━━━━━━━\n\n"

    if not tickets:
        text += "تیکتی ثبت نکرده‌اید."
    else:
        for ticket in tickets:
            status = "🟢 باز" if ticket.status == "open" else "🔴 بسته"
            text += (
                f"📦 تیکت #{ticket.id}\n"
                f"📌 وضعیت: {status}\n"
                f"📅 {ticket.created_at.strftime('%Y/%m/%d') if ticket.created_at else ''}\n\n"
            )

    await query.edit_message_text(
        text=text,
        reply_markup=get_back_keyboard("support"),
        parse_mode="HTML",
    )
