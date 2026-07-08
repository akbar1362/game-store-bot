"""
Cart service - handles shopping cart operations
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.cart import Cart, CartItem
from bot.models.game import Game


class CartService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_cart(self, user_id: int) -> Cart | None:
        """Get user's cart"""
        result = await self.session.execute(
            select(Cart).where(Cart.user_id == user_id)
        )
        cart = result.scalar_one_or_none()
        if not cart:
            cart = Cart(user_id=user_id)
            self.session.add(cart)
            await self.session.commit()
            await self.session.refresh(cart)
        return cart

    async def add_item(self, user_id: int, game_id: int, quantity: int = 1) -> CartItem:
        """Add item to cart"""
        cart = await self.get_cart(user_id)

        result = await self.session.execute(
            select(CartItem).where(
                CartItem.cart_id == cart.id, CartItem.game_id == game_id
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            existing.quantity += quantity
            await self.session.commit()
            return existing

        item = CartItem(cart_id=cart.id, game_id=game_id, quantity=quantity)
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def remove_item(self, user_id: int, game_id: int) -> bool:
        """Remove item from cart"""
        cart = await self.get_cart(user_id)
        result = await self.session.execute(
            select(CartItem).where(
                CartItem.cart_id == cart.id, CartItem.game_id == game_id
            )
        )
        item = result.scalar_one_or_none()
        if item:
            await self.session.delete(item)
            await self.session.commit()
            return True
        return False

    async def increase_quantity(self, user_id: int, game_id: int) -> bool:
        """Increase item quantity"""
        cart = await self.get_cart(user_id)
        result = await self.session.execute(
            select(CartItem).where(
                CartItem.cart_id == cart.id, CartItem.game_id == game_id
            )
        )
        item = result.scalar_one_or_none()
        if item:
            item.quantity += 1
            await self.session.commit()
            return True
        return False

    async def decrease_quantity(self, user_id: int, game_id: int) -> bool:
        """Decrease item quantity"""
        cart = await self.get_cart(user_id)
        result = await self.session.execute(
            select(CartItem).where(
                CartItem.cart_id == cart.id, CartItem.game_id == game_id
            )
        )
        item = result.scalar_one_or_none()
        if item:
            if item.quantity > 1:
                item.quantity -= 1
                await self.session.commit()
            else:
                await self.session.delete(item)
                await self.session.commit()
            return True
        return False

    async def clear_cart(self, user_id: int) -> None:
        """Clear user's cart"""
        cart = await self.get_cart(user_id)
        for item in cart.items:
            await self.session.delete(item)
        await self.session.commit()

    async def get_cart_items(self, user_id: int) -> list[dict]:
        """Get cart items with game details"""
        cart = await self.get_cart(user_id)
        items = []
        for item in cart.items:
            game_result = await self.session.execute(
                select(Game).where(Game.id == item.game_id)
            )
            game = game_result.scalar_one_or_none()
            if game:
                items.append(
                    {
                        "id": item.id,
                        "game_id": game.id,
                        "name": game.name,
                        "price": game.effective_price * item.quantity,
                        "unit_price": game.effective_price,
                        "quantity": item.quantity,
                        "image": game.image_url,
                    }
                )
        return items

    async def get_cart_total(self, user_id: int) -> int:
        """Get cart total price"""
        items = await self.get_cart_items(user_id)
        return sum(item["price"] for item in items)

    async def get_cart_item_count(self, user_id: int) -> int:
        """Get number of items in cart"""
        cart = await self.get_cart(user_id)
        return sum(item.quantity for item in cart.items)

    async def has_items(self, user_id: int) -> bool:
        """Check if cart has items"""
        cart = await self.get_cart(user_id)
        return len(cart.items) > 0
