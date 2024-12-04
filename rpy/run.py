import machine #type: ignore
import time #type: ignore
class LOG:
    def __init__(self):
        pass
    def log(self,msg):
        time.sleep(1)
        print(msg)
class RUN:
    __timeconf__=0.1
    __timeangle__=0.02
    __aspeed_1__=200
    __aspeed_2__=400
    __aspeed_3__=700
    __aspeed_4__=800
    __bspeed_1__=250
    __bspeed_2__=450
    __bspeed_3__=750
    __bspeed_4__=850
    def __init__(self):
        self.adc0=machine.ADC(machine.Pin(33))
        self.adc1=machine.ADC(machine.Pin(34))
        self.adc2=machine.ADC(machine.Pin(35))
        self.adc3=machine.ADC(machine.Pin(36))
        
        self.adc0.atten(machine.ADC.ATTN_11DB)
        self.adc1.atten(machine.ADC.ATTN_11DB)
        self.adc2.atten(machine.ADC.ATTN_11DB)
        self.adc3.atten(machine.ADC.ATTN_11DB)
        
        self.ain = machine.Pin(4, mode=machine.Pin.OUT)
        self.ain.value(0)
        self.pwa = machine.PWM(machine.Pin(12), freq = 50, duty=0)
        
        self.bin = machine.Pin(16, mode=machine.Pin.OUT)
        self.bin.value(0)
        self.pwb = machine.PWM(machine.Pin(13), freq = 50, duty=0)
        
    def readadcs(self):
        return self.adc0.read(),self.adc1.read(),self.adc2.read(),self.adc3.read()
    def turn_find(self,lr,r=10):
        t=self.__timeangle__*abs(r)
        if lr>0:
            self.ain.value(0)
            self.bin.value(1)
        else:
            self.ain.value(1)
            self.bin.value(0)
        self.pwa.duty(self.__aspeed_2__)
        self.pwb.duty(self.__bspeed_2__)
        time.sleep(t)
        while True:
            adc0 = self.adc0.read()
            adc1 = self.adc1.read()
            adc2 = self.adc2.read()
            adc3 = self.adc3.read()
            if adc0>2360:
                while True:
                    adc2 = self.adc2.read()
                    if adc2>2250:
                        self.pwa.duty(0)
                        self.pwb.duty(0)
                        break
                break
            if adc3>2500:
                while True:
                    adc1 = self.adc1.read()
                    if adc1>2360:
                        self.pwa.duty(0)
                        self.pwb.duty(0)
                        break
                break
            self.pwa.duty(self.__aspeed_2__)
            self.pwb.duty(self.__bspeed_2__)
    def turn(self,r=0):
        t=self.__timeangle__*abs(r)
        if r>0:
            self.ain.value(0)
            self.bin.value(1)
        else:
            self.ain.value(1)
            self.bin.value(0)
        self.pwa.duty(self.__aspeed_2__)
        self.pwb.duty(self.__bspeed_2__)
        time.sleep(t)
        self.pwa.duty(0)
        self.pwb.duty(0)
    def run_find(self,fb,cm=3):
        if fb>0:
            self.ain.value(0)
            self.bin.value(0)
        else:
            self.ain.value(1)
            self.bin.value(1)
        while True:
            adc0 = self.adc0.read()
            adc1 = self.adc1.read()
            adc2 = self.adc2.read()
            adc3 = self.adc3.read()
            if adc1>2360 and adc2>2250:
                self.pwa.duty(0)
                self.pwb.duty(0)
                break
            self.pwa.duty(self.__aspeed_2__)
            self.pwb.duty(self.__bspeed_2__)
    def run_cm(self,cm):
        t=self.__timeconf__*abs(cm)
        if cm>0:
            self.ain.value(0)
            self.bin.value(0)
        else:
            self.ain.value(1)
            self.bin.value(1)
        self.pwa.duty(self.__aspeed_2__)
        self.pwb.duty(self.__bspeed_2__)
        time.sleep(t)
        self.pwa.duty(0)
        self.pwb.duty(0)
        return cm
    def run_step(self,cm=3):
        self.ain.value(0)
        self.bin.value(0)
        while True:
            adc0 = self.adc0.read()
            adc1 = self.adc1.read()
            adc2 = self.adc2.read()
            adc3 = self.adc3.read()
            if adc0>2850 and adc1>2360 and adc2>2250 and adc3>2500:
                while True:
                    adc0 = self.adc0.read()
                    adc3 = self.adc3.read()
                    if adc0<2850 and adc3<2500:
                        self.pwa.duty(0)
                        self.pwb.duty(0)
                        break
                break
            if  adc1<2360 and adc2<2250:
                if adc0>2850:
                    self.pwa.duty(self.__aspeed_1__)
                    self.pwb.duty(self.__bspeed_4__)
                elif adc3>2500:
                    self.pwa.duty(self.__aspeed_4__)
                    self.pwb.duty(self.__bspeed_1__)
                else:
                    self.pwa.duty(0)
                    self.pwb.duty(0)
                    code=1
                    break
            if adc1<2360:
                self.pwa.duty(self.__aspeed_3__)
            else:
                self.pwa.duty(self.__aspeed_2__)
            if adc2<2250:
                self.pwb.duty(self.__bspeed_3__)
            else:
                self.pwb.duty(self.__bspeed_2__)
    def stop(self):
        self.pwa.duty(0)
        self.pwb.duty(0)
if __name__ == "__main__":
    run=RUN()
    log=LOG()
    while True:
        run.run_cm(10)
        run.run_find(1)
        run.run_cm(5)
        run.turn_find(1)
        log.log(1)
        run.run_step()
        log.log(2)
        run.run_cm(5)
        log.log(3)
        run.turn_find(1)
        log.log(6)
        run.run_step()
        log.log(7)
        run.run_step()
        log.log(8)
        run.turn_find(-1)
        log.log(9)
        run.run_step()
        log.log(10)
        run.run_step()
        log.log(11)
        time.sleep(3)