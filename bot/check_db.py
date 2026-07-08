"""
Test script to check database
"""
import asyncio
from bot.database import init_db, async_session
from sqlalchemy import select, func
from bot.models.game import Game


async def check_db():
    await init_db()

    async with async_session() as session:
        # Count all games
        result = await session.execute(select(func.count(Game.id)))
        total = result.scalar() or 0
        print(f"Total games: {total}")

        # Count new games
        result = await session.execute(
            select(func.count(Game.id)).where(Game.is_new == True)
        )
        new_count = result.scalar() or 0
        print(f"New games: {new_count}")

        # Count bestsellers
        result = await session.execute(
            select(func.count(Game.id)).where(Game.is_bestseller == True)
        )
        best_count = result.scalar() or 0
        print(f"Bestsellers: {best_count}")

        # Count games with discount
        result = await session.execute(
            select(func.count(Game.id)).where(Game.discount_percent > 0)
        )
        discount_count = result.scalar() or 0
        print(f"Games with discount: {discount_count}")

        # List all games
        if total > 0:
            result = await session.execute(select(Game).limit(5))
            games = result.scalars().all()
            print("\nFirst 5 games:")
            for g in games:
                print(f"  - {g.name} | Active: {g.is_active} | New: {g.is_new} | Best: {g.is_bestseller}")


if __name__ == "__main__":
    asyncio.run(check_db())
