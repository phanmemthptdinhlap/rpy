import rpy.servo as servo
import time
import machine #type: ignore
class NhaLac:
  def __init__(self,pina,pinb,pinc):
     self.ser1=servo.SERVO(machine.Pin(pina))
     self.ser2=servo.SERVO(machine.Pin(pinb))
     self.adc=machine.ADC(machine.Pin(pinc))
     self.adc.atten(machine.ADC.ATTN_11DB)
     self.ser1.move(90)
  def nhalac(self):
    try:
      self.ser2.move(0)
      value = self.adc.read()
      print(value)
      while value<3700:
        self.ser1.move(0)
        value = self.adc.read()
        print(value)
      self.ser1.move(90)
      time.sleep(1)
      while value>3900:
        value = self.adc.read()
        print(value)
        self.ser2.move(90)
      time.sleep(1)
      self.ser2.move(0)
      return True
    except:
       return False
  def __call__(self):
        self.nhalac()
def main():
  nhalac=NhaLac(6,8,0)
  while True:
    nhalac()
    time.sleep(5)
if __name__ == '__main__':
    main()