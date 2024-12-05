from machine import Pin, PWM, ADC, I2C #type: ignore
import time
class SERVO:
    # these defaults work for the standard TowerPro SG90
    __servo_pwm_freq = 50
    __min_u10_duty = 26 - 0 # offset for correction
    __max_u10_duty = 123- 0  # offset for correction
    min_angle = 0
    max_angle = 180
    current_angle = 0.001

    def __init__(self, pin):
        self.__initialise(pin)

    def update_settings(self, servo_pwm_freq, min_u10_duty, max_u10_duty, min_angle, max_angle, pin):
        self.__servo_pwm_freq = servo_pwm_freq
        self.__min_u10_duty = min_u10_duty
        self.__max_u10_duty = max_u10_duty
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.__initialise(pin)

    def move(self, angle):
        # round to 2 decimal places, so we have a chance of reducing unwanted servo adjustments
        angle = round(angle, 2)
        # do we need to move?
        if angle == self.current_angle:
            return
        self.current_angle = angle
        # calculate the new duty cycle and move the motor
        duty_u10 = self.__angle_to_u10_duty(angle)
        self.__motor.duty(duty_u10)

    def __angle_to_u10_duty(self, angle):
        return int((angle - self.min_angle) * self.__angle_conversion_factor) + self.__min_u10_duty

    def __initialise(self, pin):
        self.current_angle = -0.001
        self.__angle_conversion_factor = (self.__max_u10_duty - self.__min_u10_duty) / (self.max_angle - self.min_angle)
        self.__motor = PWM(Pin(pin),freq=50)
        self.__motor.freq(self.__servo_pwm_freq)
class SOWING:
    #cài đặt chân servo và chân ADC
    __pins1__=6
    __pins2__=8
    __pinadc__=0
    #Cài đặt chân nhận tin hiệu kích hoạt
    __pin_in__=12
    __pin_out__=13
    #Lạc đã nhả
    __count__=0
    def __init__(self):
        self.ser1=SERVO(Pin(self.__pins1__))
        self.ser2=SERVO(Pin(self.__pins2__))
        self.adc=ADC(Pin(self.__pinadc__))
        self.adc.atten(ADC.ATTN_11DB)
        self.ser1.move(90)
        self.pin_out=Pin(self.__pin_out__)

    def begin(self):
        irq=Pin(self.__pin_in__,Pin.IN,Pin.PULL_UP)
        while True:
            if (not irq) and (self._colac()):
                self._nhalac()
                self.__count__+=1
                print(self.__count__)
                time.sleep(1)
            if not self._colac():
                self._laylac()
                time.sleep(1)

    def _colac(self):
        value=self.adc.read()
        print(value)
        return True if value>2000 else False

    def _laylac(self):
        try:
            self.ser2.move(30)
            while not self._colac():
                time.sleep(1)
                self.ser1.move(0)
            self.ser1.move(80)
            return True
        except:
            return False

    def _nhalac(self):
        try:
            while self._colac():
                self.ser2.move(80)
                time.sleep(1)
            self.ser2.move(30)
            return True
        except:
            return False
        
if __name__ =="__main__":
    sowing=SOWING()
    sowing.begin()
