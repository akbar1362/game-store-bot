"""
Order service - handles order operations
"""
from datetime import datetime, timedelta
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.order import Order, OrderItem
from bot.models.user import User


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(
        self,
        user_id: int,
        items: list[dict],
        total_amount: int,
        tax_amount: int = 0,
        discount_amount: int = 0,
        final_amount: int = 0,
        payment_method: str | None = None,
    ) -> Order:
        """Create a new order"""
        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            tax_amount=tax_amount,
            discount_amount=discount_amount,
            final_amount=final_amount or total_amount,
            payment_method=payment_method,
        )
        self.session.add(order)
        await self.session.flush()

        for item in items:
            order_item = OrderItem(
                order_id=order.id,
                game_id=item["game_id"],
                quantity=item["quantity"],
                price=item["price"],
            )
            self.session.add(order_item)

        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def get_order(self, order_id: int) -> Order | None:
        """Get order by ID"""
        result = await self.session.execute(
            select(Order).where(Order.id == order_id)
        )
        return result.scalar_one_or_none()

    async def get_user_orders(
        self, user_id: int, offset: int = 0, limit: int = 10
    ) -> list[Order]:
        """Get user orders"""
        result = await self.session.execute(
            select(Order)
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_orders_by_status(
        self, status: str, offset: int = 0, limit: int = 20
    ) -> list[Order]:
        """Get orders by status"""
        result = await self.session.execute(
            select(Order)
            .where(Order.status == status)
            .order_by(Order.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_all_orders(
        self, offset: int = 0, limit: int = 20
    ) -> list[Order]:
        """Get all orders"""
        result = await self.session.execute(
            select(Order).order_by(Order.created_at.desc()).offset(offset).limit(limit)
        )
        return list(result.scalars().all())

    async def update_order_status(self, order_id: int, status: str) -> Order | None:
        """Update order status"""
        order = await self.get_order(order_id)
        if order:
            order.status = status
            await self.session.commit()
            await self.session.refresh(order)
        return order

    async def set_payment_receipt(self, order_id: int, receipt_url: str) -> Order | None:
        """Set payment receipt"""
        order = await self.get_order(order_id)
        if order:
            order.payment_receipt = receipt_url
            await self.session.commit()
        return order

    async def get_order_count(self, status: str | None = None) -> int:
        """Get order count"""
        query = select(func.count(Order.id))
        if status:
            query = query.where(Order.status == status)
        result = await self.session.execute(query)
        return result.scalar() or 0

    async def get_total_revenue(self, days: int | None = None) -> int:
        """Get total revenue"""
        query = select(func.sum(Order.final_amount)).where(
            Order.status.in_(["shipped", "delivered"])
        )
        if days:
            since = datetime.utcnow() - timedelta(days=days)
            query = query.where(Order.created_at >= since)
        result = await self.session.execute(query)
        return result.scalar() or 0

    async def get_today_revenue(self) -> int:
        """Get today's revenue"""
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        result = await self.session.execute(
            select(func.sum(Order.final_amount)).where(
                Order.status.in_(["shipped", "delivered"]),
                Order.created_at >= today,
            )
        )
        return result.scalar() or 0

    async def get_month_revenue(self) -> int:
        """Get this month's revenue"""
        now = datetime.utcnow()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        result = await self.session.execute(
            select(func.sum(Order.final_amount)).where(
                Order.status.in_(["shipped", "delivered"]),
                Order.created_at >= month_start,
            )
        )
        return result.scalar() or 0

    async def get_total_orders(self) -> int:
        """Get total order count"""
        result = await self.session.execute(select(func.count(Order.id)))
        return result.scalar() or 0
