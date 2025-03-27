import machine #type: ignore
import time #type: ignore
class LOG:
    def __init__(self):
        pass
    def log(self,msg):
        time.sleep(1)
        print(msg)
class RUN:
    #Tham số cấu hình thời gian chạy
    __timeconf__=0.05 #Thời gian chạy trong 1 cm
    __timeangle__=0.01 #Thời gian quay 1 độ
    #Tham số cấu hình tốc độ động cơ
    __aspeed_1__=450 #Tốc độ 1 động cơ M1
    __aspeed_2__=550 #Tốc độ 2 động cơ M1
    __aspeed_3__=750 #Tốc độ 3 động cơ M1
    __aspeed_4__=950 #Tốc độ 4 động cơ M1
    __bspeed_1__=430 #Tốc độ 1 động cơ M2
    __bspeed_2__=530 #Tốc độ 2 động cơ M2
    __bspeed_3__=730 #Tốc độ 3 động cơ M2
    __bspeed_4__=930 #Tốc độ 4 động cơ M2
    #Tham số cấu hình cân bằng mắt đo
    __sample_1__=2790 #Chỉ số cân bằng mắt 1   
    __sample_2__=2440 #Chỉ số cân bằng mắt 2
    __sample_3__=2340 #Chị số cân bằng mắt 3
    __sample_4__=2540 #Chị số cân bằng mắt 4
    def __init__(self):
        """
        Thư viện điều khiển chuyển động của động cơ theo line
        """
        self.adc1=machine.ADC(machine.Pin(33))
        self.adc2=machine.ADC(machine.Pin(34))
        self.adc3=machine.ADC(machine.Pin(35))
        self.adc4=machine.ADC(machine.Pin(36))
        
        self.adc1.atten(machine.ADC.ATTN_11DB)
        self.adc2.atten(machine.ADC.ATTN_11DB)
        self.adc3.atten(machine.ADC.ATTN_11DB)
        self.adc4.atten(machine.ADC.ATTN_11DB)
        
        self.ain = machine.Pin(4, mode=machine.Pin.OUT)
        self.ain.value(0)
        self.pwa = machine.PWM(machine.Pin(12), freq = 50, duty=0)
        
        self.bin = machine.Pin(16, mode=machine.Pin.OUT)
        self.bin.value(0)
        self.pwb = machine.PWM(machine.Pin(13), freq = 50, duty=0)
        
    def readadcs(self):
        """Đọc các thông số mắt đo"""
        return self.adc1.read(),\
            self.adc2.read(),\
            self.adc3.read(),\
            self.adc4.read()
    def turn_find(self,lr):
        """
        Hàm quay tìm line đen:
            lr Hướng quay (1: phải, -1: trái)
            r Độ quay ban đầu mặc định: 10
        """
        if lr>0:
            self.ain.value(0)
            self.bin.value(1)
        else:
            self.ain.value(1)
            self.bin.value(0)
        self.pwa.duty(self.__aspeed_2__)
        self.pwb.duty(self.__bspeed_2__)
        while True:
            adc2 = self.adc2.read()
            adc3 = self.adc3.read()
            if adc2>self.__sample_2__ and\
                adc3>self.__sample_3__:
                break
        while True:
            adc2 = self.adc2.read()
            adc3 = self.adc3.read()
            if adc2<self.__sample_2__ and\
                adc3<self.__sample_3__:
                break
        self.pwa.duty(0)
        self.pwb.duty(0)
    def turn(self,r=0):
        """Hàm quay:
            r góc quay mặc định: 0
            r dương quay phải, 
            r âm quay trái
        """
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
    def turn2(self,r=0,fb=0):
        """Hàm quay băng một vánh:
            r góc quay mặc định: 0
            r dương quay phải, 
            r âm quay trái
        """
        t=self.__timeangle__*abs(r)*2
        if fb==0:
            self.ain.value(0 if r>0 else 1)
            self.pwa.duty(self.__aspeed_2__)
            self.pwb.duty(0)
        else:
            self.bin.value(0 if r>0 else 1)
            self.pwb.duty(self.__bspeed_2__)
            self.pwa.duty(0)
        time.sleep(t)
        self.pwa.duty(0)
        self.pwb.duty(0)
    def run_find(self,fb):
        """Hàm chạy trong vùng trắng tìm line đen:
            fb Hướng chuyển động (1: đi về trước, 0: đi về sau)
        """
        if fb>0:
            self.ain.value(0)
            self.bin.value(0)
        else:
            self.ain.value(1)
            self.bin.value(1)
        while True:
            adc2 = self.adc2.read()
            adc3 = self.adc3.read()
            if adc2>self.__sample_2__ or\
                adc3>self.__sample_3__:
                self.pwa.duty(0)
                self.pwb.duty(0)
                break
            self.pwa.duty(self.__aspeed_2__)
            self.pwb.duty(self.__bspeed_2__)
    def run_cm(self,cm):
        """
        Hàm chạy khoảng cách cm:
            cm Khoảng cách, mặc định: 0
            cm dương chạy tiến về trước, 
            cm âm chạy lùi về sau
        """
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
    def run_step(self):
        """Hàm chạy theo line đen:
            chạy tiến về trước theo line đen, 
            dừng lại khi gặp line ngang,
            Robot tự tiến thêm một chút để mắt đo 1,4 ra khỏi vạch đen
        """
        self.ain.value(0)
        self.bin.value(0)
        while True:
            adc1 = self.adc1.read()
            adc2 = self.adc2.read()
            adc3 = self.adc3.read()
            adc4 = self.adc4.read()
            if adc1>self.__sample_1__ and\
                adc2>self.__sample_2__ and\
                adc3>self.__sample_3__ and\
                adc4>self.__sample_4__:
                self.pwa.duty(0)
                self.pwb.duty(0)
                break
            if  adc1<self.__sample_1__ and\
                adc2<self.__sample_2__ and\
                adc3<self.__sample_3__ and\
                adc4<self.__sample_4__:
                self.pwa.duty(0)
                self.pwb.duty(0)
                continue
            if adc1>self.__sample_1__ and\
                adc2<self.__sample_2__ and\
                adc3<self.__sample_3__:
                self.pwa.duty(0)
                self.pwb.duty(self.__bspeed_3__)
                continue
            if adc4>self.__sample_4__ and\
                adc3<self.__sample_3__ and\
                adc2<self.__sample_2__:
                self.pwa.duty(self.__aspeed_3__)
                self.pwb.duty(0)
                continue

            if adc2<self.__sample_2__:
                self.pwa.duty(self.__aspeed_3__)
            else:
                self.pwa.duty(self.__aspeed_2__)
            if adc3<self.__sample_3__:
                self.pwb.duty(self.__bspeed_3__)
            else:
                self.pwb.duty(self.__bspeed_2__)

    def stop(self):
        """Hàm dừng chuyển động hệ thống"""
        self.pwa.duty(0)
        self.pwb.duty(0)


# Chạy thư các hàm
if __name__ == "__main__":
    run=RUN()
    log=LOG()
    while True:
        print(run.readadcs())
        time.sleep(1)