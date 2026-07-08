"""
Ticket service - handles support tickets
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.ticket import Ticket, TicketMessage


class TicketService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_ticket(self, user_id: int, subject: str = "تیکت پشتیبانی") -> Ticket:
        """Create a new ticket"""
        ticket = Ticket(user_id=user_id, subject=subject)
        self.session.add(ticket)
        await self.session.commit()
        await self.session.refresh(ticket)
        return ticket

    async def get_ticket(self, ticket_id: int) -> Ticket | None:
        """Get ticket by ID"""
        result = await self.session.execute(
            select(Ticket).where(Ticket.id == ticket_id)
        )
        return result.scalar_one_or_none()

    async def get_user_tickets(self, user_id: int) -> list[Ticket]:
        """Get user's tickets"""
        result = await self.session.execute(
            select(Ticket)
            .where(Ticket.user_id == user_id)
            .order_by(Ticket.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_open_tickets(self) -> list[Ticket]:
        """Get all open tickets"""
        result = await self.session.execute(
            select(Ticket)
            .where(Ticket.status == "open")
            .order_by(Ticket.created_at.desc())
        )
        return list(result.scalars().all())

    async def add_message(
        self, ticket_id: int, sender_id: int, message: str, is_admin: bool = False
    ) -> TicketMessage:
        """Add message to ticket"""
        msg = TicketMessage(
            ticket_id=ticket_id,
            sender_id=sender_id,
            message=message,
            is_admin=is_admin,
        )
        self.session.add(msg)
        await self.session.commit()
        await self.session.refresh(msg)
        return msg

    async def get_ticket_messages(self, ticket_id: int) -> list[TicketMessage]:
        """Get all messages for a ticket"""
        result = await self.session.execute(
            select(TicketMessage)
            .where(TicketMessage.ticket_id == ticket_id)
            .order_by(TicketMessage.created_at.asc())
        )
        return list(result.scalars().all())

    async def close_ticket(self, ticket_id: int) -> bool:
        """Close a ticket"""
        ticket = await self.get_ticket(ticket_id)
        if ticket:
            ticket.status = "closed"
            await self.session.commit()
            return True
        return False

    async def get_ticket_count(self, status: str | None = None) -> int:
        """Get ticket count"""
        query = select(Ticket)
        if status:
            query = query.where(Ticket.status == status)
        result = await self.session.execute(query)
        return len(result.scalars().all())
