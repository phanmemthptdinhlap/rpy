import machine #type: ignore
import time
adc=machine.ADC(machine.Pin(15))
adc.atten(machine.ADC.ATTN_11DB)
while True:
  print(adc.read())
  time.sleep(0.1)