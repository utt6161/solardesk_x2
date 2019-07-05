import functools
from flask import (
    flash, g, redirect, session, url_for
)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('Для доступа необходима авторизация.')
            return redirect(url_for('auth_index.index_auth'))

        return view(**kwargs)

    return wrapped_view


def for_admin(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user:
            flash('Для доступа необходима авторизация.')
            return redirect(url_for('auth_index.index_auth'))
        else:
            if not g.user.position == 'admin':
                flash('Эта функция доступна только администраторам системы!')
                return redirect(url_for('tickets.index'))

        return view(**kwargs)

    return wrapped_view