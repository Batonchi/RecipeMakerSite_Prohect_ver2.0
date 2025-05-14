from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import desc, select, update
from functools import wraps
import asyncio

router = Blueprint('support', __name__, url_prefix='/support')

from app.web.support.forms import ComplaintForm, BroadcastForm
from app.web.support.service import ComplaintService, BroadcastService
from app.web.support.model import Complaint
from app.base.database import async_session_maker



# Декоратор для асинхронных функций
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


# Декоратор для проверки аутентификации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = request.cookies.get('auth_token')
        if not auth_token:
            flash('Пожалуйста, войдите в систему', 'danger')
            return redirect(url_for('auth.login_page'))
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


@router.route('/create', methods=['GET', 'POST'])
@async_route
@login_required
async def create_complaint():
    form = ComplaintForm()
    if form.validate_on_submit():
        try:
            complaint_data = {
                'user_id': request.cookies.get('user_id'),
                'text': form.text.data,
                'is_solved': False
            }
            await ComplaintService.insert(**complaint_data)
            flash('Ваша жалоба успешно отправлена!', 'success')
            return redirect('/')
        except Exception as e:
            flash(f'Ошибка при отправке жалобы: {str(e)}', 'danger')
    return await render_template('support.html', form=form)


@router.route('/complaints', methods=['GET'])
@async_route
@login_required
async def complaints_list():
    user_id = request.cookies.get('user_id')
    is_admin = request.cookies.get('is_admin') == '1'

    if is_admin:
        async with async_session_maker() as session_db:
            query = select(Complaint).order_by(desc(Complaint.date_pushed))
            result = await session_db.execute(query)
            complaints = result.scalars().all()
    else:
        async with async_session_maker() as session_db:
            query = select(Complaint).where(
                Complaint.user_id == user_id
            ).order_by(desc(Complaint.date_pushed))
            result = await session_db.execute(query)
            complaints = result.scalars().all()

    return await render_template('complaints_list.html',
                                 complaints=complaints,
                                 is_admin=is_admin)


@router.route('/complaints/<int:complaint_id>/solve', methods=['POST'])
@async_route
@login_required
@admin_required
async def solve_complaint(complaint_id):
    try:
        async with async_session_maker() as session_db:
            query = update(Complaint).where(
                Complaint.id == complaint_id
            ).values(is_solved=True)
            await session_db.execute(query)
            await session_db.commit()
        flash('Жалоба отмечена как решенная', 'success')
    except Exception as e:
        flash(f'Ошибка при обновлении жалобы: {str(e)}', 'danger')
    return redirect('recipe/support/complaints_list')


@router.route('/admin/broadcast', methods=['GET', 'POST'])
@async_route
@login_required
@admin_required
async def admin_broadcast():
    form = BroadcastForm()
    if form.validate_on_submit():
        try:
            await BroadcastService.send_broadcast(
                subject=form.subject.data,
                message=form.message.data
            )
            flash('Рассылка успешно отправлена!', 'success')
            return redirect(url_for('support.admin_dashboard'))
        except Exception as e:
            flash(f'Ошибка при отправке рассылки: {str(e)}', 'danger')
    return await render_template('admin_broadcast.html', form=form)


@router.route('/admin/dashboard')
@async_route
@login_required
@admin_required
async def admin_dashboard():
    async with async_session_maker() as session_db:
        total = await ComplaintService.get_count()
        solved = await ComplaintService.get_count(is_solved=True)
        unsolved = await ComplaintService.get_count(is_solved=False)

        query = select(Complaint).order_by(desc(Complaint.date_pushed)).limit(5)
        result = await session_db.execute(query)
        recent_complaints = result.scalars().all()

    return await render_template('admin_dashboard.html',
                                 total_complaints=total,
                                 solved_complaints=solved,
                                 unsolved_complaints=unsolved,
                                 recent_complaints=recent_complaints)