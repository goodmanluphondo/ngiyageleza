import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.database import get_database

blueprint = Blueprint('authentication', __name__, url_prefix='/authentication')

@blueprint.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        database = get_database()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif database.execute(
            'SELECT ID FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
        

        if error is None:
            database.execute(
                'INSERT INTO user (username, password) VALUE(?, ?)', (username, generate_password_hash(password))
            )
            database.commit()
            return redirect(url_for('auth.login'))
        
        flash(error)
    
    return render_template('templates/register.html')
    