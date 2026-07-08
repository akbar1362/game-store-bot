"""
Wallet service - handles wallet operations
"""
from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.user import User
from bot.models.wallet import WalletTransaction


class WalletService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_balance(self, user_id: int) -> int:
        """Get user wallet balance"""
        result = await self.session.execute(
            select(User).where(User.telegram_id == user_id)
        )
        user = result.scalar_one_or_none()
        return user.wallet_balance if user else 0

    async def deposit(self, user_id: int, amount: int, description: str = "افزایش موجودی") -> WalletTransaction:
        """Deposit to wallet"""
        result = await self.session.execute(
            select(User).where(User.telegram_id == user_id)
        )
        user = result.scalar_one_or_none()
        if user:
            user.wallet_balance += amount

        transaction = WalletTransaction(
            user_id=user_id,
            amount=amount,
            transaction_type="deposit",
            description=description,
            is_confirmed=True,
        )
        self.session.add(transaction)
        await self.session.commit()
        await self.session.refresh(transaction)
        return transaction

    async def withdraw(self, user_id: int, amount: int, description: str = "برداشت از کیف پول") -> bool:
        """Withdraw from wallet"""
        balance = await self.get_balance(user_id)
        if balance < amount:
            return False

        result = await self.session.execute(
            select(User).where(User.telegram_id == user_id)
        )
        user = result.scalar_one_or_none()
        if user:
            user.wallet_balance -= amount

        transaction = WalletTransaction(
            user_id=user_id,
            amount=amount,
            transaction_type="withdrawal",
            description=description,
            is_confirmed=True,
        )
        self.session.add(transaction)
        await self.session.commit()
        return True

    async def deduct(self, user_id: int, amount: int, description: str = "پرداخت") -> bool:
        """Deduct from wallet for purchase"""
        return await self.withdraw(user_id, amount, description)

    async def refund(self, user_id: int, amount: int, description: str = "بازگشت وجه") -> WalletTransaction:
        """Refund to wallet"""
        return await self.deposit(user_id, amount, description)

    async def add_bonus(self, user_id: int, amount: int, description: str = "پاداش") -> WalletTransaction:
        """Add bonus to wallet"""
        return await self.deposit(user_id, amount, description)

    async def get_transactions(
        self, user_id: int, offset: int = 0, limit: int = 10
    ) -> list[WalletTransaction]:
        """Get user transactions"""
        result = await self.session.execute(
            select(WalletTransaction)
            .where(WalletTransaction.user_id == user_id)
            .order_by(WalletTransaction.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_pending_topups(self) -> list[WalletTransaction]:
        """Get pending top-up requests"""
        result = await self.session.execute(
            select(WalletTransaction)
            .where(
                WalletTransaction.transaction_type == "deposit",
                WalletTransaction.is_confirmed == False,
            )
            .order_by(WalletTransaction.created_at.desc())
        )
        return list(result.scalars().all())

    async def confirm_topup(self, transaction_id: int) -> bool:
        """Confirm a top-up transaction"""
        result = await self.session.execute(
            select(WalletTransaction).where(WalletTransaction.id == transaction_id)
        )
        transaction = result.scalar_one_or_none()
        if transaction:
            transaction.is_confirmed = True
            await self.session.commit()
            return True
        return False
