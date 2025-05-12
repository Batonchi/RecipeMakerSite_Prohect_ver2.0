from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import desc, select, update
from app.web.support.forms import ComplaintForm
from app.web.support.model import Complaint
from app.web.users.service import UserService
from app.base.database import async_session_maker

support_router = Blueprint('support', __name__, url_prefix='/support')


@support_router.route('/complaints', methods=['GET'])
@login_required
async def complaints_list():
    # Для администратора - все жалобы, для пользователя - только свои
    if current_user.is_admin:
        async with async_session_maker() as session:
            query = select(Complaint).order_by(desc(Complaint.date_pushed))
            result = await session.execute(query)
            complaints = result.scalars().all()
    else:
        async with async_session_maker() as session:
            query = select(Complaint).where(
                Complaint.user_id == current_user.id
            ).order_by(desc(Complaint.date_pushed))
            result = await session.execute(query)
            complaints = result.scalars().all()

    return render_template('support/complaints_list.html',
                           complaints=complaints,
                           is_admin=current_user.is_admin)


@support_router.route('/complaints/create', methods=['GET', 'POST'])
@login_required
async def create_complaint():
    form = ComplaintForm()
    if form.validate_on_submit():
        try:
            async with async_session_maker() as session:
                new_complaint = Complaint(
                    user_id=current_user.id,
                    text=form.text.data,
                    is_solved=False
                )
                session.add(new_complaint)
                await session.commit()

            flash('Ваша жалоба успешно отправлена!', 'success')
            return redirect(url_for('support.complaints_list'))
        except Exception as e:
            flash(f'Ошибка при отправке жалобы: {str(e)}', 'danger')

    return render_template('support/create_complaint.html', form=form)


@support_router.route('/complaints/<int:complaint_id>/solve', methods=['POST'])
@login_required
async def solve_complaint(complaint_id):
    if not current_user.is_admin:
        flash('Недостаточно прав для выполнения этого действия', 'danger')
        return redirect(url_for('support.complaints_list'))

    try:
        async with async_session_maker() as session:
            query = update(Complaint).where(
                Complaint.id == complaint_id
            ).values(is_solved=True)
            await session.execute(query)
            await session.commit()

        flash('Жалоба отмечена как решенная', 'success')
    except Exception as e:
        flash(f'Ошибка при обновлении жалобы: {str(e)}', 'danger')

    return redirect(url_for('support.complaints_list'))


@support_router.route('/complaints/<int:complaint_id>', methods=['GET'])
@login_required
async def complaint_detail(complaint_id):
    async with async_session_maker() as session:
        query = select(Complaint).where(Complaint.id == complaint_id)
        result = await session.execute(query)
        complaint = result.scalar_one_or_none()

        if not complaint:
            flash('Жалоба не найдена', 'danger')
            return redirect(url_for('support.complaints_list'))

        # Проверка прав доступа
        if not current_user.is_admin and complaint.user_id != current_user.id:
            flash('У вас нет прав для просмотра этой жалобы', 'danger')
            return redirect(url_for('support.complaints_list'))

        # Получаем информацию о пользовате