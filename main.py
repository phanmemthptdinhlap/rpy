import network # type: ignore
import socket
import uasyncio as asyncio # type: ignore #tr
from machine import Pin # type: ignore
import time

# Cấu hình WiFi AP (Access Point)
SSID_AP = 'RobotAP'  # Tên mạng WiFi ESP tạo
PASSWORD_AP = 'password123'  # Password (ít nhất 8 ký tự)

# Cấu hình GPIO cho robot (motor driver)
MOTOR_LEFT_FWD = Pin(1, Pin.OUT)
MOTOR_LEFT_BWD = Pin(2, Pin.OUT)
MOTOR_RIGHT_FWD = Pin(3, Pin.OUT)
MOTOR_RIGHT_BWD = Pin(4, Pin.OUT)

# Hàm điều khiển motor
def stop():
    MOTOR_LEFT_FWD.off()
    MOTOR_LEFT_BWD.off()
    MOTOR_RIGHT_FWD.off()
    MOTOR_RIGHT_BWD.off()

def forward():
    stop()
    MOTOR_LEFT_FWD.on()
    MOTOR_RIGHT_FWD.on()
    time.sleep(0.5)  # Thời gian chạy
    stop()

def backward():
    stop()
    MOTOR_LEFT_BWD.on()
    MOTOR_RIGHT_BWD.on()
    time.sleep(0.5)
    stop()

def left():
    stop()
    MOTOR_LEFT_BWD.on()
    MOTOR_RIGHT_FWD.on()
    time.sleep(0.5)
    stop()

def right():
    stop()
    MOTOR_LEFT_FWD.on()
    MOTOR_RIGHT_BWD.on()
    time.sleep(0.5)
    stop()

# Tạo WiFi AP
wlan = network.WLAN(network.AP_IF)
wlan.active(True)
wlan.config(essid=SSID_AP, password=PASSWORD_AP)
print('WiFi AP đang chạy...')
print('SSID:', SSID_AP)
print('Password:', PASSWORD_AP)
print('IP mặc định:', wlan.ifconfig()[0])  # Thường là 192.168.4.1

# HTML trang điều khiển
HTML = """
<!DOCTYPE html>
<html>
<head><title>Điều Khiển Robot</title></head>
<body>
<h1>Robot Control via WiFi AP</h1>
<p>IP: {}:80 | SSID: {} | Pass: {}</p>
<form action="/"><button style="width:100px;height:50px;">Dừng</button></form>
<form action="/forward"><button style="width:100px;height:50px;background:green;">Tiến</button></form>
<form action="/backward"><button style="width:100px;height:50px;background:red;">Lùi</button></form>
<form action="/left"><button style="width:100px;height:50px;background:yellow;">Trái</button></form>
<form action="/right"><button style="width:100px;height:50px;background:yellow;">Phải</button></form>
</body>
</html>
"""

# Web server handler
async def serve_client(reader, writer):
    request_line = await reader.readline()
    request = request_line.decode().strip().split(' ')[1]  # Lấy path
    while await reader.readline() != b"\r\n":
        pass  # Bỏ qua header

    if request == '/':
        response = HTML.format(wlan.ifconfig()[0], SSID_AP, PASSWORD_AP)
        command = 'stop'
    elif request == '/forward':
        forward()
        response = HTML.format(wlan.ifconfig()[0], SSID_AP, PASSWORD_AP)
        command = 'forward'
    elif request == '/backward':
        backward()
        response = HTML.format(wlan.ifconfig()[0], SSID_AP, PASSWORD_AP)
        command = 'backward'
    elif request == '/left':
        left()
        response = HTML.format(wlan.ifconfig()[0], SSID_AP, PASSWORD_AP)
        command = 'left'
    elif request == '/right':
        right()
        response = HTML.format(wlan.ifconfig()[0], SSID_AP, PASSWORD_AP)
        command = 'right'
    else:
        response = HTML.format(wlan.ifconfig()[0], SSID_AP, PASSWORD_AP)
        command = 'unknown'

    print('Lệnh:', command)
    writer.write('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'.encode())
    writer.write(response.encode())
    await writer.drain()
    await writer.aclose()

# Hàm main (ĐÃ SỬA: Không dùng serve_forever)
async def main():
    stop()  # Dừng robot ban đầu
    server = await asyncio.start_server(serve_client, '0.0.0.0', 80)
    print('Web server chạy trên port 80')
    async with server:
        while True:  # Vòng lặp giữ server sống (FIX cho MicroPython)
            await asyncio.sleep(1)  # Sleep để uasyncio xử lý connections

# Chạy server
asyncio.run(main())