from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from auth_wraps import login_required, for_admin
# from .db import get_db
from db_orm import db_orm
from models import User, Tickets
from collections import namedtuple
from yutti.modules.pages.tools.tabs import tickets_tab
from collections import namedtuple
from sqlalchemy import func

Search = namedtuple('Tab',
                    [
                        'mode',
                        'body',
                    ])
nosearch = Search(False, '')
# nosearch mode in tickets/index.html
records_per_page = 9

bp = Blueprint('tickets', __name__, url_prefix='/tickets')
len_funk = len


@bp.route('/<int:id>')
@login_required
def ticket(id):
    # tickets = get_db().execute('SELECT t.title, t.description, t.id, t.status, t.answer, u.username, t.user_id FROM tickets AS t LEFT JOIN user AS u ON t.user_id = u.id WHERE t.id=?',(id,)).fetchall()
    tickets = Tickets.query.join(User, User.id == Tickets.user_id) \
        .add_columns(Tickets.title, Tickets.description, Tickets.id, Tickets.status, Tickets.answer, User.username,
                     Tickets.user_id) \
        .filter(Tickets.id == id);
    if (tickets[0].username == g.user.username or g.user.position == 'admin'):
        return render_template('tickets/ticket.html', tickets=tickets, tab=tickets_tab)
    else:
        return redirect(url_for('tickets.index'))


@bp.route('/')
@bp.route('/page')
@bp.route('/page/<int:page>')
@login_required
def index(page=1):
    if (g.user.position == 'admin'):
        # tickets = get_db().execute(
        #     'SELECT t.id, t.title,t.description,t.status, u.username FROM tickets AS t LEFT JOIN user AS u ON t.user_id = u.id'
        # ).fetchall()
        tickets = Tickets.query.join(User, User.id == Tickets.user_id) \
            .add_columns(User.username, User.id, User.post, Tickets.id, Tickets.title, Tickets.description,
                         Tickets.status) \
            .paginate(page, records_per_page, False)
        return render_template('tickets/index.html', tickets=tickets, tab=tickets_tab, len=len_funk, search=nosearch)
    else:
        user_id = g.user.username
        # tickets = get_db().execute(
        #     'SELECT t.id, t.title, t.description, t.status, u.username FROM tickets AS t LEFT JOIN user AS u ON t.user_id = u.id WHERE u.username=?', (user_id,)
        # ).fetchall()
        tickets = Tickets.query.join(User, User.id == Tickets.user_id).filter(User.username == user_id).paginate(page,
                                                                                                                 records_per_page,
                                                                                                                 False)
        # for t in tickets:
        #     if(len(t['title'])>20):
        #         t['title'] = t['title'][:20]+'...'
        #     if (len(t['description']) > 50):
        #         t['description'] = t['description'][:50] + '...'

        return render_template('tickets/index.html', tickets=tickets, tab=tickets_tab, len=len_funk, search=nosearch)


@bp.route('/submit', methods=['POST', 'GET'])
@login_required
def submit():
    if (request.method == 'POST'):
        # db = get_db()
        # db.execute('INSERT INTO tickets(user_id, title, description)'
        # 'VALUES(?,?,?)',(g.user['id'],request.form['title'],request.form['description']))
        # db.commit()
        db_orm.session.add(
            Tickets(user_id=g.user.id, title=request.form['title'], description=request.form['description']))
        db_orm.session.commit()
        flash('Заявка успешно добавлена')
        redirect(url_for('tickets.index'))
    return render_template('tickets/submit.html', tab=tickets_tab)


@bp.route('/answer', methods=['POST'])
@for_admin
def answer():
    # db = get_db()
    # db.execute('UPDATE tickets SET answer=?, status=1 WHERE id=?', (request.form['answer'], request.form['id']))
    # db.commit()
    db_orm.session.query(Tickets).filter(Tickets.id == request.form['id']).update({Tickets.answer: request.form['answer'], Tickets.status:1})
    db_orm.session.commit()
    # Tickets.update().where(id==request.form['id']).values(answer=request.form['answer'], status=1)
    flash('Ответ успешно добавлен')
    return redirect(url_for('tickets.index'))


