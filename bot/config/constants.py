"""
Application constants
"""
from enum import Enum


class GamePlatform(str, Enum):
    XBOX_ONE = "xbox_one"
    XBOX_SERIES_S = "xbox_series_s"
    XBOX_SERIES_X = "xbox_series_x"
    PS4 = "ps4"
    PS5 = "ps5"

    @property
    def display_name(self) -> str:
        names = {
            "xbox_one": "Xbox One",
            "xbox_series_s": "Xbox Series S",
            "xbox_series_x": "Xbox Series X",
            "ps4": "PS4",
            "ps5": "PS5",
        }
        return names.get(self.value, self.value)


class GameVersion(str, Enum):
    STANDARD = "standard"
    DELUXE = "deluxe"
    ULTIMATE = "ultimate"
    GOLD = "gold"
    PREMIUM = "premium"

    @property
    def display_name(self) -> str:
        names = {
            "standard": "Standard",
            "deluxe": "Deluxe",
            "ultimate": "Ultimate",
            "gold": "Gold",
            "premium": "Premium",
        }
        return names.get(self.value, self.value)


class GameCategory(str, Enum):
    ACTION = "action"
    SPORTS = "sports"
    RACING = "racing"
    SHOOTER = "shooter"
    HORROR = "horror"
    OPEN_WORLD = "open_world"
    ONLINE = "online"
    OFFLINE = "offline"
    STRATEGY = "strategy"
    KIDS = "kids"
    ADVENTURE = "adventure"
    SIMULATION = "simulation"

    @property
    def display_name(self) -> str:
        names = {
            "action": "اکشن",
            "sports": "ورزشی",
            "racing": "مسابقه‌ای",
            "shooter": "شوتر",
            "horror": "ترسناک",
            "open_world": "جهان باز",
            "online": "آنلاین",
            "offline": "آفلاین",
            "strategy": "استراتژیک",
            "kids": "کودک",
            "adventure": "ماجراجویی",
            "simulation": "شبیه‌سازی",
        }
        return names.get(self.value, self.value)


class OrderStatus(str, Enum):
    PENDING = "pending"
    CHECKING = "checking"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

    @property
    def display_name(self) -> str:
        names = {
            "pending": "⏳ در انتظار",
            "checking": "🔍 در حال بررسی",
            "shipped": "📦 ارسال شده",
            "delivered": "✅ تحویل داده شده",
            "cancelled": "❌ لغو شده",
        }
        return names.get(self.value, self.value)


class TicketStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"

    @property
    def display_name(self) -> str:
        names = {"open": "باز", "closed": "بسته شده"}
        return names.get(self.value, self.value)


class WalletTransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    PURCHASE = "purchase"
    REFUND = "refund"
    BONUS = "bonus"


class DiscountType(str, Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"


class AgeRating(str, Enum):
    RATING_3 = "3+"
    RATING_7 = "7+"
    RATING_12 = "12+"
    RATING_16 = "16+"
    RATING_18 = "18+"
    RP = "RP"


class SortOption(str, Enum):
    NEWEST = "newest"
    OLDEST = "oldest"
    CHEAPEST = "cheapest"
    MOST_EXPENSIVE = "most_expensive"
    MOST_POPULAR = "most_popular"
    HIGHEST_RATED = "highest_rated"
    BEST_SELLING = "best_selling"
