"""
User service - handles user operations
"""
from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.user import User


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_user(
        self,
        telegram_id: int,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> User:
        """Get existing user or create new one"""
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
            )
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
        else:
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            await self.session.commit()

        return user

    async def get_user(self, telegram_id: int) -> User | None:
        """Get user by telegram ID"""
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def update_user(self, telegram_id: int, **kwargs) -> User | None:
        """Update user data"""
        user = await self.get_user(telegram_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            await self.session.commit()
            await self.session.refresh(user)
        return user

    async def set_phone(self, telegram_id: int, phone: str) -> User | None:
        """Set user phone number"""
        return await self.update_user(telegram_id, phone=phone)

    async def ban_user(self, telegram_id: int) -> None:
        """Ban a user"""
        await self.update_user(telegram_id, is_banned=True)

    async def unban_user(self, telegram_id: int) -> None:
        """Unban a user"""
        await self.update_user(telegram_id, is_banned=False)

    async def is_banned(self, telegram_id: int) -> bool:
        """Check if user is banned"""
        user = await self.get_user(telegram_id)
        return user.is_banned if user else False

    async def is_admin(self, telegram_id: int) -> bool:
        """Check if user is admin"""
        from bot.config.settings import Config
        return telegram_id in Config.ADMIN_IDS

    async def get_all_users(self, offset: int = 0, limit: int = 20) -> list[User]:
        """Get all users with pagination"""
        result = await self.session.execute(
            select(User).order_by(User.created_at.desc()).offset(offset).limit(limit)
        )
        return list(result.scalars().all())

    async def get_user_count(self) -> int:
        """Get total user count"""
        result = await self.session.execute(select(func.count(User.id)))
        return result.scalar() or 0

    async def search_users(self, query: str) -> list[User]:
        """Search users by username or name"""
        result = await self.session.execute(
            select(User).where(
                (User.username.ilike(f"%{query}%"))
                | (User.first_name.ilike(f"%{query}%"))
                | (User.last_name.ilike(f"%{query}%"))
            )
        )
        return list(result.scalars().all())

    async def increment_purchase_count(self, telegram_id: int) -> None:
        """Increment user purchase count"""
        user = await self.get_user(telegram_id)
        if user:
            user.purchase_count += 1
            await self.session.commit()

    async def add_points(self, telegram_id: int, points: int) -> None:
        """Add points to user"""
        user = await self.get_user(telegram_id)
        if user:
            user.points += points
            await self.session.commit()
