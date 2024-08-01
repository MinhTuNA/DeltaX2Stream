import serial
import time

class GCodeCommand:
    def __init__(self, command_type, F=None, X=None, Y=None, Z=None, W=None, I=None, J=None, P=None, Q = None, S=None, A=None, E = None, R = None):
        """
        Khởi tạo đối tượng GCodeCommand với các tham số tùy chọn cho các lệnh GCode.

        :param command_type: Loại lệnh GCode (ví dụ: "G00", "M03").
        :param F: Tốc độ di chuyển (chỉ áp dụng cho một số lệnh).
        :param X: Tọa độ X.
        :param Y: Tọa độ Y.
        :param Z: Tọa độ Z.
        :param W: Tọa độ W.
        :param I: Tham số I cho các lệnh cung tròn.
        :param J: Tham số J cho các lệnh cung tròn.
        :param P: Tham số P (thường dùng cho thời gian dừng và độ dài nội suy).
        :param S: Tham số S (thường dùng cho nhiệt độ hoặc đầu ra).
        :param A: Tham số A (dùng cho gia tốc trong lệnh M204).
        :param E: Tham số E (dùng cho thay đổi bộ phận hiệu ứng trong lệnh M360).
        :param R: Tham số R (dùng cho chọn thiết bị liên kết với cổng uart bên ngoài M331).
        :
        """
        # Kiểm tra loại lệnh có hợp lệ không
        valid_commands = {
            "G00": ["F"],
            "G01": ["X", "Y", "Z"],
            "G02": ["X", "Y", "I", "J"],
            "G03": ["X", "Y", "I", "J"],
            "G04": ["P"],
            "G05": ["I", "J", "P", "Q", "X", "Y"],
            "G06": ["X", "Y", "Z", "P"],
            "G28": [],
            "G90": [],
            "G91": [],
            "G93": [],
            "M03": ["S"],
            "M05": [],
            "M84": [],
            "M104": ["S"],
            "M105": [],
            "M109": ["S"],
            "M203": ["S"],
            "M204": ["A"],
            "M205": ["S"],
            "M206": ["X", "Y", "Z"],
            "M331": ["R"],
            "M360": ["E"],
            "M361": ["P"],
            "M362": ["P"],
            "M402": ["Z"],
            "M500": [],
            "M501": [],
            "M502": []
        }
        if command_type not in valid_commands:
            raise ValueError("Invalid command type. Use appropriate command types.")
        self.command_type = command_type
        self.F = F
        self.X = X
        self.Y = Y
        self.Z = Z
        self.W = W
        self.I = I
        self.J = J
        self.P = P
        self.S = S
        self.A = A
        self.E = E
        self.R = R
        self.Q = Q  

    def __str__(self):
        """
        Chuyển đổi đối tượng GCodeCommand thành chuỗi lệnh GCode.

        :return: Chuỗi lệnh GCode.
        """
        command = f"{self.command_type}"
        if self.F is not None:
            command += f" F{self.F}"
        if self.X is not None:
            command += f" X{self.X}"
        if self.Y is not None:
            command += f" Y{self.Y}"
        if self.Z is not None:
            command += f" Z{self.Z}"
        if self.W is not None:
            command += f" W{self.W}"
        if self.I is not None:
            command += f" I{self.I}"
        if self.J is not None:
            command += f" J{self.J}"
        if self.P is not None:
            command += f" P{self.P}"
        if self.S is not None: 
            command += f" S{self.S}"
        if self.A is not None and self.command_type == "M204":  # A only for M204
            command += f" A{self.A}"
        if self.E is not None:
            command += f" E{self.E}"
        if self.R is not None:
            command += f" R{self.R}"
        if self.Q is not None:
            command += f" Q{self.Q}"
        return command

