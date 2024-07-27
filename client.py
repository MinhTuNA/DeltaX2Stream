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

SERVER_HOST = "192.168.1.101" # ip server
SERVER_PORT = 5000 # port server
bufferSize = 1024 # kích thước tối đa dữ liệu truyền nhận


TCPClientSocket = socket.socket(family=socket.AF_INET, type = socket.SOCK_STREAM)
TCPClientSocket.connect((SERVER_HOST,SERVER_PORT)) # kết nối tới server

print("Client Start")

@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("home.html")

# route xử lý code python trên web
@app.route("/remote", methods=["POST", "GET"])
def remote():
    global lock_owner
    with lock:
        if lock_owner is None:
            lock_owner = request.remote_addr
            return render_template('remote_deltax2.html')
        elif lock_owner == request.remote_addr:
            if request.method == "POST":
                python_code = request.form.get("python_code") # nhận dữ liệu từ name: python_code trong form html
                if python_code:
                    BytesToSend = str.encode(python_code) # mã hóa dữ liệu
                    TCPClientSocket.send(BytesToSend) # gửi dữ liệu tới server
                    return jsonify({'status': 'success', 'message': 'đã nhận code và gửi tới server'})
                else:
                    return jsonify({'status': 'error', 'message': 'lỗi'})
            return render_template('remote_deltax2.html')
        else:
            return redirect('/')
        
# route xử lý file script tải lên        
@app.route('/upload', methods=['POST']) 
def upload():
    file = request.files.get('file')
    if file and file.filename.endswith('.py'):
        filepath = os.path.join('/tmp', file.filename)
        file.save(filepath)

        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(bufferSize)
                if not chunk:
                    break
                TCPClientSocket.sendall(chunk)
        return jsonify({'message': 'File đã được gửi tới server'}), 200
    return jsonify({'message': 'Vui lòng upload file python'}), 400

    
# route kiểm tra trạng thái truy cập
@app.route('/check_remote', methods=['POST'])
def check_remote():
    global lock_owner
    with lock:
        if lock_owner is None:
            return jsonify({'status': 'available'})
        else:
            return jsonify({'status': 'occupied'})

# hiện địa chỉ ip khi có truy cập    
@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.remote_addr}")

# khi ngắt kết nối giải phóng, cho phép người khác truy cập
@socketio.on('disconnect')
def handle_disconnect():
    global lock_owner
    print(f"Client disconnected: {request.remote_addr}")
    if request.remote_addr == lock_owner:
        with lock:
            lock_owner = None
            print("Lock released due to client disconnect")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001,debug=True)