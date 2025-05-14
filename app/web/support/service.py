from app.base.service import BaseService
from app.base.database import async_session_maker
from app.web.support.model import Complaint
from sqlalchemy import select, func

class ComplaintService(BaseService):
    model = Complaint

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

    @classmethod
    def insert_sync(cls, **data):
        with cls.session_maker() as session:
            session.add(cls.model(**data))
            session.commit()

class BroadcastService:
    @classmethod
    async def send_broadcast(cls, subject, message):
        from app.web.users.service import UserService  # Ленивый импорт
        async with async_session_maker() as session:
            users = await UserService.get_all()
            for user in users:
                # Реализация рассылки
                pass
        return True