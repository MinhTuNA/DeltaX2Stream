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

ExcuteName = None # tên người đang thực thi chương trình

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

@app.route('/hdsd')
def hdsd():
    return render_template('hdsd.html')

# route xử lý code python trên web
@app.route("/remote", methods=["POST", "GET"])
def remote():
    global ExcuteName
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
    global lock_owner
    if "user" in session:
        name = session["user"]
        file = request.files.get('file')
        if file and file.filename.endswith('.py'):
            filepath = os.path.join('/tmp', file.filename)
            file.save(filepath)
            with open(filepath, 'rb') as f:
                while True:
                    chunk = f.read(bufferSize)
                    if not chunk:
                        break
                    payload = {
                        'user': name,
                        'python_code': chunk.decode("utf-8")
                    }
                    payload_json = json.dumps(payload)
                    payload_bytes = payload_json.encode('utf-8')
                    TCPClientSocket.sendall(payload_bytes)
                    print("đã gửi code của "+name+" tới server")
        return render_template("remote_deltax2.html",user = name)


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/get_execute_name')
def get_execute_name():
    global ExcuteName
    return jsonify({'ExecuteName': ExcuteName})

def receive_messages():
    global ExcuteName
    while True:
        try:
            message = TCPClientSocket.recv(bufferSize)
            if message:
                ExcuteName = message.decode('utf-8')
                print(f"Code của: {ExcuteName} đang được thực thi")
        except:
            break


if __name__ == '__main__':
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()
    socketio.run(app, host='0.0.0.0', port=8264)