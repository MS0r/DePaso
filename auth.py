from flask import (
    render_template, g, session, redirect, url_for, request, Blueprint, flash   
)
from werkzeug.security import check_password_hash, generate_password_hash
from DePaso.db import get_db
import functools

bp = Blueprint('auth',__name__)

@bp.route('/register', methods = ['POST','GET'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['pass1']
        repassword = request.form['repass']
        postal = request.form['postal']

        db = get_db()
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif password != repassword:
            error = 'Password is not the same'

        if error is None:
            try:
                db.execute("INSERT INTO user (username,password,email,postal) VALUES (?,?,?,?)",
                    (username,generate_password_hash(password),email,postal)
                )
                db.commit() 
            except db.IntegrityError:
                error = f" User {username} is already registered"
            else:
                return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html', error = error)
    
@bp.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass1']
        db = get_db()
        error = None
        user = db.execute("SELECT * FROM user WHERE email = ?", (email,)).fetchone()

        if user is None or not check_password_hash(user['password'],password):
            error = 'Either username or password are wrong, try it again'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
    
        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?",(user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)

    return wrapped_view