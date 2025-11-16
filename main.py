# main.py - ESP32-S3 MicroPython - Robot UDP Controller (State-Based Array)
import network
import socket
import json
import time
from machine import Pin, PWM

# === CẤU HÌNH WIFI AP ===
SSID = "ROBOT_THPT_DINHLAP"
PASSWORD = "thptdl1234"

# === CẤU HÌNH UDP ===
UDP_IP = "192.168.4.1"
UDP_PORT = 8888

# === DANH SÁCH KHÓA ĐỒNG BỘ (16 PHẦN TỬ) ===
# Thứ tự này PHẢI GIỐNG HỆT với _commandKeys trong ứng dụng Flutter
COMMAND_KEYS = [
    'robot_up', 'robot_down', 'robot_left', 'robot_right',           # 1-4: Di chuyển
    'arm_up', 'arm_down', 'arm_left', 'arm_right',                   # 9-12: Cánh tay (Rotation/Panning)
    'arm_far', 'arm_near',                                           # 13-14: Cánh tay (Extension - NEW)
    'arm_gap', 'arm_nha',                                            # 15-16: Gắp/Nhả
    'thung_tl_up', 'thung_tr_up',                                   # 5-6: Thùng trái (Bucket Left)
    'thung_tl_down', 'thung_tr_down'                                    # 7-8 : Thùng phải (Bucket Right)
]

# === CẤU HÌNH CHÂN ===
# Motor DC (L298N)
motor_l_fwd = Pin(11, Pin.OUT)
motor_l_bwd = Pin(12, Pin.OUT)
motor_r_fwd = Pin(13, Pin.OUT)
motor_r_bwd = Pin(14, Pin.OUT)

# Servo (SG90) - PWM 50Hz
servo_arm = PWM(Pin(4), freq=50)       # Cánh tay (Up/Down)
servo_bucket_l = PWM(Pin(5), freq=50)  # Thùng trái
servo_bucket_r = PWM(Pin(6), freq=50)  # Thùng phải
servo_gripper = PWM(Pin(7), freq=50)   # Gắp/Nhả
servo_arm_ext = PWM(Pin(15), freq=50)   # Kéo dài/Rút ngắn (NEW)

# === THAM SỐ ĐIỀU KHIỂN MỀM MẠI ===
# Bước nhảy góc mỗi lần cập nhật (mỗi 50ms từ Flutter)
SERVO_INCREMENT = 2.0    
MIN_ANGLE = 20.0         # Giới hạn góc tối thiểu (để bảo vệ servo)
MAX_ANGLE = 160.0        # Giới hạn góc tối đa (để bảo vệ servo)

# === BIẾN GÓC HIỆN TẠI CỦA SERVO (Lưu dưới dạng float để có độ chính xác) ===
current_arm_angle = 90.0
current_bucket_l_angle = 90.0
current_bucket_r_angle = 90.0
current_gripper_angle = MIN_ANGLE # Khởi tạo Nhả (MIN_ANGLE)
current_arm_ext_angle = 90.0 # Vị trí giữa cho kéo dài/rút ngắn

# === HÀM ĐIỀU KHIỂN SERVO (0° - 180°) ===
def servo_write(servo, angle):
    # Duty cycle: 2.5% (0°) → 12.5% (180°)
    duty = int((angle * 10 / 180) + 2.5)
    servo.duty(duty)

# Khởi tạo servo ở vị trí giữa/mặc định
servo_write(servo_arm, current_arm_angle)
servo_write(servo_bucket_l, current_bucket_l_angle)
servo_write(servo_bucket_r, current_bucket_r_angle)
servo_write(servo_gripper, current_gripper_angle)  
servo_write(servo_arm_ext, current_arm_ext_angle)

# === HÀM DỪNG MOTOR ===
def stop_motors():
    motor_l_fwd.off(); motor_l_bwd.off()
    motor_r_fwd.off(); motor_r_bwd.off()

