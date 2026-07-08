"""
Main user keyboards
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_welcome_keyboard() -> InlineKeyboardMarkup:
    """Welcome page keyboard"""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🎮 ورود به فروشگاه", callback_data="enter_store")],
        ]
    )


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Main menu keyboard"""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🎮 بازی‌های Xbox", callback_data="games_xbox"),
                InlineKeyboardButton("🎮 بازی‌های PlayStation", callback_data="games_ps"),
            ],
            [
                InlineKeyboardButton("🔥 پیشنهادهای ویژه", callback_data="special_offers"),
                InlineKeyboardButton("🆕 بازی‌های جدید", callback_data="new_games"),
            ],
            [
                InlineKeyboardButton("⭐ پرفروش‌ترین‌ها", callback_data="bestsellers"),
                InlineKeyboardButton("💰 تخفیف‌ها", callback_data="discount_games"),
            ],
            [InlineKeyboardButton("🛒 سبد خرید", callback_data="cart")],
            [
                InlineKeyboardButton("📦 سفارش‌های من", callback_data="orders"),
                InlineKeyboardButton("❤️ علاقه‌مندی‌ها", callback_data="favorites"),
            ],
            [
                InlineKeyboardButton("🔍 جستجوی بازی", callback_data="search"),
                InlineKeyboardButton("🎁 کد تخفیف", callback_data="discount_code"),
            ],
            [
                InlineKeyboardButton("💬 پشتیبانی", callback_data="support"),
                InlineKeyboardButton("📞 تماس با ما", callback_data="contact"),
            ],
            [
                InlineKeyboardButton("ℹ️ درباره فروشگاه", callback_data="about"),
                InlineKeyboardButton("⚙️ حساب کاربری", callback_data="profile"),
            ],
        ]
    )


def get_games_platform_keyboard() -> InlineKeyboardMarkup:
    """Games platform selection keyboard"""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Xbox One", callback_data="platform_xbox_one"),
                InlineKeyboardButton("Xbox Series S", callback_data="platform_xbox_series_s"),
            ],
            [
                InlineKeyboardButton("Xbox Series X", callback_data="platform_xbox_series_x"),
            ],
            [
                InlineKeyboardButton("PS4", callback_data="platform_ps4"),
                InlineKeyboardButton("PS5", callback_data="platform_ps5"),
            ],
            [
                InlineKeyboardButton("همه پلتفرم‌ها", callback_data="platform_all"),
            ],
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu"),
            ],
        ]
    )


def get_games_category_keyboard() -> InlineKeyboardMarkup:
    """Games category selection keyboard"""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🎯 اکشن", callback_data="cat_action"),
                InlineKeyboardButton("⚽ ورزشی", callback_data="cat_sports"),
            ],
            [
                InlineKeyboardButton("🏎️ مسابقه‌ای", callback_data="cat_racing"),
                InlineKeyboardButton("🔫 شوتر", callback_data="cat_shooter"),
            ],
            [
                InlineKeyboardButton("👻 ترسناک", callback_data="cat_horror"),
                InlineKeyboardButton("🌍 جهان باز", callback_data="cat_open_world"),
            ],
            [
                InlineKeyboardButton("🌐 آنلاین", callback_data="cat_online"),
                InlineKeyboardButton("💾 آفلاین", callback_data="cat_offline"),
            ],
            [
                InlineKeyboardButton("🧠 استراتژیک", callback_data="cat_strategy"),
                InlineKeyboardButton("👶 کودک", callback_data="cat_kids"),
            ],
            [
                InlineKeyboardButton("🗺️ ماجراجویی", callback_data="cat_adventure"),
                InlineKeyboardButton("🔧 شبیه‌سازی", callback_data="cat_simulation"),
            ],
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu"),
            ],
        ]
    )


def get_game_detail_keyboard(game_id: int, is_favorite: bool = False) -> InlineKeyboardMarkup:
    """Game detail page keyboard"""
    fav_text = "💔 حذف از علاقه‌مندی" if is_favorite else "❤️ افزودن به علاقه‌مندی"
    fav_action = f"remove_fav_{game_id}" if is_favorite else f"add_fav_{game_id}"

    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🛒 خرید بازی", callback_data=f"buy_{game_id}")],
            [
                InlineKeyboardButton(fav_text, callback_data=fav_action),
                InlineKeyboardButton("📤 اشتراک‌گذاری", callback_data=f"share_{game_id}"),
            ],
            [InlineKeyboardButton("⭐ امتیاز و نظر", callback_data=f"review_{game_id}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="games_list_back")],
        ]
    )


def get_pagination_keyboard(
    current_page: int,
    total_pages: int,
    prefix: str,
) -> InlineKeyboardMarkup:
    """Pagination keyboard"""
    buttons = []

    nav_row = []
    if current_page > 1:
        nav_row.append(InlineKeyboardButton("◀️", callback_data=f"{prefix}_page_{current_page - 1}"))
    nav_row.append(InlineKeyboardButton(f"📄 {current_page}/{total_pages}", callback_data="noop"))
    if current_page < total_pages:
        nav_row.append(InlineKeyboardButton("▶️", callback_data=f"{prefix}_page_{current_page + 1}"))
    buttons.append(nav_row)

    buttons.append([InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")])
    return InlineKeyboardMarkup(buttons)


def get_cart_keyboard(has_items: bool = False) -> InlineKeyboardMarkup:
    """Cart keyboard"""
    buttons = []
    if has_items:
        buttons.append([InlineKeyboardButton("💳 پرداخت", callback_data="checkout")])
        buttons.append([InlineKeyboardButton("🗑️ خالی کردن سبد", callback_data="clear_cart")])
    buttons.append([InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")])
    return InlineKeyboardMarkup(buttons)


def get_cart_item_keyboard(game_id: int) -> InlineKeyboardMarkup:
    """Cart item actions keyboard"""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("➕", callback_data=f"cart_increase_{game_id}"),
                InlineKeyboardButton("➖", callback_data=f"cart_decrease_{game_id}"),
                InlineKeyboardButton("🗑️", callback_data=f"cart_remove_{game_id}"),
            ],
        ]
    )


def get_profile_keyboard() -> InlineKeyboardMarkup:
    """Profile keyboard"""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("💰 کیف پول", callback_data="wallet")],
            [InlineKeyboardButton("📦 سفارش‌های من", callback_data="orders")],
            [InlineKeyboardButton("❤️ علاقه‌مندی‌ها", callback_data="favorites")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")],
        ]
    )


