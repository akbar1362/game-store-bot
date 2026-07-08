"""
Seed script to add sample games to the database
Run: python -m bot.seed
"""
import asyncio
import os
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "bot" / "database"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "store.db"
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

print(f"Database path: {DB_PATH}")
print(f"Database exists: {DB_PATH.exists()}")

# Setup engine
engine = create_async_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


# Import models
from bot.models.user import User
from bot.models.game import Game
from bot.models.order import Order, OrderItem
from bot.models.review import Review
from bot.models.favorite import Favorite
from bot.models.wallet import WalletTransaction
from bot.models.discount import DiscountCode
from bot.models.ticket import Ticket, TicketMessage
from bot.models.banner import Banner
from bot.models.cart import Cart, CartItem


GAMES = [
    {
        "name": "Call of Duty: Modern Warfare III",
        "description": "جدیدترین نسخه کال آف دیوتی با گرافیک خیره‌کننده و مودهای متنوع",
        "category": "shooter",
        "platforms": "PS5, Xbox Series X, PS4, Xbox One",
        "version": "standard",
        "price": 2500000,
        "discount_price": 2100000,
        "discount_percent": 16,
        "stock_status": "in_stock",
        "age_rating": "18+",
        "meta_score": 85,
        "release_date": "2023-11-10",
        "is_new": True,
        "is_bestseller": True,
    },
    {
        "name": "EA FC 25",
        "description": "بهترین بازی فوتبال با لیگ‌های معتبر جهانی و گیم‌پلی واقع‌گرایانه",
        "category": "sports",
        "platforms": "PS5, Xbox Series X, PS4, Xbox One",
        "version": "standard",
        "price": 2800000,
        "discount_price": 2400000,
        "discount_percent": 14,
        "stock_status": "in_stock",
        "age_rating": "3+",
        "meta_score": 82,
        "release_date": "2024-09-27",
        "is_new": True,
        "is_bestseller": True,
    },
    {
        "name": "Grand Theft Auto V",
        "description": "بازی افسانه‌ای جهان باز با داستان جذاب و آنلاین محبوب",
        "category": "open_world",
        "platforms": "PS5, Xbox Series X, PS4, Xbox One",
        "version": "premium",
        "price": 1800000,
        "discount_price": 1200000,
        "discount_percent": 33,
        "stock_status": "in_stock",
        "age_rating": "18+",
        "meta_score": 97,
        "release_date": "2013-09-17",
        "is_bestseller": True,
    },
    {
        "name": "God of War Ragnarök",
        "description": "ماجراجویی حماسی کریتوس در اساطیر نورس",
        "category": "adventure",
        "platforms": "PS5, PS4",
        "version": "standard",
        "price": 3000000,
        "discount_price": 2500000,
        "discount_percent": 17,
        "stock_status": "in_stock",
        "age_rating": "18+",
        "meta_score": 94,
        "release_date": "2022-11-09",
        "is_bestseller": True,
    },
    {
        "name": "Spider-Man 2",
        "description": "ماجراجویی مرد عنکبوتی در نیویورک با گرافیک نسل نهمی",
        "category": "action",
        "platforms": "PS5",
        "version": "standard",
        "price": 3200000,
        "discount_price": 2800000,
        "discount_percent": 12,
        "stock_status": "in_stock",
        "age_rating": "16+",
        "meta_score": 90,
        "release_date": "2023-10-20",
        "is_new": True,
    },
    {
        "name": "Elden Ring",
        "description": "بازی جهان باز سخت و چالش‌برانگیز از خالقان Dark Souls",
        "category": "action",
        "platforms": "PS5, Xbox Series X, PS4, Xbox One",
        "version": "standard",
        "price": 2500000,
        "discount_price": 2000000,
        "discount_percent": 20,
        "stock_status": "in_stock",
        "age_rating": "18+",
        "meta_score": 96,
        "release_date": "2022-02-25",
        "is_bestseller": True,
    },
    {
        "name": "Red Dead Redemption 2",
        "description": "ماجراجویی وسترن با داستان عمیق و جهان زنده",
        "category": "open_world",
        "platforms": "PS5, Xbox Series X, PS4, Xbox One",
        "version": "standard",
        "price": 2000000,
        "discount_price": 1400000,
        "discount_percent": 30,
        "stock_status": "in_stock",
        "age_rating": "18+",
        "meta_score": 97,
        "release_date": "2018-10-26",
        "is_bestseller": True,
    },
    {
        "name": "Assassin's Creed Mirage",
        "description": "بازگشت به ریشه‌های اساس کرید در بغداد",
        "category": "adventure",
        "platforms": "PS5, Xbox Series X, PS4, Xbox One",
        "version": "standard",
        "price": 2200000,
        "discount_price": 1800000,
        "discount_percent": 18,
        "stock_status": "in_stock",
        "age_rating": "18+",
        "meta_score": 76,
        "release_date": "2023-10-05",
        "is_new": True,
    },
    {
        "name": "Hogwarts Legacy",
        "description": "زندگی جادوگری در دنیای هری پاتر",
        "category": "adventure",
        "platforms": "PS5, Xbox Series X, PS4, Xbox One",
        "version": "deluxe",
        "price": 3500000,
        "discount_price": 2800000,
        "discount_percent": 20,
        "stock_status": "in_stock",
        "age_rating": "16+",
        "meta_score": 84,
        "release_date": "2023-02-10",
        "is_bestseller": True,
    },
    {
        "name": "Forza Horizon 5",
        "description": "بهترین بازی مسابقه‌ای با گرافیک خیره‌کننده مکزیک",
        "category": "racing",
        "platforms": "Xbox Series X, Xbox One, PC",
        "version": "standard",
        "price": 1800000,
        "discount_price": 1200000,
        "discount_percent": 33,
        "stock_status": "in_stock",
        "age_rating": "3+",
        "meta_score": 92,
        "release_date": "2021-11-09",
        "is_bestseller": True,
    },
    {
        "name": "Resident Evil 4 Remake",
        "description": "بازسازی ترسناک و هیجانی نسخه کلاسیک",
        "category": "horror",
        "platforms": "PS5, Xbox Series X, PS4",
        "version": "standard",
        "price": 2400000,
        "discount_price": 2000000,
        "discount_percent": 17,
        "stock_status": "in_stock",
        "age_rating": "18+",
        "meta_score": 93,
        "release_date": "2023-03-24",
    },
    {
        "name": "Cyberpunk 2077",
        "description": "بازی جهان باز آینده‌نگرانه در شهر نایت سیتی",
        "category": "open_world",
        "platforms": "PS5, Xbox Series X, PS4, Xbox One",
        "version": "ultimate",
        "price": 2800000,
        "discount_price": 1800000,
        "discount_percent": 36,
        "stock_status": "in_stock",
        "age_rating": "18+",
        "meta_score": 86,
        "release_date": "2020-12-10",
    },
    {
        "name": "Minecraft",
        "description": "بازی خلاقانه ساخت و ساز در دنیای بلوکی",
        "category": "kids",
        "platforms": "PS5, Xbox Series X, PS4, Xbox One, Nintendo Switch",
        "version": "standard",
        "price": 800000,
        "discount_price": 600000,
        "discount_percent": 25,
        "stock_status": "in_stock",
        "age_rating": "7+",
        "meta_score": 93,
        "release_date": "2011-11-18",
        "is_bestseller": True,
    },
    {
        "name": "The Last of Us Part I",
        "description": "داستان تأثیرگذار بقا در دنیای پسا آخرالزمانی",
        "category": "action",
        "platforms": "PS5, PC",
        "version": "standard",
        "price": 2800000,
        "discount_price": 2200000,
        "discount_percent": 21,
        "stock_status": "in_stock",
        "age_rating": "18+",
        "meta_score": 88,
        "release_date": "2022-09-02",
    },
    {
        "name": "Gran Turismo 7",
        "description": "بهترین شبیه‌ساز مسابقه واقعی",
        "category": "simulation",
        "platforms": "PS5, PS4",
        "version": "standard",
        "price": 2500000,
        "discount_price": 2000000,
        "discount_percent": 20,
        "stock_status": "in_stock",
        "age_rating": "3+",
        "meta_score": 87,
        "release_date": "2022-03-04",
    },
    {
        "name": "Starfield",
        "description": "ماجراجویی فضایی بتسدا در دنیایی عظیم",
        "category": "open_world",
        "platforms": "Xbox Series X, PC",
        "version": "premium",
        "price": 3000000,
        "discount_price": 2500000,
        "discount_percent": 17,
        "stock_status": "in_stock",
        "age_rating": "18+",
        "meta_score": 83,
        "release_date": "2023-09-06",
        "is_new": True,
    },
    {
        "name": "Diablo IV",
        "description": "بازی اکشن نقش‌آفرینی تاریک و هیجانی",
        "category": "action",
        "platforms": "PS5, Xbox Series X, PS4, Xbox One, PC",
        "version": "standard",
        "price": 2600000,
        "discount_price": 2100000,
        "discount_percent": 19,
        "stock_status": "in_stock",
        "age_rating": "18+",
        "meta_score": 86,
        "release_date": "2023-06-06",
    },
    {
        "name": "Fortnite",
        "description": "بازی رایگان بتل رویال محبوب جهان",
        "category": "online",
        "platforms": "PS5, Xbox Series X, PS4, Xbox One, Nintendo Switch",
        "version": "standard",
        "price": 0,
        "discount_price": 0,
        "discount_percent": 0,
        "stock_status": "in_stock",
        "age_rating": "12+",
        "meta_score": 80,
        "release_date": "2017-07-25",
        "is_bestseller": True,
    },
    {
        "name": "Counter-Strike 2",
        "description": "بازی شوتر رقابتی محبوب ای‌اسپورت",
        "category": "shooter",
        "platforms": "PC",
        "version": "standard",
        "price": 0,
        "discount_price": 0,
        "discount_percent": 0,
        "stock_status": "in_stock",
        "age_rating": "16+",
        "meta_score": 83,
        "release_date": "2023-09-27",
        "is_new": True,
        "is_bestseller": True,
    },
]


async def seed():
    """Add sample games to database"""
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created.")

    # Check existing games
    from sqlalchemy import select, func
    async with async_session() as session:
        result = await session.execute(select(func.count(Game.id)))
        count = result.scalar() or 0
        print(f"Existing games: {count}")

        if count > 0:
            print("Database already has games. Skipping seed.")
            return

        # Add games
        for game_data in GAMES:
            game = Game(**game_data)
            session.add(game)
            print(f"Adding: {game_data['name']} - {game_data['price']:,} Toman")

        await session.commit()
        print(f"\nDone! {len(GAMES)} games added successfully.")


if __name__ == "__main__":
    asyncio.run(seed())
