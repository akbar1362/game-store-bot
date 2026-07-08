"""
Game model
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float
from sqlalchemy.orm import relationship
from bot.database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(1000), nullable=True)
    gallery = Column(Text, nullable=True)  # JSON list of image URLs
    trailer_url = Column(String(1000), nullable=True)
    category = Column(String(50), nullable=False)
    platforms = Column(String(500), nullable=False)  # Comma-separated
    version = Column(String(50), nullable=False)
    age_rating = Column(String(10), nullable=True)
    meta_score = Column(Integer, nullable=True)
    file_size = Column(String(50), nullable=True)
    release_date = Column(String(20), nullable=True)
    price = Column(Integer, nullable=False)
    discount_price = Column(Integer, nullable=True)
    discount_percent = Column(Integer, default=0)
    stock_status = Column(String(20), default="in_stock")  # in_stock, out_of_stock, preorder
    views = Column(Integer, default=0)
    sales = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    is_new = Column(Boolean, default=False)
    is_bestseller = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reviews = relationship("Review", back_populates="game", lazy="selectin")
    order_items = relationship("OrderItem", back_populates="game", lazy="selectin")
    favorites = relationship("Favorite", back_populates="game", lazy="selectin")

    def __repr__(self):
        return f"<Game {self.name}>"

    @property
    def effective_price(self) -> int:
        return self.discount_price if self.discount_price else self.price

    @property
    def stock_display(self) -> str:
        statuses = {
            "in_stock": "✅ موجود",
            "out_of_stock": "❌ ناموجود",
            "preorder": "⏳ پیش فروش",
        }
        return statuses.get(self.stock_status, "نامشخص")
