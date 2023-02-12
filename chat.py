from flask import Blueprint, session, redirect, url_for, render_template, request
from flask_socketio import join_room, leave_room, emit
from . import socketio

bp = Blueprint('chat',__name__)

@bp.route('/room', methods = ['POST', 'GET'])
def room():
    if request.method == 'POST':
        session['name'] = request.form['username']
        session['room'] = request.form['room']
        return redirect(url_for('chat.chat'))
    return render_template('chat/index_chat.html')

@bp.route('/chat')
def chat():
    name = session.get('name')
    room = session.get('room')
    return render_template('chat/chat.html', name = name, room = room)

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)