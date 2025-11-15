# main.py - ESP32-S3 MicroPython - Robot UDP Controller
import network
import socket
import json
import time
from machine import Pin, PWM, Timer

# === CẤU HÌNH WIFI AP ===
SSID = "RobotESP32"
PASSWORD = "12345678"

# === CẤU HÌNH UDP ===
UDP_IP = "192.168.4.1"
UDP_PORT = 8888

# === CẤU HÌNH CHÂN ===
# Motor DC (L298N)
motor_l_fwd = Pin(12, Pin.OUT)
motor_l_bwd = Pin(13, Pin.OUT)
motor_r_fwd = Pin(14, Pin.OUT)
motor_r_bwd = Pin(15, Pin.OUT)

# Servo (SG90) - PWM 50Hz
servo_arm = PWM(Pin(16), freq=50)
servo_bucket_l = PWM(Pin(17), freq=50)
servo_bucket_r = PWM(Pin(19), freq=50)
servo_gripper = PWM(Pin(21), freq=50)

# === HÀM ĐIỀU KHIỂN SERVO (0° - 180°) ===
def servo_write(servo, angle):
    # Duty cycle: 2.5% (0°) → 12.5% (180°)
    duty = int((angle * 10 / 180) + 2.5)
    servo.duty(duty)

# Khởi tạo servo ở giữa
servo_write(servo_arm, 90)
servo_write(servo_bucket_l, 90)
servo_write(servo_bucket_r, 90)
servo_write(servo_gripper, 90)  # Nhả

# === BIẾN ĐIỀU KHIỂN ===
last_cmd = ""
last_time = 0
timeout = 500  # ms

# === TIMER TỰ DỪNG ===
timer = Timer(0)

def stop_all(t=None):  # t không dùng, nhưng cần để Timer hoạt động
    global last_time, last_cmd
    if time.ticks_ms() - last_time > timeout:
        motor_l_fwd.off(); motor_l_bwd.off()
        motor_r_fwd.off(); motor_r_bwd.off()
        last_cmd = ""
        print("STOP: Timeout")

timer.init(mode=Timer.PERIODIC, period=100, callback=stop_all)

# === HÀM ĐIỀU KHIỂN ROBOT ===
def control_robot(cmd):
    global last_time, last_cmd
    last_time = time.ticks_ms()
    if cmd == last_cmd:
        return
    last_cmd = cmd

    # Dừng motor trước
    motor_l_fwd.off(); motor_l_bwd.off()
    motor_r_fwd.off(); motor_r_bwd.off()

    print("CMD:", cmd)

    # === DI CHUYỂN ===
    if cmd == "robot_up":
        motor_l_fwd.on(); motor_r_fwd.on()
    elif cmd == "robot_down":
        motor_l_bwd.on(); motor_r_bwd.on()
    elif cmd == "robot_left":
        motor_l_bwd.on(); motor_r_fwd.on()
    elif cmd == "robot_right":
        motor_l_fwd.on(); motor_r_bwd.on()

    # === THÙNG ===
    elif cmd == "thung_tl_up":
        servo_write(servo_bucket_l, 135)
    elif cmd == "thung_tl_down":
        servo_write(servo_bucket_l, 45)
    elif cmd == "thung_tr_up":
        servo_write(servo_bucket_r, 135)
    elif cmd == "thung_tr_down":
        servo_write(servo_bucket_r, 45)

    # === CÁNH TAY ===
    elif cmd == "arm_up":
        servo_write(servo_arm, 135)
    elif cmd == "arm_down":
        servo_write(servo_arm, 45)
    elif cmd == "arm_left":
        servo_write(servo_arm, 45)
    elif cmd == "arm_right":
        servo_write(servo_arm, 135)

    # === GẮP / NHẢ ===
    elif cmd == "grip_g":
        servo_write(servo_gripper, 135)  # Gắp
    elif cmd == "grip_nha":
        servo_write(servo_gripper, 45)   # Nhả

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
s.settimeout(0.1)  # Non-blocking

print(f"UDP Server chạy tại {UDP_IP}:{UDP_PORT}")

# === VÒNG LẶP CHÍNH ===
while True:
    try:
        data, client_addr = s.recvfrom(1024)
        if data:
            try:
                msg = json.loads(data.decode('utf-8'))
                cmd = msg.get("cmd", "")
                val = msg.get("val", 0)
                if cmd and val > 0:
                    control_robot(cmd)
            except Exception as e:
                print("JSON error:", e)
    except OSError:
        pass  # Timeout
    time.sleep_ms(10)