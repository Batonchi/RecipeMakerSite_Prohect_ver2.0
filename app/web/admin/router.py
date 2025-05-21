from flask import Blueprint, render_template, redirect, url_for,\
    flash, request
from sqlalchemy import desc, select
from functools import wraps
import asyncio
from app.base.database import async_session_maker
from app.web.support.model import Complaint
from app.web.support.service import ComplaintService, BroadcastService
from app.web.support.forms import BroadcastForm


router = Blueprint('admin', __name__, url_prefix='/admin')


def async_route(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(f(*args, **kwargs))
            return result
        finally:
            loop.close()

    return wrapper


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = request.cookies.get('auth_token')
        if not auth_token:
            flash('Пожалуйста, войдите в систему', 'danger')
            return redirect(url_for('recipe/auth/login'))
        return f(*args, **kwargs)

    return decorated_function


# Декоратор для проверки прав администратора
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        is_admin = request.cookies.get('is_admin') == '1'
        if not is_admin:
            flash('Недостаточно прав для этого действия', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)

    return decorated_function


@router.route('/complaints')
@async_route
@login_required
@admin_required
async def admin_complaints():
    async with async_session_maker() as session:
        # Получаем только нерешенные жалобы
        query = select(Complaint).where(
            Complaint.is_solved == False
        ).order_by(desc(Complaint.date_pushed))

        result = await session.execute(query)
        complaints = result.scalars().all()

        # Получаем статистику
        total = await ComplaintService.get_count()
        solved = await ComplaintService.get_count(is_solved=True)
        unsolved = await ComplaintService.get_count(is_solved=False)

        return render_template('admin/complaints.html',
                               complaints=complaints,
                               total_complaints=total,
                               solved_complaints=solved,
                               unsolved_complaints=unsolved)


@router.route('/broadcast', methods=['GET', 'POST'])
@async_route
@login_required
@admin_required
async def admin_broadcast():
    form = BroadcastForm()
    if form.validate_on_submit():
        try:
            success = await BroadcastService.send_broadcast(
                subject=form.subject.data,
                message=form.message.data
            )
            if success:
                flash('Рассылка успешно отправлена!', 'success')
            else:
                flash('Произошла ошибка при отправке', 'warning')
            return redirect(url_for('admin.admin_complaints'))
        except Exception as e:
            flash(f'Ошибка при отправке рассылки: {str(e)}', 'danger')
    return render_template('broadcast.html', form=form)

