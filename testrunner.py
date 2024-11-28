import rpy.runner as runner
import rpy.hmc5883l as hmc5883l
import time
#run=runner.RUNER(offset=(0,0),speed=(450,700,900,1000))
hmc=hmc5883l.HMC5883L(scl=22,sda=21)
hmc.auto_update_declination()
while True:
    #run._Turn(90)
    angle,_=hmc.heading()
    print(angle)
    time.sleep(1)