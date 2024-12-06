from rpy.adcs import ADCS
from rpy.motor import MOTOR1,MOTOR2
import machine #type: ignore
import time
from rpy.sowing import SOWING
class MOVE: 
    def __init__(self, pin=None,
                 offset=(0,0),
                 speed=(250,500,750,1000,-500),
                 timeconf=0.2,timeconf2=0.019):
        if pin is not None:
            self.adcs=ADCS(pin=pin)
        else:
            self.adcs=ADCS()
            self.speed=speed
            self.timeconf=timeconf
            self.timeconf2=timeconf2
            self.hs=0
            self.motor1=MOTOR2(offset[0])
            self.motor2=MOTOR1(offset[1])
#### ----wait
    ''' ham nay chi co tac dung stop '''
    def wait(self,wait):
        while True:
            self.motor1.stop()
            self.motor2.stop()
            time.sleep(wait)
            break
    #### ---- Quay goc
    ''' quay goc khi nhap so do vao
        duong thi quay phai
        am thi quay trai
    '''
    def turn_degree(self,goc):
        self.motor1.stop()
        self.motor2.stop()
        t=self.timeconf2*abs(goc)
        if goc>0:
           self.motor2.run(400)
           self.motor1.run(-400)
        if goc<0:
           self.motor2.run(-400)
           self.motor1.run(400)   
        time.sleep(t)
        self.motor1.stop()
        self.motor2.stop()

