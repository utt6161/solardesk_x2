import functools, sqlite3

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from db_orm import db_orm
from auth_wraps import for_admin
from collections import namedtuple
from yutti.modules.pages.tools.tabs import users_tab, tickets_tab, theme
from models import User,Tickets
from sqlalchemy import desc

bp = Blueprint('admin', __name__, url_prefix='/admin')

Search = namedtuple('Tab',
    [
        'mode',
        'body',
    ])
nosearch = Search(False,'')


@bp.route('/')
@for_admin
def index():
    return render_template('admin/index.html')

records_per_page = 9
@bp.route('/users/')
@bp.route('/users/<int:page>')
@for_admin
def users(page=1):
    # users = get_db().execute(
    #     'SELECT u.id, u.username, u.email, u.first_name, '
    #     'u.last_name, u.middle_name, u.phone_number, u.post, u.active '
    #     'FROM user AS u '
    #     'ORDER BY active ASC'
    # ).fetchall()
    users = User.query.order_by(desc(User.active)).paginate(page, records_per_page, False)
    return render_template('admin/users.html', users=users, tab=users_tab, search=nosearch)





@bp.route('/activate', methods=('POST',))
@for_admin
def activate():
    error = None
    user_id = request.form['userid']
    come_from = request.form['from']

    if user_id is None:
        error = 'Не указан ID пользователя!'

    if error is None:
        # db = get_db()
        # db.execute(
        #     'UPDATE user SET active = 1'
        #     ' WHERE id = ?',
        #     (user_id,)
        # )
        # db.commit()
        db_orm.session.query(User).filter(User.id == user_id).update(
            {User.active: 1})
        db_orm.session.commit()
    message = None
    if error is not None:
        message = 'Произошла ошибка: ' + error
    else:
        message = 'Пользователь активирован!'
    flash(message)

    return redirect(url_for(come_from))


@bp.route('/search', methods=['POST','GET'])
@bp.route('/search/<int:page>', methods=['POST','GET'])
@for_admin
def search(page=1):
    if 'mode' in request.form:
        user_id = g.user.username
        if(request.form['mode']=='l'): #login filter
            users = User.query.filter(User.username.like(r"%{}%".format(request.form['search']))).all()
            search = Search(True, request.form['search'])
            return render_template('admin/search.html', users=users, tab=tickets_tab, search=search)

        elif(request.form['mode']=='e'): #email
            users = User.query.filter(User.email.like((r"%{}%".format(request.form['search'])))).all()
            search = Search(True, request.form['search'])
            return render_template('admin/search.html', users=users, tab=tickets_tab, search=search)

        elif(request.form['mode']=='t'): #tel
            users = User.query.filter(User.phone_number.like((r"%{}%".format(request.form['search'])))).all()
            search = Search(True, request.form['search'])
            return render_template('admin/search.html', users=users, tab=tickets_tab, search=search)

        elif (request.form['mode'] == 'f'): #fio
            users = User.query.filter(User.full_name.like((r"%{}%".format(request.form['search'])))).all()
            search = Search(True, request.form['search'])
            return render_template('admin/search.html', users=users, tab=tickets_tab, search=search)

        elif (request.form['mode'] == 'p'): #firm/post
            users = User.query.filter(User.post.like((r"%{}%".format(request.form['search'])))).all()
            search = Search(True, request.form['search'])
            return render_template('admin/search.html', users=users, tab=tickets_tab, search=search)

        elif (request.form['mode'] == 'a'): #activity
            users = User.query.filter(User.active.like((r"%{}%".format(request.form['search'])))).all()
            search = Search(True, request.form['search'])
            return render_template('admin/search.html', users=users, tab=tickets_tab, search=search)
    else:
        return redirect(url_for('admin.users'))

@bp.route('/test')
@for_admin
def test():
    return 'Yes, you are admin!'

#
# @bp.route('/tickets/search',methods=['GET','POST'])
# @for_admin
# def request_theme_search():
#     if request.method=='POST':
#         tickets = get_db().execute(
#             'SELECT t.id, t.title, t.description, t.status, t.username FROM tickets AS t WHERE LOWER(t.title) LIKE LOWER(?)',
#             (theme,)
#         ).fetchall()
#         return render_template('admin/request_theme_search.html', tickets=tickets, tab=tickets_tab, secondary_tab=theme)
#     return render_template('admin/request_theme_search.html', tab=tickets_tab, secondary_tab=theme)
#

# @bp.route('/tickets_search/<theme>')
# @for_admin
# def request_theme_search_post(theme):
#