from flask import Flask, render_template, Response, request, jsonify, redirect
from flask_socketio import SocketIO
import socket
import threading
import os
import subprocess

app = Flask(__name__)
socketio = SocketIO(app)
lock = threading.Lock()
lock_owner = None

SERVER_HOST = '192.168.1.101'
SERVER_PORT = 5000
bufferSize = 1024


TCPClientSocket = socket.socket(family=socket.AF_INET, type = socket.SOCK_STREAM)
TCPClientSocket.connect((SERVER_HOST,SERVER_PORT))

print("Client Start")

@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("home.html")


@app.route("/remote", methods=["POST", "GET"])
def remote():
    global lock_owner
    with lock:
        if lock_owner is None:
            lock_owner = request.remote_addr
            return render_template('remote_deltax2.html')
        elif lock_owner == request.remote_addr:
            if request.method == "POST":
                python_code = request.form.get("python_code")
                if python_code:
                    BytesToSend = str.encode(python_code)
                    TCPClientSocket.send(BytesToSend)
                    return jsonify({'status': 'success', 'message': 'code received and processed'})
                else:
                    return jsonify({'status': 'error', 'message': 'No code received'})
            return render_template('remote_deltax2.html')
        else:
            return redirect('/')
        

@app.route('/check_remote', methods=['POST'])
def check_remote():
    global lock_owner
    with lock:
        if lock_owner is None:
            return jsonify({'status': 'available'})
        else:
            return jsonify({'status': 'occupied'})

@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.remote_addr}")

@socketio.on('disconnect')
def handle_disconnect():
    global lock_owner
    print(f"Client disconnected: {request.remote_addr}")
    if request.remote_addr == lock_owner:
        with lock:
            lock_owner = None
            print("Lock released due to client disconnect")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

