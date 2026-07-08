"""
All bot messages and texts in Persian
"""
from .settings import Config


def get_welcome_message() -> str:
    """Welcome page message"""
    return (
        f"🎮 <b>{Config.STORE_NAME}</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📚 {Config.STORE_DESCRIPTION}\n\n"
        "🔹 بهترین بازی‌های Xbox و PlayStation\n"
        "🔹 قیمت‌های رقابتی و مناسب\n"
        "🔹 پشتیبانی ۲۴ ساعته\n"
        "🔹 تحویل فوری\n"
        "🔹 ضمانت اصالت محصولات\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━"
    )


def get_main_menu_message() -> str:
    """Main menu message"""
    return (
        "🏠 <b>منوی اصلی</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "از منوی زیر بخش مورد نظر خود را انتخاب کنید:"
    )


def get_games_list_message(page: int, total: int) -> str:
    """Games list message"""
    return (
        f"🎮 <b>لیست بازی‌ها</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"صفحه {page} از {total}\n"
        "روی بازی مورد نظر کلیک کنید:"
    )


def get_game_detail_message(
    name: str,
    description: str,
    genre: str,
    platforms: str,
    version: str,
    price: int,
    discount_price: int | None,
    discount_percent: int,
    stock: str,
    age_rating: str,
    release_date: str,
    views: int,
    sales: int,
    meta_score: int | None = None,
) -> str:
    """Game detail message"""
    meta_line = f"🏆 امتیاز متاکریتیک: {meta_score}/100\n" if meta_score else ""

    msg = (
        f"🎮 <b>{name}</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📝 {description}\n\n"
        f"🎭 ژانر: {genre}\n"
        f"🎮 پلتفرم: {platforms}\n"
        f"📦 نسخه: {version}\n"
        f"🔢 رده سنی: {age_rating}\n"
        f"📅 تاریخ انتشار: {release_date}\n"
        f"👀 بازدیدها: {views:,}\n"
        f"🛒 فروش: {sales:,}\n"
        f"{meta_line}\n"
        f"📌 وضعیت: {stock}\n"
    )

    if discount_price and discount_percent:
        msg += (
            f"💰 قیمت اصلی: <s>{price:,} تومان</s>\n"
            f"🏷️ قیمت با تخفیف: <b>{discount_price:,} تومان</b>\n"
            f"🔥 تخفیف: {discount_percent}%\n"
        )
    else:
        msg += f"💰 قیمت: <b>{price:,} تومان</b>\n"

    msg += "\n━━━━━━━━━━━━━━━━━━━━━━"
    return msg


