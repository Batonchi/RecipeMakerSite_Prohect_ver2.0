from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from sqlalchemy import select
from functools import wraps
import datetime
from app.web.support.forms import ComplaintForm
from app.web.support.model import Complaint
from app.base.database import async_session_maker
from app.web.users.model import User
from app.web.async_utils import async_to_sync

router = Blueprint('support', __name__, url_prefix='/support')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = request.cookies.get('auth_token')
        if not auth_token:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)

    return decorated_function


@router.route('/create', methods=['GET', 'POST'])
@login_required
@async_to_sync
async def create_complaint():
    form = ComplaintForm()

    if request.method == 'GET':
        return render_template('support.html', form=form)

    if not form.validate_on_submit():
        return jsonify({'errors': form.errors}), 400

    try:
        user_id = request.cookies.get('user_id')
        if not user_id:
            return jsonify({'error': 'Пользователь не найден'}), 401

        async with async_session_maker() as session:
            # Проверяем существование пользователя
            user = await session.get(User, int(user_id))
            if not user:
                return jsonify({'error': 'User not found'}), 404

            # Создаем новую жалобу
            complaint = Complaint(
                user_id=int(user_id),
                text=form.text.data,
                is_solved=False,
                date_pushed=datetime.datetime.now()
            )

            session.add(complaint)
            await session.commit()

            return redirect('/')

    except ValueError:
        return jsonify({'error': 'Invalid user ID'}), 400
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@router.route('/my-complaints')
@login_required
@async_to_sync
async def user_complaints():
    user_id = request.cookies.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not identified'}), 401

    try:
        async with async_session_maker() as session:
            query = select(Complaint).where(
                Complaint.user_id == int(user_id)
            ).order_by(Complaint.date_pushed.desc())
            result = await session.execute(query)
            complaints = result.scalars().all()

            complaints_data = [{
                'id': c.id,
                'text': c.text,
                'date_pushed': c.date_pushed.isoformat(),
                'is_solved': c.is_solved
            } for c in complaints]

            return jsonify({'complaints': complaints_data})

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500