import socket
import threading
import os
import subprocess

# Thiết lập socket server
ServerIP = "192.168.1.101"
ServerPort = 5000
bufferSize = 1024

msgfromServer = "From Server to"
bytesToSend = str.encode(msgfromServer)

TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCPServerSocket.bind((ServerIP, ServerPort))
TCPServerSocket.listen(5)

print("Server is starting...")

def handle_client(client_socket):
    try:
        while True:
            Data = client_socket.recv(bufferSize)
            if not Data:
                break  # Ngắt kết nối nếu không còn dữ liệu
            Data_recv = Data.decode('utf-8')
            if Data_recv:
                filepath = os.path.join("/home/deltax/DeltaX2Stream", "script.py")
                with open(filepath, "w") as file:
                    file.write(Data_recv)
                try:
                    result = subprocess.run(["python3", filepath], capture_output=True, text=True)
                    print("Script Output:")
                    print(result.stdout)
                    if result.stderr:
                        print("Script Error:")
                        print(result.stderr)
                except Exception as e:
                    print(f"Error executing script: {e}")
    finally:
        client_socket.close()  # Đảm bảo đóng kết nối client

def ReceiveThread():
    while True:
        client_socket, addr = TCPServerSocket.accept()
        print(f"Connection from {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

thread = threading.Thread(target=ReceiveThread)
thread.start()
