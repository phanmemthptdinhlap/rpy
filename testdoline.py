import rpy.DoLine as DoLine
import time
doline=DoLine.DOLINE(pin=13,sample=(2200,2200,2200,2200),offset=(0,0),speed=(300,700,900,1000))
while True:
    doline.run_steps(1)
    time.sleep(3)