@bp.route('/search', methods=['POST', 'GET'])
@bp.route('/search/<int:page>', methods=['POST', 'GET'])
def search(page=1):
    if 'mode' in request.form:
        user_id = g.user.username
        if (g.user.position == 'admin'):
            if (request.form['mode'] == 't'):
                tickets = Tickets.query.join(User, User.id == Tickets.user_id) \
                    .add_columns(User.username, User.id, User.post, Tickets.id, Tickets.title, Tickets.description,
                                 Tickets.status) \
                    .filter(Tickets.title.like(r"%{}%".format(request.form['search']))).all()

                search = Search(True, request.form['search'])
                return render_template('tickets/search.html', tickets=tickets, tab=tickets_tab, len=len_funk,
                                       search=search)
            elif (request.form['mode'] == 'd'):
                tickets = Tickets.query.join(User, User.id == Tickets.user_id) \
                    .add_columns(User.username, User.id, User.post, Tickets.id, Tickets.title, Tickets.description,
                                 Tickets.status) \
                    .filter(Tickets.description.like(r"%{}%".format(request.form['search']))).all()

                search = Search(True, request.form['search'])
                return render_template('tickets/search.html', tickets=tickets, tab=tickets_tab, len=len_funk,
                                       search=search)
            elif (request.form['mode'] == 's'):
                tickets = Tickets.query.join(User, User.id == Tickets.user_id) \
                    .add_columns(User.username, User.id, User.post, Tickets.id, Tickets.title, Tickets.description,
                                 Tickets.status) \
                    .filter(Tickets.status.like(r"%{}%".format(request.form['search']))).all()

                search = Search(True, request.form['search'])
                return render_template('tickets/search.html', tickets=tickets, tab=tickets_tab, len=len_funk,
                                       search=search)
            elif (request.form['mode'] == 'n'):
                if (g.user.position == 'admin'):
                    tickets = Tickets.query.join(User, User.id == Tickets.user_id) \
                        .add_columns(User.username, User.id, User.post, Tickets.id, Tickets.title, Tickets.description,
                                     Tickets.status) \
                        .filter(
                        Tickets.user_id == User.query.filter(User.username == request.form['search'])[0].id).all()

                    search = Search(True, request.form['search'])
                    return render_template('tickets/search.html', tickets=tickets, tab=tickets_tab, len=len_funk,
                                           search=search)
        else:
            if (request.form['mode'] == 't'):
                tickets = Tickets.query.join(User, User.id == Tickets.user_id) \
                    .add_columns(User.username, User.id, User.post, Tickets.id, Tickets.title, Tickets.description,
                                 Tickets.status) \
                    .filter(Tickets.title.like(r"%{}%".format(request.form['search']))).filter(
                    Tickets.user_id == g.user.id).all()

                search = Search(True, request.form['search'])
                return render_template('tickets/search.html', tickets=tickets, tab=tickets_tab, len=len_funk,
                                       search=search)
            elif (request.form['mode'] == 'd'):
                tickets = Tickets.query.join(User, User.id == Tickets.user_id) \
                    .add_columns(User.username, User.id, User.post, Tickets.id, Tickets.title, Tickets.description,
                                 Tickets.status) \
                    .filter(Tickets.description.like(r"%{}%".format(request.form['search']))).filter(
                    Tickets.user_id == g.user.id).all()

                search = Search(True, request.form['search'])
                return render_template('tickets/search.html', tickets=tickets, tab=tickets_tab, len=len_funk,
                                       search=search)
            elif (request.form['mode'] == 's'):
                tickets = Tickets.query.join(User, User.id == Tickets.user_id) \
                    .add_columns(User.username, User.id, User.post, Tickets.id, Tickets.title, Tickets.description,
                                 Tickets.status) \
                    .filter(Tickets.status.like(r"%{}%".format(request.form['search']))).filter(
                    Tickets.user_id == g.user.id).all()

                search = Search(True, request.form['search'])
                return render_template('tickets/search.html', tickets=tickets, tab=tickets_tab, len=len_funk,
                                       search=search)
            elif (request.form['mode'] == 'n'):
                if (g.user.position == 'admin'):
                    tickets = Tickets.query.join(User, User.id == Tickets.user_id) \
                        .add_columns(User.username, User.id, User.post, Tickets.id, Tickets.title, Tickets.description,
                                     Tickets.status) \
                        .filter(
                        Tickets.user_id == User.query.filter(User.username == request.form['search'])[0].id).filter(
                        Tickets.user_id == g.user.id).all()

                    search = Search(True, request.form['search'])
                    return render_template('tickets/search.html', tickets=tickets, tab=tickets_tab, len=len_funk,
                                           search=search)

    else:
        return redirect(url_for('tickets.index'))
