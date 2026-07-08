"""
Order and OrderItem models
"""
from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from bot.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"), nullable=False)
    total_amount = Column(Integer, nullable=False)
    tax_amount = Column(Integer, default=0)
    discount_amount = Column(Integer, default=0)
    final_amount = Column(Integer, nullable=False)
    status = Column(String(20), default="pending")  # pending, checking, shipped, delivered, cancelled
    payment_method = Column(String(20), nullable=True)  # wallet, card_to_card
    payment_receipt = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", lazy="selectin")

    def __repr__(self):
        return f"<Order #{self.id}>"


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
    game = relationship("Game", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem {self.game_id} x{self.quantity}>"
