# import sys
import smbus
# import math

class MPU6050:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.address = 0x68
        self.power_managment = 0x6B
        sample_rate = 0x19
        config_accel = 0x1A
        config_gyro = 0x1B
        int_enable = 0x38

        self.accel_x = 0x3B
        self.accel_y = 0x3D
        self.accel_z = 0x3F

        self.gyro_x = 0x43
        self.gyro_y = 0x45
        self.gyro_z = 0x47

        self.bus.write_byte_data(self.address, self.power_managment, 1)
        self.bus.write_byte_data(self.address, sample_rate, 7)
        self.bus.write_byte_data(self.address, config_accel, 0)
        self.bus.write_byte_data(self.address, config_gyro, 24)
        self.bus.write_byte_data(self.address, int_enable, 1)

    def read_data(self, add):
        high = self.bus.read_byte_data(self.address, add)
        low = self.bus.read_byte_data(self.address, add+1)

        value = ((high << 8) | low)

        if value > 32768:
            value = value - 65536

        return value

    '''def distance(self, a, b):
        return math.sqrt((a*a) + (b*b))

    def get_raw_gyro(self):
        values = [read_data(gyro_x), read_data(gyro_y), read_data(gyro_z)]
        return values

    def get_raw_accel(self):
        values = [read_data(accel_x), read_data(accel_y), read_data(accel_z)]
        return values'''

    def get_angle_gyro(self):
        gyro_angle = [self.read_data(self.gyro_x)/16384.0,
                      self.read_data(self.gyro_y)/16384.0,
                      self.read_data(self.gyro_z)/16384.0]
        return gyro_angle

    def get_angle_accel(self):
        accel_angle = [self.read_data(self.accel_x)/131.0,
                       self.read_data(self.accel_y)/131.0,
                       self.read_data(self.accel_z)/131.0]
        return accel_angle

mpu = MPU6050()
print(f'accel: {mpu.get_angle_accel}')
print(f'gyro: {mpu.get_angle_gyro}')
