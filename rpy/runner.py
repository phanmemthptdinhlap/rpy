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
    def __init__(self,sample=(1100,1200)):
        super().__init__(33,sample)

class ADC2(ADC):
    __name__='ADC2'
    def __init__(self,sample=(1500,1700)):
        super().__init__(34,sample)

class ADC3(ADC):
    __name__='ADC3'
    def __init__(self,sample=(1600,1800)):
        super().__init__(35,sample)

class ADC4(ADC):
    __name__='ADC4'
    def __init__(self,sample=(1300,1600)):
        super().__init__(36,sample)

class RUNNER: 
    class TURN_CODE:
        __auto__=0
        __manual__=1
    class RUN_CODE:
        __exit__=0
        __all_white__=1
        __all_black__=2
        __error__=3
    __msg__=''
    __offset__=(0,0)
    __speed__=(200,400,600,700)
    __timeconf__=0.2

    def __init__(self):
        """ RUNNER là thư viện thay thế cho thư viện dò line 
            Các tham số cơ bản vẫn giữ nguyên, có thêm tham số về là bàn số
        """
        self.adc0=machine.ADC(machine.Pin(33))
        self.adc1=machine.ADC(machine.Pin(34))
        self.adc2=machine.ADC(machine.Pin(35))
        self.adc3=machine.ADC(machine.Pin(36))
        
        self.adc0.atten(machine.ADC.ATTN_11DB)
        self.adc1.atten(machine.ADC.ATTN_11DB)
        self.adc2.atten(machine.ADC.ATTN_11DB)
        self.adc3.atten(machine.ADC.ATTN_11DB)

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
            t=angle*self.__timeconf__
            if angle>0:
                self.motor1.run(self.__speed__[0])
                self.motor2.run(-self.__speed__[0])
            else:
                self.motor1.run(-self.__speed__[0])
                self.motor2.run(self.__speed__[0])
            time.sleep(t)
            self.motor1.stop()
            self.motor2.stop()
    def readadcs(self):
        return self.adc0.read(),self.adc1.read(),self.adc2.read(),self.adc3.read()
    def run_step(self):
        while True:
            adc0 = self.adc0.read()
            adc1 = self.adc1.read()
            adc2 = self.adc2.read()
            adc3 = self.adc3.read()
            if adc0<100 and adc3<100:
                self.motor1.stop()
                self.motor2.stop()
                return RUNNER.RUN_CODE.__all_black__
            if adc1<100 and adc2<100:




        """while True:
            try:
                adc0=self.adcs[0].state()
                adc3=self.adcs[3].state()
                if adc0==ADC.STATE.LOW and adc3==ADC.STATE.LOW:
                   self.motor1.stop()
                   self.motor2.stop()
                   return RUNNER.RUN_CODE.__all_black__
                adc1=self.adcs[1].state()
                adc2=self.adcs[2].state()
                if adc1==ADC.STATE.LOW and adc2==ADC.STATE.LOW:
                   self.motor1.run(self.__speed__[2])
                   self.motor2.run(self.__speed__[2])
                else:
                    if adc1==ADC.STATE.LOW and adc2==ADC.STATE.HIGH:
                        self.motor1.run(self.__speed__[3])
                        if adc0==ADC.STATE.LOW:
                            self.motor2.run(self.__speed__[0])
                        else:
                            self.motor2.run(self.__speed__[1])
                    if adc2==ADC.STATE.LOW and adc1==ADC.STATE.HIGH:
                        self.motor2.run(self.__speed__[3])
                        if adc3==ADC.STATE.LOW:
                            self.motor1.run(self.__speed__[0])
                        else:
                            self.motor1.run(self.__speed__[1])
                if self.adc0==ADC.STATE.HIGH and adc1==ADC.STATE.HIGH and adc2==ADC.STATE.HIGH and adc3==ADC.STATE.HIGH:
                    self.motor1.stop()
                    self.motor2.stop()
                    return RUNNER.RUN_CODE.__all_white__
                return RUNNER.RUN_CODE.__exit__
            except Exception as e:
                __msg__=str(e)
                self.motor1.stop()
                self.motor2.stop()
                return RUNNER.RUN_CODE.__error__
        """
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
        def readadcs(self):
            print(self.runner.readadcs())
if __name__=='__main__':
    test=TEST.TESTRUNNER()
    #test=TEST.TESTADC()
    while True:
        test.readadcs()
        #test.read()