import socket
import threading
from time import sleep
import os
import subprocess

# Thiết lập socket server
ServerIP = '192.168.1.126'
ServerPort = 5000
buferSize = 1024

msgfromServer = "From Server to"
bytesToSend = str.encode(msgfromServer)

TCPServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM)

TCPServerSocket.bind((ServerIP,ServerPort))
TCPServerSocket.listen(5)

print("Server is starting...")

def ReceiveThread():
    while True:
        client, addr = TCPServerSocket.accept()
        while True:
            Data = client.recv(buferSize) # nhận dữ liệu từ client
            Data_recv = Data.decode('utf-8') # giải mã dữ liệu
            if Data_recv:
                filepath = os.path.join("/home/deltax/DeltaX2Stream", "script.py") # ghi đè file script.py tại đường dẫn....
                with open(filepath, "w") as file:
                    file.write(Data_recv)
                try:
                    # chạy file script
                    result = subprocess.run(["python3", filepath], capture_output=True, text=True)
                    print("Script Output:")
                    print(result.stdout)
                    if result.stderr:
                        print("Script Error:")
                        print(result.stderr)
                except Exception as e:
                    print(f"Error executing script: {e}")
thread = threading.Thread(target = ReceiveThread,args=()) # tạo 1 luồng xử lý việc nhận dữ liệu từ client
thread.start()
