import rpy.servo as servo
import time
import machine #type: ignore
class NhaLac:
  def __init__(self,pins1,pins2,pinadc):
     self.ser1=servo.SERVO(machine.Pin(pins1))
     self.ser2=servo.SERVO(machine.Pin(pins2))
     self.adc=machine.ADC(machine.Pin(pinadc))
     self.adc.atten(machine.ADC.ATTN_11DB)
     self.ser1.move(90)
  def colac(self):
     value=self.adc.read()
     print(value)
     return True if value>2000 else False
  def _laylac(self):
    try:
      self.ser2.move(30)
      while not self.colac():
        self.ser1.move(0)
      self.ser1.move(80)
      return True
    except:
       return False
  def nhalac(self):
    try:
      while self.colac():
        self.ser2.move(80)
      time.sleep(1)
      self.ser2.move(30)
      return True
    except:
       return False
  def __call__(self):
        self.nhalac()