class Deltax2Cmd:
    def __init__(self):
        """
        Khởi tạo đối tượng Deltax2Cmd với các thuộc tính mặc định.
        Khởi tạo UART0
        """
        try:
            self.ser = serial.Serial(
                port='/dev/ttyS0', 
                baudrate=115200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
            )
        except serial.SerialException as e:
            print(f"Error initializing serial port: {e}")
            exit()
        
        self.command_history = []

    def execute_command(self, command):
        """
        Thực thi lệnh GCode và lưu vào lịch sử lệnh.
        gửi lệnh ra uart
        """
        cmd = str(command) + "\n"
        self.ser.write(cmd.encode('utf-8'))
        self.ser.flush()
        print(f"Sent: {cmd.strip()}")
        # nếu là các lệnh di chuyển không cần đợi phản hồi từ DeltaX2
        if command.command_type in ["G01", "G02", "G03","G04", "G05", "G06"]: 
            self.command_history.append(str(command))
            time.sleep(0.7) # đợi 1 lúc để deltaX2 thực hiện lệnh
            return
        # đợi DeltaX2 phản hồi
        wait = 1
        while wait<=10:
            received_data = self.ser.readline().decode('utf-8')
            wait+=1
            time.sleep(0.1)
            if received_data:
                print(received_data)
                received_data = ""
                break
        self.command_history.append(str(command))
        
        
    def MoveTo(self, X=None, Y=None, Z=None):
        """
        Thực hiện di chuyển (G01) đến tọa độ chỉ định với tốc độ tùy chọn.

        :param X: Tọa độ X.
        :param Y: Tọa độ Y.
        :param Z: Tọa độ Z.
        """
        command = GCodeCommand("G01", X=X, Y=Y, Z=Z)
        self.execute_command(command)

    def SetSpeed(self,F = None):
        """
        :param F: Thiết lập tốc độ di chuyển
        """
        command = GCodeCommand("G00",F = F)
        self.execute_command(command)

    def ArcMove(self, command_type, X=None, Y=None, I=None, J=None):
        """
        Thực hiện di chuyển cung tròn (G02 hoặc G03) đến tọa độ chỉ định với các tham số tùy chọn.

        :param command_type: Loại cung tròn (1 cho CW, 0 cho CCW).
        :param X: Tọa độ X.
        :param Y: Tọa độ Y.
        :param Z: Tọa độ Z.
        :param W: Tọa độ W.
        :param I: Tham số I.
        :param J: Tham số J.
        :param F: Tốc độ di chuyển.
        """
        if command_type not in [1, 0]:
            raise ValueError("Invalid command type for arc move. Use 1 for CW or 0 for CCW.")
        elif command_type == 1:
            command = GCodeCommand("G02", X = X, Y = Y, I = I, J = J)
        elif command_type == 0:
            command = GCodeCommand("G03", X = X, Y = Y, I = I, J = J)
        self.execute_command(command)

    def Delay(self, time):
        """
        Thực hiện lệnh dừng (G04) để tạm dừng trong thời gian chỉ định (tính bằng mili giây).

        :param time: Thời gian dừng (mili giây).
        """
        command = GCodeCommand("G04", P=time)
        self.execute_command(command)

    def BezierSpline(self, I=None, J=None, P=None, Q=None, X=None, Y=None):
        """
        Thực hiện lệnh Bezier cubic spline (G05) đến tọa độ chỉ định với các tham số tùy chọn.

        :param I: Tham số I.
        :param J: Tham số J.
        :param P: Tham số P.
        :param Q: Tham số Q.
        :param X: Tọa độ X.
        :param Y: Tọa độ Y.
        :param F: Tốc độ di chuyển.
        """
        command = GCodeCommand("G05", I = I, J = J, P = P, Q = Q, X = X, Y = Y)
        self.execute_command(command)

    def ThetaControl(self, X=None, Y=None, Z=None, P=None):
        """
        Thực hiện điều khiển góc theta (G06) để thiết lập các góc và khoảng cách di chuyển.

        :param X: góc của khớp Theta 1.
        :param Y: góc của khớp Theta 2.
        :param Z: góc của khớp Theta 3.
        :param P: khoảng cách di chuyển, đơn vị mm.
        """
        command = GCodeCommand("G06", X=X, Y=Y, Z=Z, P=P)
        self.execute_command(command)

    def Home(self):
        """
        Thực hiện lệnh tự động về home (G28) cho tất cả các trục.
        """
        command = GCodeCommand("G28")
        self.execute_command(command)

    def SetAbsolute(self):
        """
        Đặt chế độ di chuyển thành chế độ tuyệt đối (G90).
        """
        command = GCodeCommand("G90")
        self.execute_command(command)

    def SetRelative(self):
        """
        Đặt chế độ di chuyển thành chế độ tương đối (G91).
        """
        command = GCodeCommand("G91")
        self.execute_command(command)

    def GetP(self):
        """
        Thực hiện lệnh để lấy vị trí hiện tại (G93).
        """
        command = GCodeCommand("G93")
        self.execute_command(command)
        received_data = ""
        wait = 1
        while wait<=10:
            received_data = self.ser.readline().decode('utf-8')
            wait+=1
            time.sleep(0.1)
            if received_data:
                print(received_data)
                return received_data

    def OutputOn(self, S=None):
        """
        Bật đầu ra, laser, hoặc máy hút sử dụng M03.
        :param S: Tham số điều khiển đầu ra (thường là nhiệt độ).
        """
        command = GCodeCommand("M03", S=S)
        self.execute_command(command)

    def OutputOff(self):
        """
        Tắt đầu ra, laser, hoặc máy hút sử dụng M05.
        """
        command = GCodeCommand("M05")
        self.execute_command(command)
        
    def OffSteppers(self):
        """
        Tắt động cơ bước sử dụng M84.
        """
        command = GCodeCommand("M84")
        self.execute_command(command)

    def SetTemp(self, temp):
        """
        Đặt nhiệt độ đầu nóng sử dụng M104.
        :param temp: Nhiệt độ đầu nóng.
        """
        command = GCodeCommand("M104", S=temp)
        self.execute_command(command)

    def ReportTemp(self):
        """
        Báo cáo nhiệt độ hiện tại sử dụng M105.
        """
        command = GCodeCommand("M105")
        self.execute_command(command)

        received_data = ""
        wait = 1
        while wait<=10:
            received_data = self.ser.readline().decode('utf-8')
            wait+=1
            time.sleep(0.1)
            if received_data:
                print(received_data)
                return received_data

    def WaitTemp(self, temp):
        """
        Đặt nhiệt độ đầu nóng và chờ đạt nhiệt độ đó sử dụng M109.
        :param temp: Nhiệt độ đầu nóng cần đạt.
        """
        command = GCodeCommand("M109", S=temp)
        self.execute_command(command)

    def SetF(self, value):
        """
        Đặt tốc độ di chuyển tối đa sử dụng M203.
        :value: Giá trị tốc độ di chuyển tối đa.
        """
        command = GCodeCommand("M203", S=value)
        self.execute_command(command)

    def SetAcceleration(self, value):
        """
        M204 Đặt gia tốc di chuyển.
        :value: Giá trị gia tốc.
        """
        command = GCodeCommand("M204", A=value)
        self.execute_command(command)

    def SetBeginEndVelocity(self, value):
        """M205 Đặt tốc độ bắt đầu/kết thúc."""
        command = GCodeCommand("M205", S=value)
        self.execute_command(command)

    def SetAxisOffset(self, X=None, Y=None, Z=None):
        """M206 Đặt độ lệch trục."""
        command = GCodeCommand("M206", X=X, Y=Y, Z=Z)
        self.execute_command(command)


    def SelectEffector(self, value):
        """M360 chọn bộ phận cuối cho robot .
        0-chân không (mặc định)
        1-kẹp
        2-Bút
        3-Laser
        4-Máy in
        5-Tùy chỉnh
        """
        if value not in [0, 1, 2, 3, 4, 5]:
            raise ValueError("Invalid end effector selection. Use values from 0 to 5.")
        command = GCodeCommand("M360", E=value)
        self.execute_command(command)

    def SetInterpolatedLineLength(self, length):
        """Thiết lập độ dài của mỗi đoạn trong nội suy đường thẳng dùng lệnh M361."""
        command = GCodeCommand("M361", P=length)
        self.execute_command(command)

    def SetArcSegmentLength(self, length):
        """Thiết lập độ dài của mỗi đoạn trong nội suy cung dùng lệnh M362."""
        command = GCodeCommand("M362", P=length)
        self.execute_command(command)

    def SetZMax(self, position):
        """Thiết lập vị trí Z tối đa dùng lệnh M402."""
        command = GCodeCommand("M402", Z=position)
        self.execute_command(command)

    def SaveSettings(self):
        """Lưu tất cả các cài đặt có thể cấu hình vào EEPROM dùng lệnh M500."""
        command = GCodeCommand("M500")
        self.execute_command(command)

    def RestoreSettings(self):
        """Khôi phục tất cả các cài đặt đã lưu từ EEPROM dùng lệnh M501."""
        command = GCodeCommand("M501")
        self.execute_command(command)

    def ResetSettings(self):
        """Đặt lại tất cả các cài đặt có thể cấu hình về mặc định của nhà sản xuất dùng lệnh M502."""
        command = GCodeCommand("M502")
        self.execute_command(command)


    def print_commands(self):
        """
        In tất cả các lệnh trong lịch sử lệnh.
        """
        for cmd in self.command_history:
            print(cmd)
