"""
Favorite service - handles user favorites
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.favorite import Favorite
from bot.models.game import Game


class FavoriteService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_favorite(self, user_id: int, game_id: int) -> bool:
        """Add game to favorites"""
        existing = await self.is_favorite(user_id, game_id)
        if existing:
            return False

        fav = Favorite(user_id=user_id, game_id=game_id)
        self.session.add(fav)
        await self.session.commit()
        return True

    async def remove_favorite(self, user_id: int, game_id: int) -> bool:
        """Remove game from favorites"""
        result = await self.session.execute(
            select(Favorite).where(
                Favorite.user_id == user_id, Favorite.game_id == game_id
            )
        )
        fav = result.scalar_one_or_none()
        if fav:
            await self.session.delete(fav)
            await self.session.commit()
            return True
        return False

    async def is_favorite(self, user_id: int, game_id: int) -> bool:
        """Check if game is in favorites"""
        result = await self.session.execute(
            select(Favorite).where(
                Favorite.user_id == user_id, Favorite.game_id == game_id
            )
        )
        return result.scalar_one_or_none() is not None

    async def get_favorites(self, user_id: int) -> list[Game]:
        """Get all favorite games"""
        result = await self.session.execute(
            select(Game)
            .join(Favorite, Favorite.game_id == Game.id)
            .where(Favorite.user_id == user_id, Game.is_active == True)
            .order_by(Favorite.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_favorite_count(self, user_id: int) -> int:
        """Get favorite count"""
        result = await self.session.execute(
            select(Favorite).where(Favorite.user_id == user_id)
        )
        return len(result.scalars().all())

    async def toggle_favorite(self, user_id: int, game_id: int) -> bool:
        """Toggle favorite status, returns True if added"""
        is_fav = await self.is_favorite(user_id, game_id)
        if is_fav:
            await self.remove_favorite(user_id, game_id)
            return False
        else:
            await self.add_favorite(user_id, game_id)
            return True
