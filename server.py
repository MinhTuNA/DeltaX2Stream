import socket
# import serial
import threading
from time import sleep

# Thiết lập kết nối serial
# try:
#     ser = serial.Serial(
#         port='/dev/ttyS0',  # Thay đổi thành cổng serial của bạn nếu khác
#         baudrate=115200,
#         parity=serial.PARITY_NONE,
#         stopbits=serial.STOPBITS_ONE,
#         bytesize=serial.EIGHTBITS,
#         timeout=1
#     )
# except serial.SerialException as e:
#     print(f"Error: {e}")
#     exit()


# Thiết lập socket server
ServerIP = "192.168.1.126"
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
        try:
            while True:
                Data = client.recv(buferSize)
                Data_rec = Data.decode('utf-8')
                print(Data_rec)
                client.send(bytesToSend)
        finally:
            client.close()    
thread = threading.Thread(target = ReceiveThread,args=())
thread.start()

while True:
    sleep(1)