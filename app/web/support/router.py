from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import select
from functools import wraps
import datetime
from app.web.support.forms import ComplaintForm
from app.web.support.model import Complaint
from app.base.database import async_session_maker
from app.web.users.model import User
from app.web.async_utils import async_to_sync

router = Blueprint('support', __name__, url_prefix='/support')


# Декоратор для проверки аутентификации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = request.cookies.get('auth_token')
        if not auth_token:
            flash('Пожалуйста, войдите в систему', 'danger')
            return redirect('recipe/auth/login_page')
        return f(*args, **kwargs)

    return decorated_function


# Декоратор для проверки прав администратора
# def admin_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         is_admin = request.cookies.get('is_admin') == '1'
#         if not is_admin:
#             flash('Недостаточно прав для этого действия', 'danger')
#             return redirect(url_for('index'))
#         return f(*args, **kwargs)
#
#     return decorated_function


@router.route('/create', methods=['GET', 'POST'])
@login_required
@async_to_sync
async def create_complaint():
    form = ComplaintForm()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            user_id = request.cookies.get('user_id')
            if not user_id:
                flash('Не удалось определить пользователя', 'danger')
                return redirect('recipe/auth/login')

            async with async_session_maker() as session:
                user_exists = await session.execute(
                    select(User).where(User.id == int(user_id)))
                if not user_exists.scalar():
                    flash('Пользователь не найден', 'danger')
                    return redirect('recipe/auth/login')

                complaint = Complaint(
                    user_id=int(user_id),
                    text=form.text.data,
                    is_solved=False,
                    date_pushed=datetime.datetime.now()
                )

                session.add(complaint)
                await session.commit()
                await session.refresh(complaint)

                flash('Ваша жалоба успешно отправлена!', 'success')
                return redirect('/')

        except Exception as e:
            flash(f'Ошибка при отправке жалобы: {str(e)}', 'danger')

    return render_template('support.html', form=form)


# @router.route('/admin/complaints')
# @async_route
# @login_required
# @admin_required
# async def admin_complaints():
#     async with async_session_maker() as session:
#         # Получаем только нерешенные жалобы
#         query = select(Complaint).where(
#             Complaint.is_solved == False
#         ).order_by(desc(Complaint.date_pushed))
#
#         result = await session.execute(query)
#         complaints = result.scalars().all()
#
#         # Получаем статистику
#         total = await ComplaintService.get_count()
#         solved = await ComplaintService.get_count(is_solved=True)
#         unsolved = await ComplaintService.get_count(is_solved=False)
#
#         return render_template('admin_complaints.html',
#                                complaints=complaints,
#                                total_complaints=total,
#                                solved_complaints=solved,
#                                unsolved_complaints=unsolved)
#
#
# @router.route('/admin/broadcast', methods=['GET', 'POST'])
# @async_route
# @login_required
# @admin_required
# async def admin_broadcast():
#     form = BroadcastForm()
#     if form.validate_on_submit():
#         try:
#             success = await BroadcastService.send_broadcast(
#                 subject=form.subject.data,
#                 message=form.message.data
#             )
#             if success:
#                 flash('Рассылка успешно отправлена!', 'success')
#             else:
#                 flash('Произошла ошибка при отправке', 'warning')
#             return redirect(url_for('support.admin_complaints'))
#         except Exception as e:
#             flash(f'Ошибка при отправке рассылки: {str(e)}', 'danger')
#     return render_template('admin_broadcast.html', form=form)