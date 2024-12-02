from rpy.motor import MOTOR1,MOTOR2
import machine #type: ignore
import rpy.hw.hmc5883l as hmc5883l
import time

class ADC(machine.ADC):
    class STATE:
        LOW=0
        MID=1
        HIGH=2
    class TYPE:
        TYPE_1=0
        TYPE_2=1
    __name__='ADC'
    def __init__(self, pin,sample,type=TYPE.TYPE_1):
        super().__init__(machine.Pin(pin))
        self.atten(machine.ADC.ATTN_11DB)
        self.sample=sample
        self._type=type
    def read(self):
        value=super().read()
        return 4095-value if self._type==self.TYPE.TYPE_1 else value 
    def state(self):
        return ADC.STATE.HIGH if self.read()>self.sample[1] else ADC.STATE.LOW if self.read()<self.sample[0] else ADC.STATE.MID

class ADC1(ADC):
    __name__='ADC1'
    def __init__(self,sample=(2750,3050)):
        super().__init__(33,sample)

class ADC2(ADC):
    __name__='ADC2'
    def __init__(self,sample=(3200,3500)):
        super().__init__(34,sample)

class ADC3(ADC):
    __name__='ADC3'
    def __init__(self,sample=(3200,3500)):
        super().__init__(35,sample)

class ADC4(ADC):
    __name__='ADC4'
    def __init__(self,sample=(2850,3150)):
        super().__init__(36,sample)

class RUNNER: 
    __offset__=(0,0)
    __speed__=(450,700,900,1000)
    def __init__(self):
        """ RUNNER là thư viện thay thế cho thư viện dò line 
            Các tham số cơ bản vẫn giữ nguyên, có thêm tham số về là bàn số
        """
        self.adcs=(ADC1(),ADC2(),ADC3(),ADC4())
        self.motor1=MOTOR1(self.__offset__[0])
        self.motor2=MOTOR2(self.__offset__[1])
        try:
            self.compass=hmc5883l.HMC5883L(scl=22,sda=21)
            self.compass.auto_update_declination()
        except Exception as e:
            print("Runner_init: ",e)
            self.compass=None
    def _Turn(self,angle):
        """ Góc quay sang phải mang chiều dương """
        try:
            if angle>0:
                _angle,_=self.compass.heading()
                _angle_move=_angle-angle
                _angle_move=_angle_move if _angle_move>0 else _angle_move+360
                angle=abs(_angle_move-_angle)
                while angle>1:
                    self.motor1.run(self.__speed__[0])
                    self.motor2.run(-self.__speed__[0])
                    _angle,_=self.compass.heading()
                    angle=abs(_angle_move-_angle)
            else:
                _angle,_=self.compass.heading()
                _angle_move=_angle-angle
                _angle_move=_angle_move if _angle_move<360 else _angle_move-360
                angle=abs(_angle_move-_angle)
                while angle>1:
                    self.motor1.run(-self.__speed__[0])
                    self.motor2.run(self.__speed__[0])
                    _angle,_=self.compass.heading()
                    angle=abs(_angle_move-_angle)
            self.motor1.stop()
            self.motor2.stop()
        except Exception as e:
            print(e.__str__())
    def run_step(self):
        while True:
            try:
               if self.adcs[0].state()==ADC.STATE.LOW and self.adcs[3].state()==ADC.STATE.LOW:
                   self.motor1.stop()
                   self.motor2.stop()
                   return "Đen hết"
               if self.adcs[1].state()==ADC.STATE.LOW and self.adcs[2].state()==ADC.STATE.LOW:
                   self.motor1.run(self.__speed__[2])
                   self.motor2.run(self.__speed__[2])
               else:
                   if self.adcs[1].state()==ADC.STATE.HIGH:
                        self.motor1.run(self.__speed__[3])
                        if self.adcs[3].state()==ADC.STATE.LOW:
                            self.motor2.run(self.__speed__[0])
                        else:
                            self.motor2.run(self.__speed__[1])
                   if self.adcs[2].state()==ADC.STATE.HIGH:
                        self.motor2.run(self.__speed__[3])
                        if self.adcs[0].state()==ADC.STATE.LOW:
                            self.motor1.run(self.__speed__[0])
                        else:
                            self.motor1.run(self.__speed__[1])
               if self.adcs[0].state()==ADC.STATE.HIGH and self.adcs[1].state()==ADC.STATE.HIGH and self.adcs[2].state()==ADC.STATE.HIGH and self.adcs[3].state()==ADC.STATE.HIGH:
                    self.motor1.stop()
                    self.motor2.stop()
                    return "Trắng hết"
               return "Kết thúc"
            except Exception as e:
                self.motor1.stop()
                self.motor2.stop()
                return "Lỗi:"+str(e)
    def run_steps(self,step=1):
        self.run=True
        for _ in range(step):
            self.run_step()
class TEST:
    class TESTADC:
        def __init__(self):
            self.adcs=(ADC1(),ADC2(),ADC3(),ADC4())
            self.adcs[0].read()
            self.adcs[1].read()
            self.adcs[2].read()
            self.adcs[3].read()
        def read(self):
            print([adc.read() for adc in self.adcs])
        def state(self):
            print([adc.state() for adc in self.adcs])
    class TESTRUNNER:
        def __init__(self):
            self.runner=RUNNER()    
        def run(self):
            print("begin run")
            print('run:',self.runner.run_step())

if __name__=='__main__':
    test=TEST.TESTRUNNER()
    while True:
        test.run()
        time.sleep(3)