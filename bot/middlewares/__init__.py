"""
Middleware package
"""
import logging
import time
from collections import defaultdict
from telegram import Update
from telegram.ext import ContextTypes


logger = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiter middleware"""

    def __init__(self, max_requests: int = 30, window: int = 60):
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(list)

    def is_rate_limited(self, user_id: int) -> bool:
        now = time.time()
        self.requests[user_id] = [
            t for t in self.requests[user_id] if now - t < self.window
        ]
        if len(self.requests[user_id]) >= self.max_requests:
            return True
        self.requests[user_id].append(now)
        return False


rate_limiter = RateLimiter()


async def rate_limit_middleware(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Check rate limit"""
    user_id = update.effective_user.id if update.effective_user else 0
    if rate_limiter.is_rate_limited(user_id):
        if update.callback_query:
            await update.callback_query.answer("لطفاً صبر کنید...", show_alert=True)
        elif update.message:
            await update.message.reply_text("لطفاً صبر کنید...")
        return False
    return True


async def logging_middleware(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log updates"""
    user = update.effective_user
    if user:
        logger.info(
            f"User {user.id} ({user.username or 'N/A'}) - "
            f"Message: {update.message.text if update.message else 'N/A'} - "
            f"Callback: {update.callback_query.data if update.callback_query else 'N/A'}"
        )