def get_cart_message(items: list, total: int, tax: int, grand_total: int) -> str:
    """Cart message"""
    msg = (
        "🛒 <b>سبد خرید</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    )
    if not items:
        msg += "سبد خرید شما خالی است."
    else:
        for i, item in enumerate(items, 1):
            msg += f"{i}. {item['name']}\n"
            msg += f"   تعداد: {item['quantity']} | قیمت: {item['price']:,} تومان\n\n"
        msg += f"💰 جمع کل: {total:,} تومان\n"
        msg += f"📊 مالیات: {tax:,} تومان\n"
        msg += f"💳 مبلغ قابل پرداخت: <b>{grand_total:,} تومان</b>\n"
    msg += "\n━━━━━━━━━━━━━━━━━━━━━━"
    return msg


def get_profile_message(
    name: str,
    phone: str,
    user_id: int,
    join_date: str,
    points: int,
    purchases: int,
    wallet: int,
) -> str:
    """User profile message"""
    return (
        "👤 <b>حساب کاربری</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📛 نام: {name}\n"
        f"📱 موبایل: {phone}\n"
        f"🆔 آیدی تلگرام: {user_id}\n"
        f"📅 تاریخ عضویت: {join_date}\n"
        f"⭐ امتیاز: {points}\n"
        f"🛒 تعداد خرید: {purchases}\n"
        f"💰 موجودی کیف پول: {wallet:,} تومان\n"
        "\n━━━━━━━━━━━━━━━━━━━━━━"
    )


def get_wallet_message(balance: int) -> str:
    """Wallet message"""
    return (
        "💰 <b>کیف پول</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"موجودی فعلی: <b>{balance:,} تومان</b>\n"
        "\n━━━━━━━━━━━━━━━━━━━━━━"
    )


def get_orders_message(orders: list) -> str:
    """Orders list message"""
    msg = (
        "📦 <b>سفارش‌های من</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    )
    if not orders:
        msg += "شما هنوز سفارشی ثبت نکرده‌اید."
    else:
        for order in orders:
            msg += (
                f"📦 سفارش #{order['id']}\n"
                f"📅 تاریخ: {order['date']}\n"
                f"💰 مبلغ: {order['total']:,} تومان\n"
                f"📌 وضعیت: {order['status']}\n\n"
            )
    msg += "━━━━━━━━━━━━━━━━━━━━━━"
    return msg


def get_favorites_message() -> str:
    """Favorites message"""
    return (
        "❤️ <b>علاقه‌مندی‌ها</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "بازی‌های مورد علاقه شما:"
    )


def get_search_message() -> str:
    """Search prompt message"""
    return (
        "🔍 <b>جستجوی بازی</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "نام بازی یا ژانر مورد نظر را وارد کنید:\n\n"
        "💡 <i>نکته: فقط کافیست بخشی از نام را تایپ کنید</i>"
    )


def get_support_message() -> str:
    """Support message"""
    return (
        "💬 <b>پشتیبانی</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "برای ارسال تیکت پشتیبانی، پیام خود را ارسال کنید.\n"
        "تیم پشتیبانی ما در اسرع وقت پاسخ خواهد داد."
    )


def get_contact_message() -> str:
    """Contact us message"""
    from .settings import Config

    return (
        "📞 <b>تماس با ما</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📱 شماره تماس: {Config.STORE_PHONE}\n"
        f"💬 پشتیبانی: @{Config.SUPPORT_USERNAME}\n"
        f"💳 شماره کارت: {Config.STORE_CARD_NUMBER}\n"
        f"👤 به نام: {Config.STORE_CARD_HOLDER}\n"
        f"🏦 بانک: {Config.STORE_CARD_BANK}\n"
        "\n━━━━━━━━━━━━━━━━━━━━━━"
    )


def get_about_message() -> str:
    """About us message"""
    from .settings import Config

    return (
        f"ℹ️ <b>درباره {Config.STORE_NAME}</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{Config.STORE_DESCRIPTION}\n\n"
        "🔹 فروش رسمی بازی‌های اورجینال\n"
        "🔹 پشتیبانی ۲۴ ساعته\n"
        "🔹 ضمانت بازگشت وجه\n"
        "🔹 به‌روزرسانی قیمت‌ها\n"
        "\n━━━━━━━━━━━━━━━━━━━━━━"
    )


def get_discount_code_message() -> str:
    """Discount code message"""
    return (
        "🎁 <b>کد تخفیف</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "کد تخفیف خود را وارد کنید:"
    )


def get_new_games_message() -> str:
    """New games message"""
    return (
        "🆕 <b>بازی‌های جدید</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "جدیدترین بازی‌های اضافه شده:"
    )


def get_bestsellers_message() -> str:
    """Bestsellers message"""
    return (
        "⭐ <b>پرفروش‌ترین‌ها</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "محبوب‌ترین بازی‌ها:"
    )


def get_special_offers_message() -> str:
    """Special offers message"""
    return (
        "🔥 <b>پیشنهادهای ویژه</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "بهترین تخفیف‌های ویژه:"
    )


def get_discount_games_message() -> str:
    """Discount games message"""
    return (
        "💰 <b>تخفیف‌ها</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "بازی‌های دارای تخفیف:"
    )


# Admin messages
def get_admin_panel_message() -> str:
    """Admin panel message"""
    return (
        "⚙️ <b>پنل مدیریت</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "به پنل مدیریت خوش آمدید.\n"
        "از منوی زیر بخش مورد نظر را انتخاب کنید:"
    )


def get_admin_stats_message(
    users: int,
    orders: int,
    today_income: int,
    month_income: int,
    top_game: str,
    online_users: int,
) -> str:
    """Admin statistics message"""
    return (
        "📊 <b>آمار پنل</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👥 تعداد کاربران: {users:,}\n"
        f"📦 تعداد سفارش‌ها: {orders:,}\n"
        f"💰 درآمد امروز: {today_income:,} تومان\n"
        f"💰 درآمد ماه: {month_income:,} تومان\n"
        f"🏆 پرفروش‌ترین بازی: {top_game}\n"
        f"🟢 کاربران آنلاین: {online_users}\n"
        "\n━━━━━━━━━━━━━━━━━━━━━━"
    )


# Order notifications
def get_order_placed_message(order_id: int, total: int) -> str:
    return (
        f"✅ <b>سفارش شما ثبت شد!</b>\n\n"
        f"📦 شماره سفارش: #{order_id}\n"
        f"💰 مبلغ: {total:,} تومان\n"
        f"📌 وضعیت: در انتظار بررسی\n\n"
        f"⏳ لطفاً منتظر تأیید سفارش باشید."
    )


def get_order_confirmed_message(order_id: int) -> str:
    return (
        f"✅ <b>سفارش #{order_id} تأیید شد!</b>\n\n"
        f"📦 سفارش شما در حال پردازش است."
    )


def get_order_shipped_message(order_id: int) -> str:
    return (
        f"📦 <b>سفارش #{order_id} ارسال شد!</b>\n\n"
        f"اطلاعات بازی برای شما ارسال خواهد شد."
    )


def get_order_delivered_message(order_id: int) -> str:
    return (
        f"✅ <b>سفارش #{order_id} تحویل داده شد!</b>\n\n"
        f"از خرید شما ممنونیم! 🎮"
    )


def get_order_cancelled_message(order_id: int) -> str:
    return (
        f"❌ <b>سفارش #{order_id} لغو شد</b>\n\n"
        f"در صورت سؤال با پشتیبانی تماس بگیرید."
    )


# Broadcast messages
def get_broadcast_success_message(count: int) -> str:
    return f"✅ پیام با موفقیت به {count} کاربر ارسال شد."


def get_no_results_message() -> str:
    return "🔍 نتیجه‌ای یافت نشد."


def get_error_message() -> str:
    return "❌ خطایی رخ داده است. لطفاً دوباره تلاش کنید."


def get_back_button_text() -> str:
    return "🔙 بازگشت"


def get_confirm_text() -> str:
    return "آیا مطمئن هستید؟"
