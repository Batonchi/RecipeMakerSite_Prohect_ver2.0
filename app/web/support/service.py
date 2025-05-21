from app.base.service import BaseService
from app.base.database import async_session_maker
from app.web.support.model import Complaint
from sqlalchemy import select, func


class ComplaintService(BaseService):
    model = Complaint

    from app.base.service import BaseService
    from app.base.database import async_session_maker
    from app.web.support.model import Complaint
    from sqlalchemy import select, func

    class ComplaintService(BaseService):
        model = Complaint

        @classmethod
        async def insert(cls, **data):
            async with async_session_maker() as session:
                complaint = cls.model(**data)
                session.add(complaint)
                await session.commit()
                await session.refresh(complaint)
                return complaint

    @classmethod
    async def get_user_complaints(cls, user_id):
        return await cls.get_any(user_id=user_id)

    @classmethod
    async def update_complaint_status(cls, complaint_id, status):
        await cls.update({'id': complaint_id}, is_solved=status)

    @classmethod
    async def get_count(cls, **filters):
        async with async_session_maker() as session:
            query = select(func.count()).select_from(cls.model)
            if filters:
                query = query.filter_by(**filters)
            result = await session.execute(query)
            return result.scalar()


class BroadcastService:
    @classmethod
    async def send_broadcast(cls, subject, message):
        from app.web.users.service import UserService
        from app.base.mail import send_email  # Импортируем функцию отправки email

        async with async_session_maker() as session:
            users = await UserService.get_all()
            for user in users:
                if user.email:  # Отправляем только если есть email
                    await send_email(
                        to=user.email,
                        subject=subject,
                        body=message
                    )
        return True