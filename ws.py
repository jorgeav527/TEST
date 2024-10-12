from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/ws")
def index():
    return render_template("ws_index.html")

@socketio.on("connect")
def handle_connect():
    sid = request.sid
    print(f"Cliente conectatdo URL-SID: {sid}")
    emit("set_sid", {"sid": sid})


@socketio.on("message")
def handle_message(msg):
    sid = request.sid
    print(f"Mensaje de cliente: {sid}: {msg}")
    send(f"Echo del servidor {sid}: {msg}", broadcast=True)



if __name__ == "__main__":
    socketio.run(app=app, debug=True)