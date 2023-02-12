import os
from flask import Flask
from . import db, auth
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)
    app.instance_path = os.path.join(os.getcwd(), "DePaso\instance")
    app.config.from_mapping(
        SECRET_KEY = 'key',
        DATABASE = os.path.join(app.instance_path, "databases.sqlite")
    )
    
    if test_config is None:
        app.config.from_pyfile('config.py',silent = True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.add_url_rule('/',endpoint='index')
    
    from . import chat
    app.register_blueprint(chat.bp)
    socketio.init_app(app)
    if __name__ == '__main__':
        socketio.run(app)
        
    return app
    