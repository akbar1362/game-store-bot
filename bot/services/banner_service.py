"""
Banner service - handles banner operations
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.banner import Banner


class BannerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_active_banners(self) -> list[Banner]:
        """Get all active banners"""
        result = await self.session.execute(
            select(Banner)
            .where(Banner.is_active == True)
            .order_by(Banner.priority.desc())
        )
        return list(result.scalars().all())

    async def get_banner(self, banner_id: int) -> Banner | None:
        """Get banner by ID"""
        result = await self.session.execute(
            select(Banner).where(Banner.id == banner_id)
        )
        return result.scalar_one_or_none()

    async def create_banner(
        self,
        image_url: str,
        title: str | None = None,
        link: str | None = None,
        priority: int = 0,
    ) -> Banner:
        """Create a new banner"""
        banner = Banner(
            title=title,
            image_url=image_url,
            link=link,
            priority=priority,
        )
        self.session.add(banner)
        await self.session.commit()
        await self.session.refresh(banner)
        return banner

    async def update_banner(self, banner_id: int, **kwargs) -> Banner | None:
        """Update banner"""
        banner = await self.get_banner(banner_id)
        if banner:
            for key, value in kwargs.items():
                if hasattr(banner, key):
                    setattr(banner, key, value)
            await self.session.commit()
        return banner

    async def delete_banner(self, banner_id: int) -> bool:
        """Delete banner"""
        banner = await self.get_banner(banner_id)
        if banner:
            await self.session.delete(banner)
            await self.session.commit()
            return True
        return False

    async def toggle_banner(self, banner_id: int) -> bool:
        """Toggle banner active status"""
        banner = await self.get_banner(banner_id)
        if banner:
            banner.is_active = not banner.is_active
            await self.session.commit()
            return True
        return False

    async def get_all_banners(self) -> list[Banner]:
        """Get all banners"""
        result = await self.session.execute(
            select(Banner).order_by(Banner.priority.desc())
        )
        return list(result.scalars().all())
