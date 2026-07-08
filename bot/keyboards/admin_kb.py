"""
Admin panel keyboards
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_admin_panel_keyboard() -> InlineKeyboardMarkup:
    """Main admin panel keyboard"""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📊 آمار", callback_data="admin_stats"),
                InlineKeyboardButton("👥 کاربران", callback_data="admin_users"),
            ],
            [
                InlineKeyboardButton("🎮 بازی‌ها", callback_data="admin_games"),
                InlineKeyboardButton("📦 سفارش‌ها", callback_data="admin_orders"),
            ],
            [
                InlineKeyboardButton("💰 پرداخت‌ها", callback_data="admin_payments"),
                InlineKeyboardButton("🎁 تخفیف‌ها", callback_data="admin_discounts"),
            ],
            [
                InlineKeyboardButton("💬 پیام‌ها", callback_data="admin_messages"),
                InlineKeyboardButton("🖼️ بنرها", callback_data="admin_banners"),
            ],
            [
                InlineKeyboardButton("📢 اطلاعیه‌ها", callback_data="admin_notifications"),
                InlineKeyboardButton("📝 نظرات", callback_data="admin_reviews"),
            ],
            [
                InlineKeyboardButton("📦 موجودی", callback_data="admin_inventory"),
                InlineKeyboardButton("💰 کیف پول", callback_data="admin_wallet"),
            ],
            [
                InlineKeyboardButton("📈 گزارش‌ها", callback_data="admin_reports"),
                InlineKeyboardButton("📋 لاگ‌ها", callback_data="admin_logs"),
            ],
            [
                InlineKeyboardButton("⚙️ تنظیمات", callback_data="admin_settings"),
                InlineKeyboardButton("🔙 خروج", callback_data="exit_admin"),
            ],
        ]
    )


def get_admin_games_keyboard() -> InlineKeyboardMarkup:
    """Admin games management keyboard"""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("➕ افزودن بازی", callback_data="admin_add_game")],
            [InlineKeyboardButton("📋 لیست بازی‌ها", callback_data="admin_list_games")],
            [InlineKeyboardButton("🔍 جستجوی بازی", callback_data="admin_search_game")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")],
        ]
    )


def get_admin_users_keyboard() -> InlineKeyboardMarkup:
    """Admin users management keyboard"""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📋 لیست کاربران", callback_data="admin_list_users")],
            [InlineKeyboardButton("🔍 جستجوی کاربر", callback_data="admin_search_user")],
            [InlineKeyboardButton("📢 ارسال همگانی", callback_data="admin_broadcast")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")],
        ]
    )


def get_admin_orders_keyboard() -> InlineKeyboardMarkup:
    """Admin orders management keyboard"""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("⏳ در انتظار", callback_data="admin_orders_pending")],
            [InlineKeyboardButton("🔍 در حال بررسی", callback_data="admin_orders_checking")],
            [InlineKeyboardButton("📦 ارسال شده", callback_data="admin_orders_shipped")],
            [InlineKeyboardButton("✅ تحویل شده", callback_data="admin_orders_delivered")],
            [InlineKeyboardButton("❌ لغو شده", callback_data="admin_orders_cancelled")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")],
        ]
    )


def get_admin_settings_keyboard() -> InlineKeyboardMarkup:
    """Admin settings keyboard"""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📝 تغییر نام فروشگاه", callback_data="admin_set_name")],
            [InlineKeyboardButton("🖼️ تغییر لوگو", callback_data="admin_set_logo")],
            [InlineKeyboardButton("💳 تغییر شماره کارت", callback_data="admin_set_card")],
            [InlineKeyboardButton("📝 تغییر متن‌ها", callback_data="admin_set_texts")],
            [InlineKeyboardButton("🔧 فعال/غیرفعال", callback_data="admin_toggle")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")],
        ]
    )


def get_admin_broadcast_keyboard() -> InlineKeyboardMarkup:
    """Admin broadcast keyboard"""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📝 ارسال متن", callback_data="broadcast_text")],
            [InlineKeyboardButton("🖼️ ارسال عکس", callback_data="broadcast_photo")],
            [InlineKeyboardButton("🎬 ارسال ویدئو", callback_data="broadcast_video")],
            [InlineKeyboardButton("📎 ارسال فایل", callback_data="broadcast_file")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_users")],
        ]
    )


def get_admin_confirm_keyboard(action: str) -> InlineKeyboardMarkup:
    """Admin confirmation keyboard"""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ تأیید", callback_data=f"admin_confirm_{action}"),
                InlineKeyboardButton("❌ لغو", callback_data=f"admin_deny_{action}"),
            ],
        ]
    )


def get_admin_game_edit_keyboard(game_id: int) -> InlineKeyboardMarkup:
    """Admin game edit keyboard"""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📝 ویرایش نام", callback_data=f"admin_edit_game_name_{game_id}")],
            [InlineKeyboardButton("💰 تغییر قیمت", callback_data=f"admin_edit_game_price_{game_id}")],
            [InlineKeyboardButton("📝 ویرایش توضیحات", callback_data=f"admin_edit_game_desc_{game_id}")],
            [InlineKeyboardButton("🖼️ تغییر تصویر", callback_data=f"admin_edit_game_image_{game_id}")],
            [InlineKeyboardButton("🎭 تغییر ژانر", callback_data=f"admin_edit_game_cat_{game_id}")],
            [InlineKeyboardButton("🎮 تغییر پلتفرم", callback_data=f"admin_edit_game_platform_{game_id}")],
            [InlineKeyboardButton("📦 تغییر موجودی", callback_data=f"admin_edit_game_stock_{game_id}")],
            [InlineKeyboardButton("🔥 تخفیف", callback_data=f"admin_edit_game_discount_{game_id}")],
            [InlineKeyboardButton("🗑️ حذف بازی", callback_data=f"admin_delete_game_{game_id}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_games")],
        ]
    )


def get_admin_order_detail_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Admin order detail keyboard"""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ تأیید", callback_data=f"admin_order_confirm_{order_id}"),
                InlineKeyboardButton("📦 ارسال", callback_data=f"admin_order_ship_{order_id}"),
            ],
            [
                InlineKeyboardButton("✅ تحویل", callback_data=f"admin_order_deliver_{order_id}"),
                InlineKeyboardButton("❌ لغو", callback_data=f"admin_order_cancel_{order_id}"),
            ],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_orders")],
        ]
    )