#### ---- Quay bat line
    def turn(self,r):
        ''' robot quay
            r=1   di chuyển qua phải
            r=0   di chuyển qua trái
        '''
        values=self.adcs.line()
        while not values[1] and not values[2]:
            if r==1:
                self.motor1.stop()
                self.motor2.run(400)
            if r==0:
                self.motor1.run(400)
                self.motor2.stop()
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
    def nha_hat(self):
        run=True
        tu=MOVE()
        c=0
        while run:
            try:
                adcs=self.adcs.line()
                if adcs[0] == True and adcs[1] == True and adcs[2] == True and adcs[3] == True:     #True= den, False= trang
                    c=c+1
                    print(c)
                    if c>4:
                        self.motor1.stop()
                        self.motor2.stop()
                        time.sleep(0.1)
                        self.motor1.run(self.speed[1])
                        self.motor2.run(self.speed[1])
                        time.sleep(0.5)
                        self.motor1.stop()
                        self.motor2.stop()
                        time.sleep(1)
                        tu.turn_degree(45)
                        tu.turn(1)
                        '''self.motor1.stop()
                        time.sleep(2.3)'''
                        self.motor1.stop()
                        self.motor2.stop()
                        time.sleep(0.5)								########ĐANG SỬA##############
                        tu.run_theoline(10)
                        '''self.motor1.run(self.speed[1])
                        self.motor2.run(self.speed[1])
                        time.sleep(10)'''
                        self.motor1.stop()
                        self.motor2.stop()
                        self.motor1.run(self.speed[4])
                        self.motor2.run(self.speed[1])
                        time.sleep(1)
                        self.motor1.stop()
                        self.motor2.stop()
                        c=0
                        
                    else:
                        self.motor1.stop()
                        self.motor2.stop()
                        time.sleep(0.1)
                        self.motor1.run(self.speed[1])
                        self.motor2.run(self.speed[1])
                        time.sleep(1.8)
                        self.motor1.stop()
                        self.motor2.stop()
                        time.sleep(0.2)
                        self.motor1.run(self.speed[1])
                        time.sleep(1.5)
                        self.motor1.stop()
                        time.sleep(1)
                        ##nha hat##
                        self.motor1.run(self.speed[4])
                        time.sleep(1.5)
                        self.motor1.stop()
                        time.sleep(0.2)
                        self.motor2.run(self.speed[1])
                        time.sleep(1.5)
                        self.motor2.stop()
                        time.sleep(1)
                        ##nha hat##
                        self.motor2.run(self.speed[4])
                        time.sleep(1.5)
                        self.motor2.stop()
                        
                if adcs[0] == True and adcs[1] == True and adcs[2] == False and adcs[3]==False:
                    ##print('TH2')
                    #print('0den,1den,2trang,3trang')
                    self.motor1.run(self.speed[3])
                    self.motor2.run(self.speed[1])
                if adcs[0] ==False and adcs[1] ==False and adcs[2] ==True and adcs[3] ==True:
                    ##print('TH3')
                    #print('0trang,1trang,2den,3den')
                    self.motor1.run(self.speed[1])
                    self.motor2.run(self.speed[3])
                if adcs[0] ==True and adcs[1] ==False and adcs[2] ==False and adcs[3] ==False:
                    ##print('TH4')
                    #print('0den,1trang,2trang,3trang')
                    self.motor1.run(self.speed[2])
                    self.motor2.stop()
                if adcs[0] ==False and adcs[1] ==False and adcs[2] ==False and adcs[3] ==True:
                    ##print('TH5')
                    #print('0trang,1trang,2trang,3den')
                    self.motor1.stop()
                    self.motor2.run(self.speed[2])
                if adcs[0] ==False and adcs[1] ==True and adcs[2] ==True and adcs[3] ==False:
                    ##print('TH6')
                    #print('0trang,1den,2den,3trang')
                    self.motor1.run(self.speed[2])
                    self.motor2.run(self.speed[2])
                if adcs[0] ==False and adcs[1] ==True and adcs[2] ==True and adcs[3] ==True:
                    ##print('TH7')
                    #print('0trang,1den,2den,3den')
                    self.motor1.run(self.speed[2])
                    self.motor2.run(self.speed[3])
                if adcs[0] ==True and adcs[1] ==True and adcs[2] ==True and adcs[3] ==False:
                    ##print('TH8')
                    #print('0den,1den,2den,3trang')
                    self.motor1.run(self.speed[3])
                    self.motor2.run(self.speed[2])
                if adcs[0] ==False and adcs[1] ==False and adcs[2] ==False and adcs[3] ==False :
                    #print('TH9')
                    self.motor1.stop()
                    self.motor2.stop()
                    return 0
                if adcs[0] ==False and adcs[1] ==True and adcs[2] ==False  and adcs[3] ==False:
                    ##print('TH10')
                    #print('0trang,1den,2trang,3trang')
                    self.motor1.run(self.speed[2])
                    self.motor2.run(self.speed[1])
                if adcs[0] ==False and adcs[1] ==False  and adcs[2] ==True and adcs[3] ==False:
                    ##print('TH11')
                    #print('0trang,1trang,2den,3trang')
                    self.motor1.run(self.speed[1])
                    self.motor2.run(self.speed[2])
            except ValueError as ve:
                #print('false',ve)
                self.motor1.stop()
                self.motor2.stop()
                return -1
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
                    #self.motor1.run(self.speed[1])
                    #self.motor2.run(self.speed[1])
                    return 1
                    
                if adcs[0] == True and adcs[1] == True and adcs[2] == False and adcs[3]==False:
                    ##print('TH2')
                    #print('0den,1den,2trang,3trang')
                    self.motor1.run(self.speed[3])
                    self.motor2.run(self.speed[1])
                if adcs[0] ==False and adcs[1] ==False and adcs[2] ==True and adcs[3] ==True:
                    ##print('TH3')
                    #print('0trang,1trang,2den,3den')
                    self.motor1.run(self.speed[1])
                    self.motor2.run(self.speed[3])
                if adcs[0] ==True and adcs[1] ==False and adcs[2] ==False and adcs[3] ==False:
                    ##print('TH4')
                    #print('0den,1trang,2trang,3trang')
                    self.motor1.run(self.speed[2])
                    self.motor2.stop()
                if adcs[0] ==False and adcs[1] ==False and adcs[2] ==False and adcs[3] ==True:
                    ##print('TH5')
                    #print('0trang,1trang,2trang,3den')
                    self.motor1.stop()
                    self.motor2.run(self.speed[2])
                if adcs[0] ==False and adcs[1] ==True and adcs[2] ==True and adcs[3] ==False:
                    ##print('TH6')
                    #print('0trang,1den,2den,3trang')
                    self.motor1.run(self.speed[3])
                    self.motor2.run(self.speed[3])
                if adcs[0] ==False and adcs[1] ==True and adcs[2] ==True and adcs[3] ==True:
                    ##print('TH7')
                    #print('0trang,1den,2den,3den')
                    self.motor1.run(self.speed[2])
                    self.motor2.run(self.speed[3])
                if adcs[0] ==True and adcs[1] ==True and adcs[2] ==True and adcs[3] ==False:
                    ##print('TH8')
                    #print('0den,1den,2den,3trang')
                    self.motor1.run(self.speed[3])
                    self.motor2.run(self.speed[2])
                if adcs[0] ==False and adcs[1] ==False and adcs[2] ==False and adcs[3] ==False :
                    #print('TH9')
                    self.motor1.stop()
                    self.motor2.stop()
                    return 0
                if adcs[0] ==False and adcs[1] ==True and adcs[2] ==False  and adcs[3] ==False:
                    ##print('TH10')
                    #print('0trang,1den,2trang,3trang')
                    self.motor1.run(self.speed[2])
                    self.motor2.run(self.speed[1])
                if adcs[0] ==False and adcs[1] ==False  and adcs[2] ==True and adcs[3] ==False:
                    ##print('TH11')
                    #print('0trang,1trang,2den,3trang')
                    self.motor1.run(self.speed[1])
                    self.motor2.run(self.speed[2])
            except ValueError as ve:
                #print('false',ve)
                self.motor1.stop()
                self.motor2.stop()
                return -1
        self.motor1.stop()
        self.motor2.stop()
        return True
    def _run_steps(self,step=1):
        self.run=True
        for _ in range(step):
            self._run_step()
    def run_steps(self,step=1):
        self._run_steps(step)
    def nha_ha(self):
        c=0
        while True:
            if c>4:
                print('alo')
                self.motor1.stop()
                self.motor2.stop()
                self.motor2.run(400)
                self.motor1.run(-400)
                time.sleep(1.71)
                self.motor2.run(800)
                self.motor1.run(800)
                time.sleep(2.8)
                self.motor2.run(400)
                self.motor1.run(-400)
                time.sleep(1.71)
                c=0
            else:   
                self.motor1.run(self.speed[1])
                self.motor2.run(self.speed[1])
                time.sleep(2)
                self.motor1.stop()
                self.motor2.stop()
                time.sleep(0.5)
                self.motor1.run(self.speed[1])
                time.sleep(2)
                self.motor1.stop()
                time.sleep(2)
                ###nhả hạt###
                self.motor1.run(self.speed[4])
                time.sleep(2)
                self.motor1.stop()
                self.motor2.run(self.speed[1])
                time.sleep(2)
                self.motor2.stop()
                time.sleep(2)
                ###nhả hạt###
                self.motor2.run(self.speed[4])
                time.sleep(2)
                self.motor2.stop()
                print(c)
