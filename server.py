import socket
import threading
import os
import subprocess
import json
import queue
import time

# Thiết lập socket server
ServerIP = "192.168.1.101"
ServerPort = 5000
bufferSize = 1024

TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCPServerSocket.bind((ServerIP, ServerPort))
TCPServerSocket.listen(5)

CodeQueue = queue.Queue()  # tạo hàng đợi cho code và tên người dùng
NameQueue = queue.Queue()
ClientSockets = {}  # Lưu trữ kết nối client

print("Server is starting...")

def handle_client(client_socket):
    try:
        while True:
            Data = client_socket.recv(bufferSize)
            if not Data:
                break
            Data_recv = Data.decode('utf-8')
            payload = json.loads(Data_recv)
            user_name = payload.get('user')
            python_code = payload.get('python_code')
            if python_code:
                print("đã nhận code của " + user_name)
                CodeQueue.put(python_code)
                NameQueue.put(user_name)
                ClientSockets[user_name] = client_socket  # Lưu trữ kết nối client
                print("đã thêm code của " + user_name + " vào hàng đợi")
    except (ConnectionResetError, BrokenPipeError):
        print(f"Kết nối bị lỗi hoặc bị đóng")
    finally:
        client_socket.close()  # Đảm bảo đóng kết nối client

def ExecuteProgram():
    while True:
        CodeExecute = CodeQueue.get()
        UserName = NameQueue.get()
        if CodeExecute:
            filepath = os.path.join("/home/deltax/DeltaX2Stream", "script.py")
            with open(filepath, "w") as file:
                file.write(CodeExecute)
                print("đang thực thi code của " + UserName)
                DataName = UserName.encode('utf-8')
                
                # Gửi dữ liệu tới client
                if UserName in ClientSockets:
                    client_socket = ClientSockets[UserName]
                    try:
                        client_socket.sendall(DataName)
                        print("đã gửi NameExecute tới client: " + UserName)
                    except BrokenPipeError:
                        print(f"Lỗi BrokenPipeError khi gửi dữ liệu đến {UserName}")
                    except Exception as e:
                        print(f"Lỗi khi gửi dữ liệu: {e}")

                print("code: ")
                print(CodeExecute)
            try:
                result = subprocess.run(["python3", filepath], capture_output=True, text=True)
                if result.stdout:
                    print("Script Output:")
                    print(result.stdout)
                if result.stderr:
                    print("Chương trình lỗi")
                    print(result.stderr)
            except Exception as e:
                print(f"Error executing script: {e}")
        else:
            print("hết code trong hàng đợi")
            time.sleep(1)

def ReceiveThread():
    while True:
        client_socket, addr = TCPServerSocket.accept()
        print(f"Connection from {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

Execute_thread = threading.Thread(target=ExecuteProgram)
Execute_thread.start()

thread = threading.Thread(target=ReceiveThread)
thread.start()
