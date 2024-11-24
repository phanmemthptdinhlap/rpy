import math
import machine # type: ignore

from ustruct import pack # type: ignore
from array import array


class HMC5883L:
    """ HMC5883L là một là bàn số sử dụng i2c để giao tiếp với vi điều khiển
        Kết nối các chân cơ bản như sau:

        HMC5883L    ESP32

        SCL         SCL:22
        SDA         SDA:21
        VCC         VCC:3.3v
        GND         GND
       """
    __gain__ = {
        '0.88': (0 << 5, 0.73),
        '1.3':  (1 << 5, 0.92),
        '1.9':  (2 << 5, 1.22),
        '2.5':  (3 << 5, 1.52),
        '4.0':  (4 << 5, 2.27),
        '4.7':  (5 << 5, 2.56),
        '5.6':  (6 << 5, 3.03),
        '8.1':  (7 << 5, 4.35)
    }

    def __init__(self, scl=22, sda=21, address=30, gauss='1.3', declination=(0, 0)):
        """ Khởi tạo lớp HMC5883L.

        Tham số truyền vào:
            scl (int): chân xung đồng hồ, mặc định 22.
            sda (int): chân dữ liệu,mặc định  21.
            address (int): địa chỉ, mặc định  30.
            gauss (str): mặc định '1.3'.
            declination (tuple): điều chỉnh hướng, mặc định  (0, 0).
        """
        self.i2c = i2c = machine.I2C(scl=machine.Pin(scl), sda=machine.Pin(sda), freq=100000)

        # Initialize sensor.
        i2c.start()

        # Configuration register A:
        #   0bx11xxxxx  -> 8 samples averaged per measurement
        #   0bxxx100xx  -> 15 Hz, rate at which data is written to output registers
        #   0bxxxxxx00  -> Normal measurement mode
        i2c.writeto_mem(30, 0x00, pack('B', 0b111000))

        # Configuration register B:
        reg_value, self.gain = self.__gain__[gauss]
        i2c.writeto_mem(30, 0x01, pack('B', reg_value))

        # Set mode register to continuous mode.
        i2c.writeto_mem(30, 0x02, pack('B', 0x00))
        i2c.stop()

        # Convert declination (tuple of degrees and minutes) to radians.
        self.declination = (declination[0] + declination[1] / 60) * math.pi / 180

        # Reserve some memory for the raw xyz measurements.
        self.data = array('B', [0] * 6)

    def read(self):
        """ Đọc dữ liệu từ HMC5883L.

        Giá trị trả lại:
            giá trị: (x, y, z)
        """
        data = self.data
        gain = self.gain

        self.i2c.readfrom_mem_into(30, 0x03, data)

        x = (data[0] << 8) | data[1]
        z = (data[2] << 8) | data[3]
        y = (data[4] << 8) | data[5]

        x = x - (1 << 16) if x & (1 << 15) else x
        y = y - (1 << 16) if y & (1 << 15) else y
        z = z - (1 << 16) if z & (1 << 15) else z

        x = round(x * gain, 4)
        y = round(y * gain, 4)
        z = round(z * gain, 4)

        return x, y, z

    def _heading(self, x, y):
        """ Tính hướng.

        Tham số truyền vào:
            x (float): Giá trị x.
            y (float): Giá trị y.

        Giá trị trả lại:
            hướng: (độ,phút)
        """
        heading_rad = math.atan2(y, x)
        heading_rad += self.declination

        # Correct reverse heading.
        if heading_rad < 0:
            heading_rad += 2 * math.pi

        # Compensate for wrapping.
        elif heading_rad > 2 * math.pi:
            heading_rad -= 2 * math.pi

        # Convert from radians to degrees.
        heading = heading_rad * 180 / math.pi
        degrees = math.floor(heading)
        minutes = round((heading - degrees) * 60)
        return degrees, minutes

    def heading(self):
        """ Lấy hướng.
         Giá trị trả lại:
            hướng: (độ, phút)
        """
        x,y,z = self.read()
        return self._heading(x,y)
    def __call__ (self):
        x, y, z = self.read()
        degrees, minutes = self._heading(x, y)
        return {'xyz': (x, y, z), 'heading': (degrees,minutes)} #{'x': x, 'y': y, 'z': z, 'degrees': degrees, 'minutes': minutes} 
    def __str__ (self):
        return self.format_result(*self.read())
    def format_result(self, x, y, z):
        degrees, minutes = self._heading(x, y)
        return 'X: {:.4f}, Y: {:.4f}, Z: {:.4f}, Heading: {}° {}′ '.format(x, y, z, degrees, minutes)