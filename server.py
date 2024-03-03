from socket import SocketIO
from flask_app import app
from flask_app.controllers import users,vets,admins
from flask_socketio import SocketIO, send

socketio = SocketIO(app, cors_allowed_origins="*")

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5050)

