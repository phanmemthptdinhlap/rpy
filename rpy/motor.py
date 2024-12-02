import machine #type: ignore 
import time

class MOTOR:
    def __init__(self,a,p,offset=0):
        self.ain = machine.Pin(a, mode=machine.Pin.OUT)
        self.ain.value(0)
        self.pw = machine.PWM(machine.Pin(p), freq = 50)
        self.pw.duty(0)
        self.offset = offset

    def run(self,speed):
        if speed==0:
            self.stop()
        else:
            huong=0 if speed>=0 else 1
            speed=abs(speed)+self.offset if abs(speed)+self.offset<1023 else 1023
            self.pw.duty(speed)
            self.ain.value(huong)

    def __call__(self, speed, time=None):
        if time is not None:self.runtime(speed, time)
        else: self.run(speed)

    def stop(self):
        self.pw.duty(0)

    def runtime(self,speed, time):
        self.run(speed)
        time.sleep(time)
        self.stop()

class MOTOR1(MOTOR):
    def __init__(self,offset=0):
        super().__init__(4,12,offset)

class MOTOR2(MOTOR):
    def __init__(self,offset=0):
        super().__init__(16,13,offset)
