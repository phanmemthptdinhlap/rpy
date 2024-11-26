import rpy.hmc5883l as hmc5883l
import time
laban=hmc5883l.HMC5883L(scl=22,sda=21)
while True:
    print(laban.heading())
    time.sleep(1)
