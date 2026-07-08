"""
Game service - handles game operations
"""
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.game import Game
from bot.config.constants import GameCategory, GamePlatform, SortOption


class GameService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_game(self, game_id: int) -> Game | None:
        """Get game by ID"""
        result = await self.session.execute(select(Game).where(Game.id == game_id))
        return result.scalar_one_or_none()

    async def get_all_games(
        self,
        offset: int = 0,
        limit: int = 10,
        platform: str | None = None,
        category: str | None = None,
        sort: str = SortOption.NEWEST,
        search: str | None = None,
        min_price: int | None = None,
        max_price: int | None = None,
        year: int | None = None,
        is_active: bool = True,
    ) -> list[Game]:
        """Get games with filters and pagination"""
        query = select(Game).where(Game.is_active == is_active)

        if platform:
            if platform.lower() == "playstation":
                query = query.where(
                    or_(
                        Game.platforms.ilike("%PS5%"),
                        Game.platforms.ilike("%PS4%"),
                    )
                )
            elif platform.lower() == "xbox":
                query = query.where(Game.platforms.ilike("%Xbox%"))
            else:
                query = query.where(Game.platforms.ilike(f"%{platform}%"))

        if category:
            query = query.where(Game.category == category)

        if search:
            query = query.where(
                or_(
                    Game.name.ilike(f"%{search}%"),
                    Game.description.ilike(f"%{search}%"),
                )
            )

        if min_price is not None:
            query = query.where(Game.price >= min_price)

        if max_price is not None:
            query = query.where(Game.price <= max_price)

        if year:
            query = query.where(Game.release_date.ilike(f"%{year}%"))

        sort_map = {
            SortOption.NEWEST: Game.created_at.desc(),
            SortOption.OLDEST: Game.created_at.asc(),
            SortOption.CHEAPEST: Game.price.asc(),
            SortOption.MOST_EXPENSIVE: Game.price.desc(),
            SortOption.MOST_POPULAR: Game.views.desc(),
            SortOption.BEST_SELLING: Game.sales.desc(),
        }
        query = query.order_by(sort_map.get(sort, Game.created_at.desc()))
        query = query.offset(offset).limit(limit)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_game_count(
        self,
        platform: str | None = None,
        category: str | None = None,
        search: str | None = None,
        is_active: bool = True,
    ) -> int:
        """Get total game count with filters"""
        query = select(func.count(Game.id)).where(Game.is_active == is_active)

        if platform:
            if platform.lower() == "playstation":
                query = query.where(
                    or_(
                        Game.platforms.ilike("%PS5%"),
                        Game.platforms.ilike("%PS4%"),
                    )
                )
            elif platform.lower() == "xbox":
                query = query.where(Game.platforms.ilike("%Xbox%"))
            else:
                query = query.where(Game.platforms.ilike(f"%{platform}%"))
        if category:
            query = query.where(Game.category == category)
        if search:
            query = query.where(
                or_(
                    Game.name.ilike(f"%{search}%"),
                    Game.description.ilike(f"%{search}%"),
                )
            )

        result = await self.session.execute(query)
        return result.scalar() or 0

    async def get_new_games(self, limit: int = 10) -> list[Game]:
        """Get new games"""
        result = await self.session.execute(
            select(Game)
            .where(Game.is_active == True, Game.is_new == True)
            .order_by(Game.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_bestsellers(self, limit: int = 10) -> list[Game]:
        """Get bestselling games"""
        result = await self.session.execute(
            select(Game)
            .where(Game.is_active == True)
            .order_by(Game.sales.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_special_offers(self, limit: int = 10) -> list[Game]:
        """Get games with discount"""
        result = await self.session.execute(
            select(Game)
            .where(Game.is_active == True, Game.discount_percent > 0)
            .order_by(Game.discount_percent.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_featured_games(self, limit: int = 10) -> list[Game]:
        """Get featured games"""
        result = await self.session.execute(
            select(Game)
            .where(Game.is_active == True, Game.is_featured == True)
            .order_by(Game.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_games_by_platform(self, platform: str, limit: int = 10) -> list[Game]:
        """Get games by platform"""
        result = await self.session.execute(
            select(Game)
            .where(Game.is_active == True, Game.platforms.ilike(f"%{platform}%"))
            .order_by(Game.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def increment_views(self, game_id: int) -> None:
        """Increment game views"""
        game = await self.get_game(game_id)
        if game:
            game.views += 1
            await self.session.commit()

    async def increment_sales(self, game_id: int, quantity: int = 1) -> None:
        """Increment game sales"""
        game = await self.get_game(game_id)
        if game:
            game.sales += quantity
            await self.session.commit()

    async def create_game(self, **kwargs) -> Game:
        """Create a new game"""
        game = Game(**kwargs)
        self.session.add(game)
        await self.session.commit()
        await self.session.refresh(game)
        return game

    async def update_game(self, game_id: int, **kwargs) -> Game | None:
        """Update game data"""
        game = await self.get_game(game_id)
        if game:
            for key, value in kwargs.items():
                if hasattr(game, key):
                    setattr(game, key, value)
            await self.session.commit()
            await self.session.refresh(game)
        return game

    async def delete_game(self, game_id: int) -> bool:
        """Delete game (soft delete)"""
        game = await self.get_game(game_id)
        if game:
            game.is_active = False
            await self.session.commit()
            return True
        return False

    async def search_games(self, query: str) -> list[Game]:
        """Search games by name"""
        result = await self.session.execute(
            select(Game)
            .where(Game.is_active == True, Game.name.ilike(f"%{query}%"))
            .order_by(Game.views.desc())
        )
        return list(result.scalars().all())

    async def get_similar_games(self, game_id: int, limit: int = 5) -> list[Game]:
        """Get similar games based on category"""
        game = await self.get_game(game_id)
        if not game:
            return []
        result = await self.session.execute(
            select(Game)
            .where(
                Game.is_active == True,
                Game.id != game_id,
                Game.category == game.category,
            )
            .order_by(Game.sales.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_top_game(self) -> str:
        """Get top selling game name"""
        result = await self.session.execute(
            select(Game).where(Game.is_active == True).order_by(Game.sales.desc()).limit(1)
        )
        game = result.scalar_one_or_none()
        return game.name if game else "نامشخص"
