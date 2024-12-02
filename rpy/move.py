from rpy.adcs import ADCS
from rpy.motor import MOTOR1,MOTOR2
import machine #type: ignore
import time

class MOVE: 
    def __init__(self, pin=None,
                 offset=(0,0),
                 speed=(300,700,900,1000),
                 timeconf=0.2):
        if pin is not None:
            self.adcs=ADCS(pin=pin)
        else:
            self.adcs=ADCS()
            self.speed=speed
            self.timeconf=timeconf
            self.motor1=MOTOR2(offset[0])
            self.motor2=MOTOR1(offset[1])

#### ---- Quay goc
    def turn(self,r=True):
        ''' robot quay
            r=True    di chuyển qua phải
            r=False   di chuyển qua trái
        '''
        values=self.adcs.line()
        while not values[0] and not values[3]:
            if r:
                self.motor1.run(0)
                self.motor2.run(400)
            else:
                self.motor1.run(400)
                self.motor2.run(0)
            # TODO figure out why this line is even needed
            values=self.adcs.line()
        self.motor1.stop()
        self.motor2.stop()

#### ---- Di thang mot khoang cm
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

#### ---- Do line
    def run_line(self):
        ''' Robot tự động di chuyển theo vạch đen
            và dùng lại khi gặp vach ngang
        '''
        run=True
        while run:
            try:
                ret=0
                adcs=self.adcs.line()
                if adcs[0] == True and adcs[1] == True and adcs[2] == True and adcs[3] == True:     #True= den, False= trang
                    self.motor1.stop()
                    self.motor2.stop()
                    break
                if adcs[0] == True and adcs[1] == True and adcs[2] == False and adcs[3]==False:
                    print('TH2')
                    self.motor1.run(self.speed[3])
                    self.motor2.run(self.speed[2])
                if adcs[0] ==False and adcs[1] ==False and adcs[2] ==True and adcs[3] ==True:
                    print('TH3')
                    self.motor1.run(self.speed[2])
                    self.motor2.run(self.speed[3])
                if adcs[0] ==True and adcs[1] ==False and adcs[2] ==False and adcs[3] ==False:
                    print('TH4')
                    self.motor1.run(self.speed[2])
                    self.motor2.run(self.speed[0])
                if adcs[0] ==False and adcs[1] ==False and adcs[2] ==False and adcs[3] ==True:
                    print('TH5')
                    self.motor1.run(self.speed[0])
                    self.motor2.run(self.speed[2])
                if adcs[0] ==False and adcs[1] ==True and adcs[2] ==True and adcs[3] ==False:
                    print('TH6')
                    self.motor1.run(self.speed[3])
                    self.motor2.run(self.speed[3])
                if adcs[0] ==False and adcs[1] ==True and adcs[2] ==True and adcs[3] ==True:
                    print('TH7')
                    self.motor1.run(self.speed[2])
                    self.motor2.run(self.speed[1])
                if adcs[0] ==True and adcs[1] ==True and adcs[2] ==True and adcs[3] ==False:
                    print('TH8')
                    self.motor1.run(self.speed[1])
                    self.motor2.run(self.speed[2])
                if adcs[0] ==False and adcs[1] ==False and adcs[2] ==False and adcs[3] ==False :
                    print('TH9')
                    self.motor1.run(self.speed[2])
                    self.motor2.run(self.speed[0])
                    time.sleep(0.5)
                    break
                if adcs[0] ==False and adcs[1] ==True and adcs[2] ==False  and adcs[3] ==False:
                    print('TH10')
                    self.motor1.run(self.speed[0])
                    self.motor2.run(self.speed[2])
                if adcs[0] ==False and adcs[1] ==False  and adcs[2] ==True and adcs[3] ==False:
                    print('TH11')
                    self.motor1.run(self.speed[2])
                    self.motor2.run(self.speed[0])
                if adcs[0] ==True and adcs[1] ==True and adcs[2] == False and adcs[3]==True:
                    print('TH12')
                    self.motor1.run(self.speed[2])
                    self.motor2.run(self.speed[1])
                if adcs[0] ==True and adcs[1] ==False  and adcs[2] == True and adcs[3]==True:
                    print('TH13')
                    self.motor1.run(self.speed[2])
                    self.motor2.run(self.speed[1])
            except:
                print('false')
                run=False
                self.motor1.stop()
                self.motor2.stop()
                return False
        self.motor1.stop()
        self.motor2.stop()
        return True

    '''
    def _run_steps(self,step=1):
        self.run=True
        for _ in range(step):
            self._run_step()
    def run_steps(self,step=1):
        self._run_steps(step)
    '''
