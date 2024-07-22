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

UDPServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)

UDPServerSocket.bind((ServerIP,ServerPort))

print("Server is starting...")

def ReceiveThread():
    while True:
        ByteAddressPair = UDPServerSocket.recvfrom(buferSize)
        Data_rec = ByteAddressPair[0].decode('utf-8')
        address = ByteAddressPair[1]
        print(Data_rec)
        print(address)
        UDPServerSocket.sendto(bytesToSend,address)

thread = threading.Thread(target = ReceiveThread,args=())
thread.start()

while True:
    sleep(1)