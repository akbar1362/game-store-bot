"""
Utility functions
"""
import logging
from pathlib import Path
from loguru import logger as loguru_logger
from bot.config.settings import Config, Paths


def setup_logging():
    """Setup application logging"""
    Paths.LOGS_DIR.mkdir(parents=True, exist_ok=True)

    loguru_logger.add(
        str(Paths.LOGS_DIR / "bot_{time:YYYY-MM-DD}.log"),
        rotation="00:00",
        retention="30 days",
        compression="zip",
        level=Config.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        encoding="utf-8",
    )

    loguru_logger.add(
        str(Paths.LOGS_DIR / "errors_{time:YYYY-MM-DD}.log"),
        rotation="00:00",
        retention="60 days",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        encoding="utf-8",
    )

    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def format_price(price: int) -> str:
    """Format price with commas"""
    return f"{price:,}"


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."
