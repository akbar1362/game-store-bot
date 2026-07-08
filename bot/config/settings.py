"""
Settings and configuration management
"""
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")


class Config:
    """Main configuration class"""

    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    ADMIN_IDS: list[int] = [
        int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()
    ]
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite+aiosqlite:///{BASE_DIR / 'bot' / 'database' / 'store.db'}")
    DATABASE_PATH: str = str(BASE_DIR / "bot" / "database" / "store.db")

    STORE_NAME: str = os.getenv("STORE_NAME", "🎮 GameStore Pro")
    STORE_DESCRIPTION: str = os.getenv("STORE_DESCRIPTION", "فروشگاه تخصصی بازی‌های Xbox و PlayStation")
    STORE_LOGO: str = os.getenv("STORE_LOGO", "")
    STORE_BANNER: str = os.getenv("STORE_BANNER", "")
    STORE_PHONE: str = os.getenv("STORE_PHONE", "")
    STORE_CARD_NUMBER: str = os.getenv("STORE_CARD_NUMBER", "")
    STORE_CARD_HOLDER: str = os.getenv("STORE_CARD_HOLDER", "")
    STORE_CARD_BANK: str = os.getenv("STORE_CARD_BANK", "")

    SUPPORT_USERNAME: str = os.getenv("SUPPORT_USERNAME", "")
    CHANNEL_ID: str = os.getenv("CHANNEL_ID", "")

    TAX_RATE: float = float(os.getenv("TAX_RATE", "0"))
    WALLET_TOP_UP_MIN: int = int(os.getenv("WALLET_TOP_UP_MIN", "50000"))

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    BACKUP_ENABLED: bool = os.getenv("BACKUP_ENABLED", "true").lower() == "true"
    BACKUP_INTERVAL_HOURS: int = int(os.getenv("BACKUP_INTERVAL_HOURS", "24"))


class Paths:
    """File paths configuration"""

    BASE_DIR = BASE_DIR
    BOT_DIR = BASE_DIR / "bot"
    ASSETS_DIR = BOT_DIR / "assets"
    IMAGES_DIR = ASSETS_DIR / "images"
    LOGOS_DIR = IMAGES_DIR / "logos"
    BANNERS_DIR = IMAGES_DIR / "banners"
    GAMES_DIR = IMAGES_DIR / "games"
    LOGS_DIR = BOT_DIR / "logs"
    BACKUP_DIR = BOT_DIR / "backup"
    DATABASE_PATH = BASE_DIR / "bot" / "database" / "store.db"