def get_wallet_keyboard() -> InlineKeyboardMarkup:
    """Wallet keyboard"""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("💰 افزایش موجودی", callback_data="wallet_topup")],
            [InlineKeyboardButton("📜 تاریخچه تراکنش", callback_data="wallet_history")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="profile")],
        ]
    )


def get_wallet_amount_keyboard() -> InlineKeyboardMarkup:
    """Wallet top-up amount selection"""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("۵۰,۰۰۰ تومان", callback_data="wallet_amount_50000")],
            [InlineKeyboardButton("۱۰۰,۰۰۰ تومان", callback_data="wallet_amount_100000")],
            [InlineKeyboardButton("۲۰۰,۰۰۰ تومان", callback_data="wallet_amount_200000")],
            [InlineKeyboardButton("۵۰۰,۰۰۰ تومان", callback_data="wallet_amount_500000")],
            [InlineKeyboardButton("مبلغ دلخواه", callback_data="wallet_amount_custom")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="wallet")],
        ]
    )


def get_payment_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Payment method selection keyboard"""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("💰 پرداخت از کیف پول", callback_data=f"pay_wallet_{order_id}")],
            [InlineKeyboardButton("💳 کارت به کارت", callback_data=f"pay_card_{order_id}")],
            [InlineKeyboardButton("❌ لغو سفارش", callback_data=f"cancel_order_{order_id}")],
        ]
    )


def get_support_keyboard() -> InlineKeyboardMarkup:
    """Support keyboard"""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📝 ارسال تیکت جدید", callback_data="new_ticket")],
            [InlineKeyboardButton("📜 تاریخچه تیکت‌ها", callback_data="ticket_history")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")],
        ]
    )


def get_confirm_keyboard(action: str) -> InlineKeyboardMarkup:
    """Confirmation keyboard"""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ بله", callback_data=f"confirm_{action}"),
                InlineKeyboardButton("❌ خیر", callback_data=f"deny_{action}"),
            ],
        ]
    )


def get_back_keyboard(callback_data: str = "main_menu") -> InlineKeyboardMarkup:
    """Simple back button keyboard"""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🔙 بازگشت", callback_data=callback_data)],
        ]
    )


def get_sort_keyboard(prefix: str = "sort") -> InlineKeyboardMarkup:
    """Sort options keyboard"""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📅 جدیدترین", callback_data=f"{prefix}_newest")],
            [InlineKeyboardButton("💰 ارزان‌ترین", callback_data=f"{prefix}_cheapest")],
            [InlineKeyboardButton("💎 گران‌ترین", callback_data=f"{prefix}_most_expensive")],
            [InlineKeyboardButton("⭐ محبوب‌ترین", callback_data=f"{prefix}_most_popular")],
            [InlineKeyboardButton("🏆 بهترین امتیاز", callback_data=f"{prefix}_highest_rated")],
            [InlineKeyboardButton("📈 پرفروش‌ترین", callback_data=f"{prefix}_best_selling")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")],
        ]
    )


def get_filter_keyboard() -> InlineKeyboardMarkup:
    """Filter options keyboard"""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🎯 پلتفرم", callback_data="filter_platform")],
            [InlineKeyboardButton("🎭 ژانر", callback_data="filter_category")],
            [InlineKeyboardButton("💰 قیمت", callback_data="filter_price")],
            [InlineKeyboardButton("📅 سال انتشار", callback_data="filter_year")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")],
        ]
    )


def get_review_keyboard(game_id: int) -> InlineKeyboardMarkup:
    """Review keyboard"""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⭐", callback_data=f"rate_{game_id}_1"),
                InlineKeyboardButton("⭐", callback_data=f"rate_{game_id}_2"),
                InlineKeyboardButton("⭐", callback_data=f"rate_{game_id}_3"),
                InlineKeyboardButton("⭐", callback_data=f"rate_{game_id}_4"),
                InlineKeyboardButton("⭐", callback_data=f"rate_{game_id}_5"),
            ],
            [InlineKeyboardButton("🔙 بازگشت", callback_data=f"game_{game_id}")],
        ]
    )


def get_search_keyboard() -> InlineKeyboardMarkup:
    """Search keyboard"""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🎯 جستجوی پیشرفته", callback_data="advanced_search")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")],
        ]
    )


def get_search_advanced_keyboard() -> InlineKeyboardMarkup:
    """Advanced search keyboard"""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📝 نام بازی", callback_data="search_name")],
            [InlineKeyboardButton("🎭 ژانر", callback_data="search_genre")],
            [InlineKeyboardButton("💰 قیمت", callback_data="search_price")],
            [InlineKeyboardButton("🎮 پلتفرم", callback_data="search_platform")],
            [InlineKeyboardButton("📅 سال انتشار", callback_data="search_year")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="search")],
        ]
    )
