from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import desc, select, update
from functools import wraps
import asyncio
import datetime
from app.web.support.forms import ComplaintForm, BroadcastForm
from app.web.support.service import ComplaintService, BroadcastService
from app.web.support.model import Complaint
from app.base.database import async_session_maker
from app.web.users.model import User

router = Blueprint('support', __name__, url_prefix='/support')


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
            user_id = request.cookies.get('user_id')
            if not user_id:
                flash('Не удалось определить пользователя', 'danger')
                return redirect('recipe/auth/login')

            # Создаем новую сессию для проверки пользователя
            async with async_session_maker() as session:
                # Проверяем существование пользователя
                user_exists = await session.execute(
                    select(User).where(User.id == int(user_id)))
                if not user_exists.scalar():
                    flash('Пользователь не найден', 'danger')
                    return redirect('recipe/auth/login')
                # Закрываем текущую сессию перед созданием новой
                await session.close()

                # Создаем данные для жалобы
                complaint_data = {
                    'user_id': int(user_id),
                    'text': form.text.data,
                    'is_solved': form.is_solved.data,
                    'date_pushed': datetime.datetime.now()
                }

                # Используем отдельную сессию для вставки
                await ComplaintService.insert(**complaint_data)

                flash('Ваша жалоба успешно отправлена!', 'success')
                return redirect('/recipe')

        except ValueError as e:
            flash(f'Ошибка в данных: {str(e)}', 'danger')
        except Exception as e:
            flash(f'Ошибка при отправке жалобы: {str(e)}', 'danger')

    return render_template('support.html', form=form)


@router.route('/admin/complaints')
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

        return render_template('admin_complaints.html',
                               complaints=complaints,
                               total_complaints=total,
                               solved_complaints=solved,
                               unsolved_complaints=unsolved)


@router.route('/admin/broadcast', methods=['GET', 'POST'])
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
            return redirect(url_for('support.admin_complaints'))
        except Exception as e:
            flash(f'Ошибка при отправке рассылки: {str(e)}', 'danger')
    return render_template('admin_broadcast.html', form=form)