def get_admin_discount_keyboard() -> InlineKeyboardMarkup:
    """Admin discount management keyboard"""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("➕ افزودن کد تخفیف", callback_data="admin_add_discount")],
            [InlineKeyboardButton("📋 لیست کدها", callback_data="admin_list_discounts")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")],
        ]
    )


def get_admin_reports_keyboard() -> InlineKeyboardMarkup:
    """Admin reports keyboard"""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📅 گزارش روزانه", callback_data="report_daily")],
            [InlineKeyboardButton("📅 گزارش ماهانه", callback_data="report_monthly")],
            [InlineKeyboardButton("📅 گزارش سالانه", callback_data="report_yearly")],
            [InlineKeyboardButton("💰 گزارش سود", callback_data="report_profit")],
            [InlineKeyboardButton("📦 گزارش موجودی", callback_data="report_inventory")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")],
        ]
    )


def get_admin_backup_keyboard() -> InlineKeyboardMarkup:
    """Admin backup keyboard"""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("💾 ایجاد بکاپ", callback_data="admin_create_backup")],
            [InlineKeyboardButton("📥 دانلود بکاپ", callback_data="admin_download_backup")],
            [InlineKeyboardButton("📤 بازگردانی", callback_data="admin_restore_backup")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")],
        ]
    )


def get_admin_notification_keyboard() -> InlineKeyboardMarkup:
    """Admin notification keyboard"""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📦 ارسال اعلان سفارش", callback_data="admin_notify_order")],
            [InlineKeyboardButton("🎮 ارسال اعلان بازی جدید", callback_data="admin_notify_game")],
            [InlineKeyboardButton("🔥 ارسال اعلان تخفیف", callback_data="admin_notify_discount")],
            [InlineKeyboardButton("📢 ارسال همگانی", callback_data="admin_broadcast")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")],
        ]
    )
