from flask import (
    Blueprint, render_template, g, request, url_for, redirect, flash
)
from DePaso.db import get_db
from DePaso.auth import login_required

bp = Blueprint('travel',__name__)

@bp.route('/')
def index():
    db = get_db()
    travels = db.execute(
        " SELECT t.id, user_id, price, departure, arrival, departure_time"
        " FROM travel t WHERE departure = ?"
        " ORDER BY created DESC"
    ).fetchall

    return render_template('travel/index.html', travels = travels)

@bp.route('/create_travel', methods = ['POST','GET'])
@login_required
def create_travel():
    if request.method == 'POST':
        departure = request.form['departure']
        arrival = request.form['arrival']
        price = request.form['price']
        departure_time = request.form['departure_time']
        passengers = request.form['passengers']
        error = None

        if not departure:
            error = "There is no departure"
        elif not arrival:
            error = "There is no arrival"
        elif not price:
            error = "Price was not asigned"
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                " INSERT INTO travel (user_id, price, departure, arrival, departure_time, passengers)"
                " VALUES (?,?,?,?)", (g.user['id'], price, departure, arrival, departure_time, passengers)
            )
            db.commit()
            return redirect(url_for('travel.index'))

    return render_template('travel/create.html')

@bp.route('/search_car', methods = ['POST', 'GET'])
def search_car():
    if request.method == 'POST':
        departure = request.form['departure']
        arrival = request.form['arrival']
        departure_time = request.form['departure_time']
        passengers = request.form['passengers']
        error = None

        if not departure:
            error = 'Departure is required'
        elif not arrival:
            error = 'Arrival is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            travels = db.execute(
                " SELECT t.id, departure, arrival, departure_time, passengers, price"
                " FROM travel WHERE departure = ? AND arrival = ? AND departure_time = ?"
                " AND passengers = ?", (departure, arrival, departure_time, passengers)
            ).fetchall()
            return redirect(url_for('search',travels = travels))
    
    return render_template('travel/search_car.html')

