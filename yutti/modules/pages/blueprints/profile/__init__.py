import functools, sqlite3
from db import get_db
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from models import User, Tickets
from db_orm import db_orm
from auth_wraps import login_required, for_admin
from yutti.modules.pages.tools.tabs import users_tab

bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/user_id<int:id>')
@login_required
def index(id):
    # user = get_db().execute('SELECT u.email, u.username, u.id, u.phone_number, u.full_name FROM user AS u WHERE u.id=?',(id,)).fetchall()

    user = User.query.add_columns(User.email, User.username, User.id, User.phone_number, User.full_name).filter(
        User.id == id)
    return render_template('profile/index.html', user=user, tab=users_tab)


@bp.route('/user_edit/<int:id>', methods=['POST', 'GET'])
@login_required
@for_admin
def edit_user(id):
    if request.method == 'POST':
        email = request.form['email']
        phone_number = request.form['phone_number']
        post = request.form['post']
        # db = get_db()
        # db.execute('UPDATE user SET email = ?, phone_number=?, post=? WHERE id=?',
        #             (email,phone_number,post, id))
        # db.commit()

        db_orm.session.query(User).filter(User.id == id).update(
            {User.email: email, User.phone_number: phone_number, User.post: post})
        db_orm.session.commit()

        flash('Данные успешно обновлены.')
        
    # user = get_db().execute(
    #     'SELECT u.email, u.username, u.id, u.phone_number, u.full_name, u.post FROM user AS u WHERE u.id=?',
    #     (id,)).fetchall()

    user = User.query.add_columns(User.email, User.username, User.id, User.phone_number, User.full_name,
                                  User.post).filter(User.id == id)
    return render_template('profile/edit.html', tab=users_tab, id=id, user=user)


@bp.route('/edit')
@login_required
def edit():
    return render_template('profile/edit.html')
