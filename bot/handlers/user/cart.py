"""
Cart and checkout handlers
"""
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.database import async_session
from bot.services.cart_service import CartService
from bot.services.game_service import GameService
from bot.services.order_service import OrderService
from bot.services.wallet_service import WalletService
from bot.services.discount_service import DiscountService
from bot.keyboards.user_kb import get_cart_keyboard, get_main_menu_keyboard, get_payment_keyboard
from bot.config.messages import get_cart_message, get_error_message


async def cart_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle cart view"""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id

    async with async_session() as session:
        cart_service = CartService(session)
        items = await cart_service.get_cart_items(user_id)
        total = await cart_service.get_cart_total(user_id)

    tax = int(total * 0.09)  # 9% tax
    grand_total = total + tax

    text = get_cart_message(
        items=items,
        total=total,
        tax=tax,
        grand_total=grand_total,
    )

    await query.edit_message_text(
        text=text,
        reply_markup=get_cart_keyboard(has_items=bool(items)),
        parse_mode="HTML",
    )


async def add_to_cart_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle add to cart"""
    query = update.callback_query
    await query.answer("✅ به سبد اضافه شد")

    game_id = int(query.data.split("_")[2])
    user_id = update.effective_user.id

    async with async_session() as session:
        game_service = GameService(session)
        game = await game_service.get_game(game_id)

        if not game or game.stock_status != "in_stock":
            await query.answer("❌ محصول موجود نیست", show_alert=True)
            return

        cart_service = CartService(session)
        await cart_service.add_item(user_id, game_id)


async def remove_from_cart_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle remove from cart"""
    query = update.callback_query
    await query.answer("🗑️ از سبد حذف شد")

    game_id = int(query.data.split("_")[2])
    user_id = update.effective_user.id

    async with async_session() as session:
        cart_service = CartService(session)
        await cart_service.remove_item(user_id, game_id)


async def increase_cart_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle increase cart item quantity"""
    query = update.callback_query
    await query.answer()

    game_id = int(query.data.split("_")[3])
    user_id = update.effective_user.id

    async with async_session() as session:
        cart_service = CartService(session)
        await cart_service.increase_quantity(user_id, game_id)


async def decrease_cart_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle decrease cart item quantity"""
    query = update.callback_query
    await query.answer()

    game_id = int(query.data.split("_")[3])
    user_id = update.effective_user.id

    async with async_session() as session:
        cart_service = CartService(session)
        await cart_service.decrease_quantity(user_id, game_id)


async def clear_cart_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle clear cart"""
    query = update.callback_query
    await query.answer("🗑️ سبد خالی شد")

    user_id = update.effective_user.id

    async with async_session() as session:
        cart_service = CartService(session)
        await cart_service.clear_cart(user_id)

    from bot.keyboards.user_kb import get_back_keyboard
    await query.edit_message_text(
        text="🛒 سبد خرید شما خالی شد.",
        reply_markup=get_back_keyboard("main_menu"),
        parse_mode="HTML",
    )


async def checkout_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle checkout"""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id

    async with async_session() as session:
        cart_service = CartService(session)
        items = await cart_service.get_cart_items(user_id)

        if not items:
            await query.edit_message_text(
                text="🛒 سبد خرید شما خالی است.",
                reply_markup=get_main_menu_keyboard(),
                parse_mode="HTML",
            )
            return

        total = await cart_service.get_cart_total(user_id)
        tax = int(total * 0.09)
        grand_total = total + tax

        # Create order
        order_service = OrderService(session)
        order_items = [
            {"game_id": item["game_id"], "quantity": item["quantity"], "price": item["unit_price"]}
            for item in items
        ]
        order = await order_service.create_order(
            user_id=user_id,
            items=order_items,
            total_amount=total,
            tax_amount=tax,
            final_amount=grand_total,
        )

        # Clear cart
        await cart_service.clear_cart(user_id)

    from bot.config.messages import get_order_placed_message

    await query.edit_message_text(
        text=get_order_placed_message(order.id, grand_total),
        reply_markup=get_payment_keyboard(order.id),
        parse_mode="HTML",
    )


async def pay_wallet_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle wallet payment"""
    query = update.callback_query

    order_id = int(query.data.split("_")[2])
    user_id = update.effective_user.id

    async with async_session() as session:
        order_service = OrderService(session)
        wallet_service = WalletService(session)
        game_service = GameService(session)

        order = await order_service.get_order(order_id)
        if not order:
            await query.answer("❌ سفارش یافت نشد", show_alert=True)
            return

        balance = await wallet_service.get_balance(user_id)
        if balance < order.final_amount:
            await query.answer(
                f"❌ موجودی کافی نیست.\nموجودی: {balance:,} تومان\nمبلغ مورد نیاز: {order.final_amount:,} تومان",
                show_alert=True,
            )
            return

        # Deduct from wallet
        await wallet_service.deduct(
            user_id,
            order.final_amount,
            f"پرداخت سفارش #{order_id}",
        )

        # Update order status
        await order_service.update_order_status(order_id, "checking")

        # Update game sales
        for item in order.items:
            await game_service.increment_sales(item.game_id, item.quantity)

        # Update user purchase count
        from bot.services.user_service import UserService
        user_service = UserService(session)
        await user_service.increment_purchase_count(user_id)

    from bot.config.messages import get_order_confirmed_message

    await query.edit_message_text(
        text=get_order_confirmed_message(order_id),
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )


async def pay_card_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle card to card payment"""
    query = update.callback_query
    await query.answer()

    from bot.config.settings import Config

    order_id = int(query.data.split("_")[2])

    await query.edit_message_text(
        text=(
            f"💳 <b>پرداخت کارت به کارت</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"شماره کارت: <code>{Config.STORE_CARD_NUMBER}</code>\n"
            f"به نام: {Config.STORE_CARD_HOLDER}\n"
            f"بانک: {Config.STORE_CARD_BANK}\n\n"
            f"لطفاً مبلغ را واریز کرده و رسید را ارسال کنید.\n"
            f"شماره سفارش: #{order_id}\n\n"
            f"⏳ پس از تأیید مدیر، سفارش شما پردازش خواهد شد."
        ),
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )


async def cancel_order_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle cancel order"""
    query = update.callback_query
    await query.answer()

    order_id = int(query.data.split("_")[2])

    async with async_session() as session:
        order_service = OrderService(session)
        await order_service.update_order_status(order_id, "cancelled")

    from bot.config.messages import get_order_cancelled_message

    await query.edit_message_text(
        text=get_order_cancelled_message(order_id),
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )
