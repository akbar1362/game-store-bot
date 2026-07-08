"""
Wallet Transaction model
"""
from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from bot.database import Base


class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"), nullable=False)
    amount = Column(Integer, nullable=False)
    transaction_type = Column(String(20), nullable=False)  # deposit, withdrawal, purchase, refund, bonus
    description = Column(Text, nullable=True)
    receipt_url = Column(String(500), nullable=True)
    is_confirmed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="wallet_transactions")

    def __repr__(self):
        return f"<WalletTransaction {self.transaction_type} {self.amount}>"
