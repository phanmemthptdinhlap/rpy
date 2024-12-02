from rpy.adcs import ADCS
from rpy.motor import MOTOR1,MOTOR2
import machine #type: ignore
import time

class MOVE: 
    def __init__(self, pin=None,
                 offset=(0,50),
                 speed=(250,500,750,1000,0),
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
    def turn_degree(self,goc):
        t=self.timeconf*abs(goc)
        if goc>0:
           self.motor1.run(400)
           self.motor2.stop()
        if goc<0:
           self.motor1.stop()
           self.motor2.run(-400)   
        time.sleep(t)
#### ---- Quay bat line
    def turn(self,r=1):
        ''' robot quay
            r=1    di chuyển qua phải
            r=0   di chuyển qua trái
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
        self.motor1.run(200)
        self.motor2.run(200)
        time.sleep(0.2)
        self.motor1.stop()
        self.motor2.stop()

#### ---- Di thang mot khoang cm
#         Nhìn từ phía sau, motor1= phải; motor2= trái
    def run_cm(self,cm):
        ''' Robot di chuyển tiến về trước hoặc lùi về sau một khoảng cm
            Nếu cm dương robot di chuyển về trươc
            Nếu cm âm robot di chuyển về sau
        '''
        t=self.timeconf*abs(cm)
        if cm>0:
            self.motor1.run(800)
            self.motor2.run(800)
        if cm<0:
            self.motor1.run(-800)
            self.motor2.run(-800)
        time.sleep(t)
        self.motor1.stop()
        self.motor2.stop()

#### ---- Do line
    def run_line(self):
        ''' Robot tự động di chuyển theo vạch đen'''
        run=True
        while run:
            try:
                ret=0
                adcs=self.adcs.line()
                if adcs[0] == True and adcs[1] == True and adcs[2] == True and adcs[3] == True:     #True= den, False= trang
                    self.motor1.stop()
                    self.motor2.stop()
                    return 1
                if adcs[0] == True and adcs[1] == True and adcs[2] == False and adcs[3]==False:
                    #print('TH2')
                    print('0den,1den,2trang,3trang')
                    self.motor1.run(self.speed[3])
                    self.motor2.run(self.speed[1])
                if adcs[0] ==False and adcs[1] ==False and adcs[2] ==True and adcs[3] ==True:
                    #print('TH3')
                    print('0trang,1trang,2den,3den')
                    self.motor1.run(self.speed[1])
                    self.motor2.run(self.speed[3])
                if adcs[0] ==True and adcs[1] ==False and adcs[2] ==False and adcs[3] ==False:
                    #print('TH4')
                    print('0den,1trang,2trang,3trang')
                    self.motor1.run(self.speed[2])
                    self.motor2.stop()
                if adcs[0] ==False and adcs[1] ==False and adcs[2] ==False and adcs[3] ==True:
                    #print('TH5')
                    print('0trang,1trang,2trang,3den')
                    self.motor1.stop()
                    self.motor2.run(self.speed[2])
                if adcs[0] ==False and adcs[1] ==True and adcs[2] ==True and adcs[3] ==False:
                    #print('TH6')
                    print('0trang,1den,2den,3trang')
                    self.motor1.run(self.speed[3])
                    self.motor2.run(self.speed[3])
                if adcs[0] ==False and adcs[1] ==True and adcs[2] ==True and adcs[3] ==True:
                    #print('TH7')
                    print('0trang,1den,2den,3den')
                    self.motor1.run(self.speed[2])
                    self.motor2.run(self.speed[3])
                if adcs[0] ==True and adcs[1] ==True and adcs[2] ==True and adcs[3] ==False:
                    #print('TH8')
                    print('0den,1den,2den,3trang')
                    self.motor1.run(self.speed[3])
                    self.motor2.run(self.speed[2])
                if adcs[0] ==False and adcs[1] ==False and adcs[2] ==False and adcs[3] ==False :
                    print('TH9')
                    self.motor1.stop()
                    self.motor2.stop()
                    return 0
                if adcs[0] ==False and adcs[1] ==True and adcs[2] ==False  and adcs[3] ==False:
                    #print('TH10')
                    print('0trang,1den,2trang,3trang')
                    self.motor1.run(self.speed[2])
                    self.motor2.run(self.speed[1])
                if adcs[0] ==False and adcs[1] ==False  and adcs[2] ==True and adcs[3] ==False:
                    #print('TH11')
                    print('0trang,1trang,2den,3trang')
                    self.motor1.run(self.speed[1])
                    self.motor2.run(self.speed[2])
            except ValueError as ve:
                print('false',ve)
                self.motor1.stop()
                self.motor2.stop()
                return -1
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