# === HÀM PHÂN TÍCH VÀ ĐIỀU KHIỂN TỪ MẢNG GIÁ TRỊ ===
def process_commands(values):
    """
    Phân tích mảng 16 giá trị và thực hiện hành động (Motor cứng, Servo mềm).
    """
    if len(values) != len(COMMAND_KEYS):
        print("Lỗi: Số lượng lệnh không khớp (nhận:", len(values), "cần:", len(COMMAND_KEYS), ")")
        return

    # Khai báo các biến góc là global để có thể thay đổi giá trị
    global current_arm_angle, current_bucket_l_angle, current_bucket_r_angle, current_gripper_angle, current_arm_ext_angle

    # --- PHASE 1: XỬ LÝ DI CHUYỂN (MOTOR) ---
    is_moving = False
    stop_motors() # Dừng motor trước

    # Chỉ kiểm tra 4 lệnh di chuyển đầu tiên (index 0 đến 3)
    for i in range(4):
        if values[i] == 1:
            cmd = COMMAND_KEYS[i]
            is_moving = True
            
            # Xử lý lệnh di chuyển
            # print("MOVE:", cmd)
            if cmd == "robot_up":
                motor_l_fwd.on(); motor_r_fwd.on()
            elif cmd == "robot_down":
                motor_l_bwd.on(); motor_r_bwd.on()
            elif cmd == "robot_left":
                motor_l_bwd.on(); motor_r_fwd.on()
            elif cmd == "robot_right":
                motor_l_fwd.on(); motor_r_bwd.on()
            
            # Chỉ cho phép 1 lệnh di chuyển tại 1 thời điểm.
            print("Moving:", cmd,end=' | ')
            break 
            
    # --- PHASE 2: TÍNH TOÁN GÓC MỚI CHO SERVO (Điều khiển mềm mại) ---
    
    # Tính toán góc mới dựa trên SERVO_INCREMENT
    
    # Thùng (Bucket)
    if values[COMMAND_KEYS.index('thung_tl_up')] == 1:
        current_bucket_l_angle += SERVO_INCREMENT
    elif values[COMMAND_KEYS.index('thung_tl_down')] == 1:
        current_bucket_l_angle -= SERVO_INCREMENT

    if values[COMMAND_KEYS.index('thung_tr_up')] == 1:
        current_bucket_r_angle += SERVO_INCREMENT
    elif values[COMMAND_KEYS.index('thung_tr_down')] == 1:
        current_bucket_r_angle -= SERVO_INCREMENT
    
    # Cánh tay (Arm Rotation/Panning)
    if values[COMMAND_KEYS.index('arm_up')] == 1:
        current_arm_angle += SERVO_INCREMENT
    elif values[COMMAND_KEYS.index('arm_down')] == 1:
        current_arm_angle -= SERVO_INCREMENT
    elif values[COMMAND_KEYS.index('arm_left')] == 1:
        # Panning trái
        current_arm_angle -= SERVO_INCREMENT
    elif values[COMMAND_KEYS.index('arm_right')] == 1:
        # Panning phải
        current_arm_angle += SERVO_INCREMENT

    # Cánh tay (Arm Extension - NEW)
    if values[COMMAND_KEYS.index('arm_far')] == 1:
        current_arm_ext_angle += SERVO_INCREMENT
    elif values[COMMAND_KEYS.index('arm_near')] == 1:
        current_arm_ext_angle -= SERVO_INCREMENT

    # Gắp / Nhả (Gripper) - Dùng góc cố định để đảm bảo hành động dứt khoát
    if values[COMMAND_KEYS.index('arm_gap')] == 1:
        current_gripper_angle = MAX_ANGLE  # Gắp (góc lớn)
    elif values[COMMAND_KEYS.index('arm_nha')] == 1:
        current_gripper_angle = MIN_ANGLE  # Nhả (góc nhỏ)


    # --- PHASE 3: CẬP NHẬT GÓC VÀ ÁP DỤNG GIỚI HẠN ---

    # Áp dụng giới hạn góc (Clamping) cho tất cả các servo điều khiển mềm mại
    current_arm_angle = max(MIN_ANGLE, min(MAX_ANGLE, current_arm_angle))
    current_bucket_l_angle = max(MIN_ANGLE, min(MAX_ANGLE, current_bucket_l_angle))
    current_bucket_r_angle = max(MIN_ANGLE, min(MAX_ANGLE, current_bucket_r_angle))
    current_arm_ext_angle = max(MIN_ANGLE, min(MAX_ANGLE, current_arm_ext_angle))

    # Áp dụng góc mới (chuyển float sang int để sử dụng hàm servo_write)
    servo_write(servo_arm, int(current_arm_angle))
    servo_write(servo_bucket_l, int(current_bucket_l_angle))
    servo_write(servo_bucket_r, int(current_bucket_r_angle))
    servo_write(servo_gripper, int(current_gripper_angle))
    servo_write(servo_arm_ext, int(current_arm_ext_angle))

    # Tùy chọn: In log góc để kiểm tra
    print(f"Arm:{int(current_arm_angle)} | Ext:{int(current_arm_ext_angle)} | Grip:{int(current_gripper_angle)} | BktL:{int(current_bucket_l_angle)} | BktR:{int(current_bucket_r_angle)}")


# === KHỞI TẠO WIFI AP ===
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=SSID, password=PASSWORD, authmode=network.AUTH_WPA_WPA2_PSK)
ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))

print("WiFi AP:", SSID)
print("IP:", ap.ifconfig()[0])

# === UDP SERVER ===
addr = socket.getaddrinfo(UDP_IP, UDP_PORT)[0][-1]
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(addr)
s.settimeout(0.1) # Non-blocking

print(f"UDP Server chạy tại {UDP_IP}:{UDP_PORT}")

# === VÒNG LẶP CHÍNH ===
while True:
    try:
        # Nhận gói UDP
        data, client_addr = s.recvfrom(1024)
        if data:
            try:
                # Dữ liệu nhận được là một chuỗi JSON của mảng (ví dụ: "[0, 1, 0, ...]")
                values = json.loads(data.decode('utf-8'))
                # print("Dữ liệu nhận từ", client_addr, ":", values)
                if isinstance(values, list):
                    print()
                    process_commands(values)
                else:
                    print("Lỗi: Dữ liệu nhận không phải là mảng (List).")

            except Exception as e:
                print("JSON/Processing error:", e)
    except OSError:
         print(".",end='')#pass  # Timeout (không có dữ liệu mới)
    
    time.sleep_ms(10) # Dừng một chút để ổn định