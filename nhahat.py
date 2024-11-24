import rpy.hmc5883l as hmc5883l
import time
laban=hmc5883l.HMC5883L(scl=5,sda=4)
while True:
    print(laban.heading())
    time.sleep(1)
    
