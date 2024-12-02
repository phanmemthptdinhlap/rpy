from rpy.motor import MOTOR1,MOTOR2

import machine #type: ignore
import rpy.hw.hmc5883l as hmc5883l
import time

class ADC(machine.ADC):
    LOW=0
    MID=1
    HIGH=2

    def __init__(self, pin,sample):
        super().__init__(machine.Pin(pin))
        self.atten(machine.ADC.ATTN_11DB)
        self.sample=sample

    def state(self):
        return self.HIGH if self.read()<self.sample[0] else self.LOW if self.read()>self.sample[0] else self.MID

class ADC1(ADC):
    def __init__(self,sample=(200,400)):
        super().__init__(33,sample)

class ADC2(ADC):
    def __init__(self,sample=(200,400)):
        super().__init__(34,sample)

class ADC3(ADC):
    def __init__(self,sample=(200,400)):
        super().__init__(35,sample)

class ADC4(ADC):
    def __init__(self,sample=(200,400)):
        super().__init__(36,sample)

class RUNNER: 
    __offset__=(0,0)
    __speed__=(300,700,900,1000)
    def __init__(self):
        """ RUNNER là thư viện thay thế cho thư viện dò line 
            Các tham số cơ bản vẫn giữ nguyên, có thêm tham số về là bàn số
        """
        self.adcs=(ADC1(),ADC2(),ADC3(),ADC4())
        self.motor1=MOTOR2(self.__offset__[0])
        self.motor2=MOTOR1(self.__offset__[1])
        self.compass=hmc5883l.HMC5883L(scl=22,sda=21)
        self.compass.auto_update_declination()

    def _Turn(self,angle):
        """ Góc quay sang phải mang chiều dương """
        if angle>0:
            _angle,_=self.compass.heading()
            _angle_move=_angle-angle
            _angle_move=_angle_move if _angle_move>0 else _angle_move+360
            angle=abs(_angle_move-_angle)
            while angle>1:
                self.motor1.run(self.speed[0])
                self.motor2.run(-self.speed[0])
                _angle,_=self.compass.heading()
                angle=abs(_angle_move-_angle)
        else:
            _angle,_=self.compass.heading()
            _angle_move=_angle-angle
            _angle_move=_angle_move if _angle_move<360 else _angle_move-360
            angle=abs(_angle_move-_angle)
            while angle>1:
                self.motor1.run(-self.speed[0])
                self.motor2.run(self.speed[0])
                _angle,_=self.compass.heading()
                angle=abs(_angle_move-_angle)
        self.motor1.stop()
        self.motor2.stop()

    def run_step(self):
        while True:
            try:
               if self.adcs[0].state()==ADC.HIGH and self.adcs[3].state()==ADC.HIGH:
            except Exception as e:
                print('false')
                run=False
                self.motor1.stop()
                self.motor2.stop()
                return False
        self.motor1.stop()
        self.motor2.stop()
        return True

    def _run_steps(self,step=1):
        self.run=True
        for _ in range(step):
            self._run_step()

    def run_steps(self,step=1):
        self._run_steps(step)
