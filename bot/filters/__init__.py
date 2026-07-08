"""
Filters package
"""
from telegram.ext import BaseFilter
from bot.config.settings import Config


class IsAdmin(BaseFilter):
    """Filter to check if user is admin"""

    def filter(self, update):
        return update.effective_user.id in Config.ADMIN_IDS


class IsBanned(BaseFilter):
    """Filter to check if user is banned"""

    def filter(self, update):
        return getattr(update.effective_user, "is_banned", False)


class IsNotAdmin(BaseFilter):
    """Filter to check if user is not admin"""

    def filter(self, update):
        return update.effective_user.id not in Config.ADMIN_IDS