####----run theo line
    def run_theoline(self,cm):
        #print('vcl')
        while cm >0:
                adcs=self.adcs.line()
                if adcs[0] == True and adcs[1] == True and adcs[2] == True and adcs[3] == True:  
                    self.motor1.run(self.speed[1])
                    self.motor2.run(self.speed[1])
                    cm=cm-0.01
                elif adcs[0] == True and adcs[1] == True and adcs[2] == False and adcs[3]==False:
                    self.motor1.run(self.speed[3])
                    self.motor2.run(self.speed[1])
                    cm=cm-0.01
                elif adcs[0] ==False and adcs[1] ==False and adcs[2] ==True and adcs[3] ==True:
                    self.motor1.run(self.speed[1])
                    self.motor2.run(self.speed[3])
                    cm=cm-0.01
                elif adcs[0] ==True and adcs[1] ==False and adcs[2] ==False and adcs[3] ==False: 
                    self.motor1.run(self.speed[2])
                    self.motor2.stop()
                    cm=cm-0.01
                elif adcs[0] ==False and adcs[1] ==False and adcs[2] ==False and adcs[3] ==True:
                    self.motor1.stop()
                    self.motor2.run(self.speed[2])
                    cm=cm-0.01
                elif adcs[0] ==False and adcs[1] ==True and adcs[2] ==True and adcs[3] ==False:
                    self.motor1.run(self.speed[3])
                    self.motor2.run(self.speed[3])
                    cm=cm-0.01
                elif adcs[0] ==False and adcs[1] ==True and adcs[2] ==True and adcs[3] ==True:
                    self.motor1.run(self.speed[2])
                    self.motor2.run(self.speed[3])
                    cm=cm-0.01
                elif adcs[0] ==True and adcs[1] ==True and adcs[2] ==True and adcs[3] ==False:
                    self.motor1.run(self.speed[3])
                    self.motor2.run(self.speed[2])
                    cm=cm-0.01
                elif adcs[0] ==False and adcs[1] ==False and adcs[2] ==False and adcs[3] ==False :
                    self.motor1.run(-self.speed[0])
                    self.motor2.run(-self.speed[0])
                    cm=cm-0.01
                elif adcs[0] ==False and adcs[1] ==True and adcs[2] ==False  and adcs[3] ==False:
                    self.motor1.run(self.speed[2])
                    self.motor2.run(self.speed[1])
                    cm=cm-0.01
                elif adcs[0] ==False and adcs[1] ==False  and adcs[2] ==True and adcs[3] ==False:
                    self.motor1.run(self.speed[1])
                    self.motor2.run(self.speed[2])
                    cm=cm-0.01
                else:
                    cm=cm-0.01
                    self.motor1.stop()
                    self.motor2.stop()
                ##print(cm)
        while cm<0:
                #print('vcl')#very cool lib
                self.motor1.stop()
                self.motor2.stop()
                break

