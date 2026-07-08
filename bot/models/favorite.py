"""
Favorite model
"""
from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from bot.database import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="favorites")
    game = relationship("Game", back_populates="favorites")

    __table_args__ = (UniqueConstraint("user_id", "game_id", name="uq_user_game_fav"),)

    def __repr__(self):
        return f"<Favorite user={self.user_id} game={self.game_id}>"
