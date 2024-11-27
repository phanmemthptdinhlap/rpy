from rpy.adcs import ADCS
from rpy.motor import MOTOR1,MOTOR2
import machine #type: ignore
import time

class MOVE: 
    def __init__(self, pin=None,
                 offset=(0,0),speed=(300,700,900,1000),timeconf=0.2):
        if pin is not None:
            self.adcs=ADCS(pin=pin)
        else:
            self.adcs=ADCS()
            self.speed=speed
            self.timeconf=timeconf
            self.motor1=MOTOR2(offset[0])
            self.motor2=MOTOR1(offset[1])
##############Quay goc#############
    def turn(self,r=True ):
        '''
        r=True rôbot sẽ di chuyển qua phải
        r=False robot sẽ di chuyển qua trái
        '''
        values=self.adcs.line()
        while not values[0] and not values[3]:
            if r:
                self.motor1.run(0)
                self.motor2.run(400)
            else:
                self.motor1.run(400)
                self.motor2.run(0)
            values=self.adcs.line()
        self.motor1.stop()
        self.motor2.stop()
############Đi thăng một khoảng cm##########
    def run_cm(self,cm):
        ''' Robot di chuyển tiến về trước hoặc lùi về sau một khoảng cm
            Nếu cm dương robot di chuyển về trươc
            Nếu cm âm robot di chuyển về sau
        '''
        t=self.timeconf*abs(cm)
        if cm>0:
            self.motor1.run(400)
            self.motor2.run(400)
        else:
            self.motor1.run(-400)
            self.motor2.run(-400)
        time.sleep(t)
        self.motor1.stop()
        self.motor2.stop()
##########Dò line#####################
    ''' Robot tự động di chuyển theo vạch đen và dùng lại khi gặp vặc ngang'''
    def run_line(self):        
        run=True
        while run:
            try:
                index1=2
                index2=2
                ret=0
                adcs=self.adcs.line()
                if adcs[0] == True and adcs[1] == True and adcs[2] == True and adcs[3] == True:     #True= den, False= trang
                    self.motor1.stop()
                    self.motor2.stop()
                    break
                if adcs[0] == True and adcs[1] == True and adcs[2] == False and adcs[3]==False:
                    print('TH2')
                    index1=3
                    index2=2
                if adcs[0] ==False and adcs[1] ==False and adcs[2] ==True and adcs[3] ==True:
                    print('TH3')
                    index1=2
                    index2=3
                if adcs[0] ==True and adcs[1] ==False and adcs[2] ==False and adcs[3] ==False:
                    print('TH4')
                    index1=2
                    index2=0
                if adcs[0] ==False and adcs[1] ==False and adcs[2] ==False and adcs[3] ==True:
                    print('TH5')
                    index1=0
                    index2=2
                if adcs[0] ==False and adcs[1] ==True and adcs[2] ==True and adcs[3] ==False:
                    print('TH6')
                    index1=3
                    index2=3
                if adcs[0] ==False and adcs[1] ==True and adcs[2] ==True and adcs[3] ==True:
                    print('TH7')
                    index1=2
                    index2=1
                if adcs[0] ==True and adcs[1] ==True and adcs[2] ==True and adcs[3] ==False:
                    print('TH8')
                    index1=1
                    index2=2
                if adcs[0] ==False and adcs[1] ==False and adcs[2] ==False and adcs[3] ==False :
                    print('TH9')
                    index1=2
                    index2=0
                    time.sleep(0.5)
                    break
                if adcs[0] ==False and adcs[1] ==True and adcs[2] ==False  and adcs[3] ==False:
                    print('TH10')
                    index1=0
                    index2=2
                if adcs[0] ==False and adcs[1] ==False  and adcs[2] ==True and adcs[3] ==False:
                    print('TH11')
                    index1=2
                    index2=0
                if adcs[0] ==True and adcs[1] ==True and adcs[2] == False and adcs[3]==True:
                    print('TH12')
                    index1=2
                    index2=1
                if adcs[0] ==True and adcs[1] ==False  and adcs[2] == True and adcs[3]==True:
                    print('TH13')
                    index1=2
                    index2=1
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
    
''' def _run_steps(self,step=1):
        self.run=True
        for _ in range(step):
            self._run_step()
    def run_steps(self,step=1):
        self._run_steps(step)'''
        
            


