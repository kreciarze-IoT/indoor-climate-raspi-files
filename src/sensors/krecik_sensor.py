import datetime

from bmp280 import BMP280

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

class KrecikSensor:
    def __init__(self):
        self.bus = SMBus(1)
        self.bmp280 = BMP280(i2c_dev=self.bus)

    def get_temperature(self):
        return round(self.bmp280.get_temperature(),2)

    def get_pressure(self):
        return round(self.bmp280.get_pressure(),2)

    def get_time(self):
        current_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
        return datetime.datetime.now(current_timezone).isoformat(timespec='milliseconds')

    def get_data(self):
        return {
            'time':self.get_time(),
            'temperature': self.get_temperature(),
            'pressure': self.get_pressure()
        }
