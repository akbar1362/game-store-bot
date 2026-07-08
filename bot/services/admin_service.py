"""
Admin service - handles admin-specific operations
"""
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.user import User
from bot.models.order import Order
from bot.models.game import Game
from bot.config.settings import Paths


class AdminService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_stats(self) -> dict:
        """Get admin dashboard statistics"""
        user_count_result = await self.session.execute(select(func.count(User.id)))
        user_count = user_count_result.scalar() or 0

        order_count_result = await self.session.execute(select(func.count(Order.id)))
        order_count = order_count_result.scalar() or 0

        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_revenue_result = await self.session.execute(
            select(func.sum(Order.final_amount)).where(
                Order.status.in_(["shipped", "delivered"]),
                Order.created_at >= today,
            )
        )
        today_revenue = today_revenue_result.scalar() or 0

        month_start = today.replace(day=1)
        month_revenue_result = await self.session.execute(
            select(func.sum(Order.final_amount)).where(
                Order.status.in_(["shipped", "delivered"]),
                Order.created_at >= month_start,
            )
        )
        month_revenue = month_revenue_result.scalar() or 0

        top_game_result = await self.session.execute(
            select(Game).where(Game.is_active == True).order_by(Game.sales.desc()).limit(1)
        )
        top_game = top_game_result.scalar_one_or_none()

        return {
            "users": user_count,
            "orders": order_count,
            "today_income": today_revenue,
            "month_income": month_revenue,
            "top_game": top_game.name if top_game else "نامشخص",
            "online_users": 0,
        }

    async def create_backup(self) -> str | None:
        """Create database backup"""
        try:
            backup_dir = Paths.BACKUP_DIR
            backup_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            db_path = Paths.DATABASE_PATH
            backup_path = backup_dir / f"backup_{timestamp}.db"

            shutil.copy2(str(db_path), str(backup_path))
            return str(backup_path)
        except Exception:
            return None

    async def get_backups(self) -> list[str]:
        """Get list of backups"""
        backup_dir = Paths.BACKUP_DIR
        if not backup_dir.exists():
            return []
        return sorted(
            [str(f) for f in backup_dir.glob("backup_*.db")],
            reverse=True,
        )

    async def restore_backup(self, backup_path: str) -> bool:
        """Restore database from backup"""
        try:
            source = Path(backup_path)
            if not source.exists():
                return False
            shutil.copy2(str(source), str(Paths.DATABASE_PATH))
            return True
        except Exception:
            return False

    async def get_daily_sales(self, days: int = 30) -> list[dict]:
        """Get daily sales data"""
        results = []
        for i in range(days):
            date = datetime.utcnow().date() - timedelta(days=i)
            start = datetime.combine(date, datetime.min.time())
            end = start + timedelta(days=1)

            result = await self.session.execute(
                select(
                    func.count(Order.id),
                    func.sum(Order.final_amount),
                ).where(
                    Order.created_at >= start,
                    Order.created_at < end,
                    Order.status.in_(["shipped", "delivered"]),
                )
            )
            row = result.one()
            results.append({
                "date": date.isoformat(),
                "orders": row[0] or 0,
                "revenue": row[1] or 0,
            })

        return results

    async def get_monthly_sales(self, months: int = 12) -> list[dict]:
        """Get monthly sales data"""
        results = []
        now = datetime.utcnow()
        for i in range(months):
            month_date = now - timedelta(days=30 * i)
            start = month_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if month_date.month == 12:
                end = start.replace(year=start.year + 1, month=1)
            else:
                end = start.replace(month=start.month + 1)

            result = await self.session.execute(
                select(
                    func.count(Order.id),
                    func.sum(Order.final_amount),
                ).where(
                    Order.created_at >= start,
                    Order.created_at < end,
                    Order.status.in_(["shipped", "delivered"]),
                )
            )
            row = result.one()
            results.append({
                "month": start.strftime("%Y-%m"),
                "orders": row[0] or 0,
                "revenue": row[1] or 0,
            })

        return results
