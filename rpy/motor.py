import machine #type: ignore 
import time

class MOTOR:
    def __init__(self,a,p,offset=0):
        self.ain = machine.Pin(a, mode=machine.Pin.OUT)
        self.ain.value(0)
        self.pw = machine.PWM(machine.Pin(p), freq = 50)
        self.pw.duty(0)
        self.offset = offset

    def run(self,tocdo):
        if tocdo==0:
            self.stop()
        else:
            huong=0 if tocdo>=0 else 1
            tocdo=abs(tocdo)+self.offset if abs(tocdo)+self.offset<1023 else 1023
            self.pw.duty(tocdo)
            self.ain.value(huong)

    def __call__(self, tocdo, thoigian=None):
        if thoigian is not None:self.runtime(tocdo, thoigian)
        else: self.run(tocdo)

    def stop(self):
        self.pw.duty(0)

    def runtime(self,tocdo, thoigian):
        self.run(tocdo)
        time.sleep(thoigian)
        self.stop()

class MOTOR1(MOTOR):
    def __init__(self,offset=0):
        super().__init__(4,12,offset)

class MOTOR2(MOTOR):
    def __init__(self,offset=0):
        super().__init__(16,13,offset)
