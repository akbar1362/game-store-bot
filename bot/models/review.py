"""
Review model
"""
from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from bot.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text, nullable=True)
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reviews")
    game = relationship("Game", back_populates="reviews")

    def __repr__(self):
        return f"<Review by {self.user_id} for Game {self.game_id}>"
