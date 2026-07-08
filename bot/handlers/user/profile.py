"""
Profile and wallet handlers
"""
from telegram import Update
from telegram.ext import ContextTypes

from bot.database import async_session
from bot.services.user_service import UserService
from bot.services.wallet_service import WalletService
from bot.keyboards.user_kb import get_profile_keyboard, get_wallet_keyboard, get_wallet_amount_keyboard, get_back_keyboard
from bot.config.messages import get_profile_message, get_wallet_message


async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle profile view"""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id

    async with async_session() as session:
        service = UserService(session)
        user = await service.get_user(user_id)

        if not user:
            await query.edit_message_text(text="خطایی رخ داده است.")
            return

    text = get_profile_message(
        name=user.first_name or user.username or "نامشخص",
        phone=user.phone or "ثبت نشده",
        user_id=user.telegram_id,
        join_date=user.created_at.strftime("%Y/%m/%d") if user.created_at else "نامشخص",
        points=user.points,
        purchases=user.purchase_count,
        wallet=user.wallet_balance,
    )

    await query.edit_message_text(
        text=text,
        reply_markup=get_profile_keyboard(),
        parse_mode="HTML",
    )


async def wallet_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle wallet view"""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id

    async with async_session() as session:
        wallet_service = WalletService(session)
        balance = await wallet_service.get_balance(user_id)

    text = get_wallet_message(balance)

    await query.edit_message_text(
        text=text,
        reply_markup=get_wallet_keyboard(),
        parse_mode="HTML",
    )


async def wallet_topup_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle wallet top-up"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text="💰 <b>افزایش موجودی</b>\n\nمبلغ مورد نظر را انتخاب کنید:",
        reply_markup=get_wallet_amount_keyboard(),
        parse_mode="HTML",
    )


async def wallet_amount_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle wallet top-up amount selection"""
    query = update.callback_query
    await query.answer()

    amount_str = query.data.replace("wallet_amount_", "")

    if amount_str == "custom":
        await query.edit_message_text(
            text="💰 مبلغ مورد نظر را به تومان وارد کنید:",
            reply_markup=get_back_keyboard("wallet"),
        )
        context.user_data["waiting_for"] = "wallet_custom_amount"
        return

    amount = int(amount_str)
    user_id = update.effective_user.id

    from bot.config.settings import Config

    await query.edit_message_text(
        text=(
            f"💰 <b>افزایش موجودی</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"مبلغ: <b>{amount:,} تومان</b>\n\n"
            f"💳 شماره کارت: <code>{Config.STORE_CARD_NUMBER}</code>\n"
            f"👤 به نام: {Config.STORE_CARD_HOLDER}\n"
            f"🏦 بانک: {Config.STORE_CARD_BANK}\n\n"
            f"لطفاً مبلغ را واریز کرده و رسید را ارسال کنید."
        ),
        reply_markup=get_back_keyboard("wallet"),
        parse_mode="HTML",
    )


async def wallet_history_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle wallet history"""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id

    async with async_session() as session:
        wallet_service = WalletService(session)
        transactions = await wallet_service.get_transactions(user_id, limit=10)

    type_names = {
        "deposit": "💰 افزایش",
        "withdrawal": "💸 برداشت",
        "purchase": "🛒 خرید",
        "refund": "🔄 بازگشت",
        "bonus": "🎁 پاداش",
    }

    text = "📜 <b>تاریخچه تراکنش</b>\n━━━━━━━━━━━━━━━━━━━━━━\n\n"

    if not transactions:
        text += "تراکنشی ثبت نشده است."
    else:
        for tx in transactions:
            tx_type = type_names.get(tx.transaction_type, tx.transaction_type)
            text += (
                f"{tx_type}\n"
                f"💰 مبلغ: {tx.amount:,} تومان\n"
                f"📝 {tx.description or ''}\n"
                f"📅 {tx.created_at.strftime('%Y/%m/%d %H:%M') if tx.created_at else ''}\n\n"
            )

    await query.edit_message_text(
        text=text,
        reply_markup=get_back_keyboard("wallet"),
        parse_mode="HTML",
    )


async def wallet_custom_amount_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle custom wallet top-up amount"""
    if context.user_data.get("waiting_for") != "wallet_custom_amount":
        return

    try:
        amount = int(update.message.text.replace(",", "").replace("،", ""))
    except ValueError:
        await update.message.reply_text("❌ لطفاً یک عدد صحیح وارد کنید.")
        return

    if amount < 10000:
        await update.message.reply_text("❌ حداقل مبلغ ۱۰,۰۰۰ تومان است.")
        return

    context.user_data["waiting_for"] = None

    from bot.config.settings import Config

    await update.message.reply_text(
        text=(
            f"💰 <b>افزایش موجودی</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"مبلغ: <b>{amount:,} تومان</b>\n\n"
            f"💳 شماره کارت: <code>{Config.STORE_CARD_NUMBER}</code>\n"
            f"👤 به نام: {Config.STORE_CARD_HOLDER}\n"
            f"🏦 بانک: {Config.STORE_CARD_BANK}\n\n"
            f"لطفاً مبلغ را واریز کرده و رسید را ارسال کنید."
        ),
        reply_markup=get_back_keyboard("wallet"),
        parse_mode="HTML",
    )
