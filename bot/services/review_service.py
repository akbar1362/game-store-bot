"""
Review service - handles game reviews
"""
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.review import Review
from bot.models.user import User


class ReviewService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_review(
        self, user_id: int, game_id: int, rating: int, comment: str | None = None
    ) -> Review:
        """Add a review"""
        existing = await self.get_user_review(user_id, game_id)
        if existing:
            existing.rating = rating
            existing.comment = comment
            await self.session.commit()
            await self.session.refresh(existing)
            return existing

        review = Review(
            user_id=user_id,
            game_id=game_id,
            rating=rating,
            comment=comment,
        )
        self.session.add(review)
        await self.session.commit()
        await self.session.refresh(review)
        return review

    async def get_user_review(self, user_id: int, game_id: int) -> Review | None:
        """Get user's review for a game"""
        result = await self.session.execute(
            select(Review).where(
                Review.user_id == user_id, Review.game_id == game_id
            )
        )
        return result.scalar_one_or_none()

    async def get_game_reviews(
        self, game_id: int, approved_only: bool = True
    ) -> list[Review]:
        """Get all reviews for a game"""
        query = select(Review).where(Review.game_id == game_id)
        if approved_only:
            query = query.where(Review.is_approved == True)
        query = query.order_by(Review.created_at.desc())
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_average_rating(self, game_id: int) -> float:
        """Get average rating for a game"""
        result = await self.session.execute(
            select(func.avg(Review.rating)).where(
                Review.game_id == game_id, Review.is_approved == True
            )
        )
        return result.scalar() or 0.0

    async def approve_review(self, review_id: int) -> bool:
        """Approve a review"""
        result = await self.session.execute(
            select(Review).where(Review.id == review_id)
        )
        review = result.scalar_one_or_none()
        if review:
            review.is_approved = True
            await self.session.commit()
            return True
        return False

    async def delete_review(self, review_id: int) -> bool:
        """Delete a review"""
        result = await self.session.execute(
            select(Review).where(Review.id == review_id)
        )
        review = result.scalar_one_or_none()
        if review:
            await self.session.delete(review)
            await self.session.commit()
            return True
        return False

    async def get_pending_reviews(self) -> list[Review]:
        """Get unapproved reviews"""
        result = await self.session.execute(
            select(Review)
            .where(Review.is_approved == False)
            .order_by(Review.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_all_reviews(self) -> list[Review]:
        """Get all reviews"""
        result = await self.session.execute(
            select(Review).order_by(Review.created_at.desc())
        )
        return list(result.scalars().all())
