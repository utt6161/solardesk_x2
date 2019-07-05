import functools, sqlite3
import redis
from auth_wraps import login_required, for_admin
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from db_orm import db_orm
from models import User, Tickets
from yutti.modules.pages.tools.login import RegisterForm
from yutti.modules.pages.tools.login import LoginForm

from collections import namedtuple

bp = Blueprint('auth_index', __name__, url_prefix="/")

Tab = namedtuple('Tab',
    [
        'li_div_register',
        'aria_selecter_register',
        'li_div_login',
        'aria_selecter_login',
    ])
register_tab = Tab('active show', 'true', '', 'false')
login_tab = Tab('', 'false', 'active show', 'true')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter(User.id==user_id).first()


@bp.route('/', methods=('GET','POST'))
def index_auth():
    if g.user != None:
        return redirect(url_for('tickets.index'))
    register_form = RegisterForm()
    login_form = LoginForm()
    if request.method == 'POST':
        if request.form['btn'] == 'reg':
            if register_form.validate_on_submit():

                error = None

                if User.query.filter(User.username==register_form.username.data).first() is not None:
                    error = 'Пользователь {} уже существует.'.format(register_form.username.data)
                    flash(error)
                    return render_template('auth/index_auth.html', login_form=login_form, register_form=register_form,
                                           tab=register_tab)

                if User.query.filter(User.email==register_form.email.data).first() is not None:
                    error = 'Пользователь c таким email уже существует.'
                    flash(error)
                    return render_template('auth/index_auth.html', login_form=login_form, register_form=register_form,
                                           tab=register_tab)

                if User.query.filter(User.phone_number==register_form.phone_number.data).first() is not None:
                    error = 'Пользователь c таким номером телефона уже существует.'
                    flash(error)
                    return render_template('auth/index_auth.html', login_form=login_form, register_form=register_form,
                                           tab=register_tab)

                db_orm.session.add(User(username=register_form.username.data,
                                     password=generate_password_hash(register_form.password.data),
                                     email=register_form.email.data,
                                     phone_number=register_form.phone_number.data,
                                     full_name=register_form.last_name.data + " " +  register_form.first_name.data + " " + register_form.middle_name.data))
                db_orm.session.commit()
                flash('Регистрация произведена успешно, ожидайте верификации ваших данных.')
                return render_template('auth/index_auth.html', login_form=login_form, register_form=register_form, tab=login_tab)
            else:
                return render_template('auth/index_auth.html', login_form=login_form, register_form=register_form, tab=register_tab)
        else:
            if login_form.validate_on_submit():
                error = None

                user = User.query.add_columns(User.id, User.username, User.active, User.password).filter(User.username==login_form.username.data).first()

                if (user is None) or (not check_password_hash(user.password, login_form.password.data)):
                    error = 'Неправильный логин или пароль, перепроверьте данные еще раз'
                elif user.active == 0:
                    error = 'Данная учетная запись еще не была верифицирована администратором системы.'

                if error is None:
                    session.clear()
                    session['user_id'] = user.id
                    return redirect(url_for('tickets.index'))

                flash(error)
            else:
                flash('validate_on_submit вернул false')
                return render_template('auth/index_auth.html', login_form=login_form, register_form=register_form, tab=login_tab)
    return render_template('auth/index_auth.html', login_form=login_form, register_form=register_form, tab=login_tab)




@bp.route('/logout')
def logout():
    session['user_id'] = None
    return redirect(url_for('auth_index.index_auth'))



