from rpy.adcs import ADCS
from rpy.motor import MOTOR1,MOTOR2
import machine #type: ignore

class DOLINE: 
    def __init__(self, pin=None,sample=(2200,2200,2200,2200),
                 offset=(0,0),speed=(300,700,900,1000)):
        if pin is not None:
            self.adcs=ADCS(pin=pin)
        else:
            self.adcs=ADCS()
        self.sample=sample
        self.speed=speed
        self.motor1=MOTOR2(offset[0])
        self.motor2=MOTOR1(offset[1])
    def _run_step(self):
        run=True
        while run:
            try:
                index1=2
                index2=2
                adcs=self.adcs.line()
                if adcs[0]==1 and adcs[1]==1 and adcs[2]==1 and adcs[3]==1:#0= den, 1= trang
                    self.motor1.stop()
                    self.motor2.stop()   
                    break
                if adcs[0]==0 and adcs[1]==0 and adcs[2]==1 and adcs[3]==1:#0= den, 1= trang
                    print('TH2')
                    index1=3
                    index2=4
                if adcs[0]==1 and adcs[1]==1 and adcs[2]==0 and adcs[3]==0:#0= den, 1= trang
                    print('TH3')
                    index1=4
                    index2=3
                if adcs[0]==0 and adcs[1]==1 and adcs[2]==1 and adcs[3]==1:#0= den, 1= trang
                    print('TH4')
                    index1=0
                    index2=2
                if adcs[0]==1 and adcs[1]==1 and adcs[2]==1 and adcs[3]==0:#0= den, 1= trang
                    print('TH5')
                    index1=2
                    index2=0
                if adcs[0]==1 and adcs[1]==0 and adcs[2]==0 and adcs[3]==1:#0= den, 1= trang
                    print('TH6')
                    index1=3
                    index2=3
                if adcs[0]==1 and adcs[1]==1 and adcs[2]==0 and adcs[3]==1:#0= den, 1= trang
                    print('TH7')
                    index1=1
                    index2=0
                if adcs[0]==1 and adcs[1]==0 and adcs[2]==1 and adcs[3]==1:#0= den, 1= trang
                    print('TH8')
                    index1=0
                    index2=1
                if adcs[0]==1 and adcs[1]==0 and adcs[2]==0 and adcs[3]==0:#0= den, 1= trang
                    print('TH9')
                    index1=0
                    index2=1
                if adcs[0]==0 and adcs[1]==0 and adcs[2]==0 and adcs[3]==1:#0= den, 1= trang
                    print('TH10')
                    index1=1
                    index2=0
                if adcs[0]==0 and adcs[1]==0 and adcs[2]==0 and adcs[3]==0:#0= den, 1= trang
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
