"""
Discount service - handles discount codes
"""
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.discount import DiscountCode


class DiscountService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_discount(self, code: str) -> DiscountCode | None:
        """Get discount code"""
        result = await self.session.execute(
            select(DiscountCode).where(DiscountCode.code == code.upper())
        )
        return result.scalar_one_or_none()

    async def validate_code(self, code: str, order_amount: int = 0) -> tuple[bool, str]:
        """Validate a discount code"""
        discount = await self.get_discount(code)
        if not discount:
            return False, "❌ کد تخفیف یافت نشد."

        if not discount.is_valid:
            if not discount.is_active:
                return False, "❌ کد تخفیف غیرفعال است."
            if discount.expires_at and discount.expires_at < datetime.utcnow():
                return False, "❌ کد تخفیف منقضی شده است."
            if discount.max_uses != -1 and discount.current_uses >= discount.max_uses:
                return False, "❌ کد تخفیف تمام شده است."

        if order_amount < discount.min_order_amount:
            return False, f"❌ حداقل مبلغ سفارش: {discount.min_order_amount:,} تومان"

        return True, "✅ کد تخفیف معتبر است."

    async def calculate_discount(self, code: str, amount: int) -> tuple[int, str]:
        """Calculate discount amount"""
        discount = await self.get_discount(code)
        if not discount:
            return 0, ""

        if discount.discount_type == "percentage":
            discount_amount = int(amount * discount.discount_value / 100)
        else:
            discount_amount = min(discount.discount_value, amount)

        return discount_amount, discount.code

    async def use_code(self, code: str) -> None:
        """Mark discount code as used"""
        discount = await self.get_discount(code)
        if discount:
            discount.current_uses += 1
            await self.session.commit()

    async def create_discount(
        self,
        code: str,
        discount_type: str,
        discount_value: int,
        min_order_amount: int = 0,
        max_uses: int = -1,
        expires_at: datetime | None = None,
    ) -> DiscountCode:
        """Create a new discount code"""
        discount = DiscountCode(
            code=code.upper(),
            discount_type=discount_type,
            discount_value=discount_value,
            min_order_amount=min_order_amount,
            max_uses=max_uses,
            expires_at=expires_at,
        )
        self.session.add(discount)
        await self.session.commit()
        await self.session.refresh(discount)
        return discount

    async def get_all_discounts(self) -> list[DiscountCode]:
        """Get all discount codes"""
        result = await self.session.execute(
            select(DiscountCode).order_by(DiscountCode.created_at.desc())
        )
        return list(result.scalars().all())

    async def toggle_discount(self, discount_id: int) -> bool:
        """Toggle discount active status"""
        result = await self.session.execute(
            select(DiscountCode).where(DiscountCode.id == discount_id)
        )
        discount = result.scalar_one_or_none()
        if discount:
            discount.is_active = not discount.is_active
            await self.session.commit()
            return True
        return False

    async def delete_discount(self, discount_id: int) -> bool:
        """Delete a discount code"""
        result = await self.session.execute(
            select(DiscountCode).where(DiscountCode.id == discount_id)
        )
        discount = result.scalar_one_or_none()
        if discount:
            await self.session.delete(discount)
            await self.session.commit()
            return True
        return False
