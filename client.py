from flask import Flask, render_template, url_for, request, jsonify, redirect,send_from_directory,session
from flask_socketio import SocketIO
import socket
import threading
import os
import json

app = Flask(__name__)
app.secret_key = 'ronaldo'
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
    if request.method == 'POST':
        user_name = request.form["username"]
        if user_name:
            session["user"] = user_name
            return redirect("/remote")
    return render_template("home.html")

# route xử lý code python trên web
@app.route("/remote", methods=["POST", "GET"])
def remote():
    global lock_owner
    if "user" in session:
        name = session["user"]
        if request.method == "POST":
            data = request.get_json()  # Nhận dữ liệu từ name: python_code trong form HTML
            python_code = data.get("python_code")
            if python_code:
                payload = {
                    'user': name,
                    'python_code': python_code
                }
                print(payload)
                json_payload = json.dumps(payload)
                BytesToSend = json_payload.encode('utf8')  # Mã hóa dữ liệu thành dạng byte
                TCPClientSocket.sendall(BytesToSend)  # Gửi dữ liệu tới server
                print("đã gửi code của "+name+" tới server")
                return render_template('remote_deltax2.html')
            else:
                return render_template('remote_deltax2.html')
        return render_template("remote_deltax2.html", user=name)
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
    return render_template('remote_deltax2.html')


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)




if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8264)