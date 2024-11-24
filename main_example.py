from rpy.mpu6050 import MPU6050
from rpy import mpu6050 as mpu
import time
mpu6050 = MPU6050(addr=0x68, scl=5, sda=4)
mpu6050.set_accel_range(mpu._ACC_RNG_8G)
mpu6050.set_gyro_range(mpu._GYR_RNG_500DEG)
def main():
  while True:
    print(mpu6050.read_accel_data())
    time.sleep(0.05)
if __name__ == '__main__':
    main()