"""
Admin reports handlers
"""
from telegram import Update
from telegram.ext import ContextTypes

from bot.database import async_session
from bot.services.admin_service import AdminService
from bot.keyboards.admin_kb import get_admin_reports_keyboard, get_admin_panel_keyboard
from bot.keyboards.user_kb import get_back_keyboard


async def admin_reports_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle admin reports"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text="📈 <b>گزارش‌ها</b>\n\nنوع گزارش را انتخاب کنید:",
        reply_markup=get_admin_reports_keyboard(),
        parse_mode="HTML",
    )


async def report_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle specific report"""
    query = update.callback_query
    await query.answer()

    report_type = query.data.replace("report_", "")

    async with async_session() as session:
        service = AdminService(session)

        if report_type == "daily":
            data = await service.get_daily_sales(days=7)
            title = "📊 گزارش فروش روزانه (۷ روز اخیر)"
            text = f"{title}\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            for item in data:
                text += f"📅 {item['date']}: {item['orders']} سفارش | {item['revenue']:,} تومان\n"

        elif report_type == "monthly":
            data = await service.get_monthly_sales(months=6)
            title = "📊 گزارش فروش ماهانه (۶ ماه اخیر)"
            text = f"{title}\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            for item in data:
                text += f"📅 {item['month']}: {item['orders']} سفارش | {item['revenue']:,} تومان\n"

        elif report_type == "yearly":
            data = await service.get_monthly_sales(months=12)
            title = "📊 گزارش فروش سالانه"
            text = f"{title}\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            for item in data:
                text += f"📅 {item['month']}: {item['orders']} سفارش | {item['revenue']:,} تومان\n"

        elif report_type == "profit":
            stats = await service.get_stats()
            text = (
                "💰 <b>گزارش سود</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"💰 درآمد امروز: {stats['today_income']:,} تومان\n"
                f"💰 درآمد ماه: {stats['month_income']:,} تومان\n"
            )

        elif report_type == "inventory":
            from bot.services.game_service import GameService
            game_service = GameService(session)
            games = await game_service.get_all_games(limit=50)

            text = "📦 <b>گزارش موجودی</b>\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            for game in games:
                text += f"🎮 {game.name}: {game.stock_display}\n"

        else:
            text = "گزارش نامشخص"

    await query.edit_message_text(
        text=text,
        reply_markup=get_admin_reports_keyboard(),
        parse_mode="HTML",
    )
