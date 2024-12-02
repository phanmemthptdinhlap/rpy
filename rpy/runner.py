from rpy.adcs import ADCS
from rpy.motor import MOTOR1,MOTOR2

import machine #type: ignore
import rpy.hmc5883l as hmc5883l
import time

class RUNER: 
    def __init__(self, adcpin=None,
                 offset=(0,0),speed=(450,700,900,1000)):
        """ RUNNER là thư viện thay thế cho thư viện dò line 
            Các tham số cơ bản vẫn giữ nguyên, có thêm tham số về là bàn số
            Các tham số truyền vào:
                adcpin (int): Chân ADC mắt dò line, mặc định None.
                sda (int): chân dữ liệu,mặc định  21.
                address (int): địa chỉ, mặc định  30.
                gauss (str): mặc định '1.3'.
                """
        if adcpin is not None:
            self.adcs=ADCS(pin=adcpin)
        else:
            self.adcs=ADCS()
        self.speed=speed
        self.motor1=MOTOR2(offset[0])
        self.motor2=MOTOR1(offset[1])
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
            
    def _run_step(self):
        run=True
        while run:
            try:
                index1=2
                index2=2
                adcs=self.adcs.line()
                if adcs[0] == True and adcs[1] == True and adcs[2] == True and adcs[3] == True:#True= den, False= trang
                    self.motor1.stop()
                    self.motor2.stop()   
                    break
                if adcs[0] == True and adcs[1] == True and adcs[2] == False and adcs[3]==False:
                    print('TH2')
                    index1=2
                    index2=3
                if adcs[0] ==False and adcs[1] ==False and adcs[2] ==True and adcs[3] ==True:
                    print('TH3')
                    index1=3
                    index2=2
                if adcs[0] ==True and adcs[1] ==False and adcs[2] ==False and adcs[3] ==False:
                    print('TH4')
                    index1=0
                    index2=2
                if adcs[0] ==False and adcs[1] ==False and adcs[2] ==False and adcs[3] ==True:
                    print('TH5')
                    index1=2
                    index2=0
                if adcs[0] ==False and adcs[1] ==True and adcs[2] ==True and adcs[3] ==False:
                    print('TH6')
                    index1=3
                    index2=3
                if adcs[0] ==False and adcs[1] ==True and adcs[2] ==True and adcs[3] ==True:
                    print('TH9')
                    index1=0
                    index2=2
                if adcs[0] ==True and adcs[1] ==True and adcs[2] ==True and adcs[3] ==False:
                    print('TH10')
                    index1=2
                    index2=0
                if adcs[0] ==True and adcs[1] ==True and adcs[2] ==True and adcs[3] ==True :
                    print('TH11')
                    self.motor1.stop()
                    self.motor2.stop()
                self.motor1.run(self.speed[index1])
                self.motor2.run(self.speed[index2])
            except:
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
