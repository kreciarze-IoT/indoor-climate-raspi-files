#!/usr/bin/env python

import sys
import pytz
import time
import requests
from datetime import datetime

from bmp280 import BMP280

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

print("""temperature-and-pressure.py - Displays the temperature and pressure.

Press Ctrl+C to exit!

""")


def post_record(device_bearer_token: str = '', temperature: float = 0., pressure: float = 0.) -> requests:
    if device_bearer_token == '':
        raise ValueError('Device bearer token is empty')
    url = "https://krecik.bieda.it/records"
    timezone = pytz.timezone('Europe/Warsaw')
    current_time = datetime.now(timezone).isoformat(
        timespec='milliseconds')
    headers = {
        'Authorization': 'Bearer ' + device_bearer_token
    }
    payload = {
        "when": current_time,
        "temperature": temperature,
        "pressure": pressure
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 401:
        raise ValueError('Device bearer token is not valid')
    return response


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('Device bearer token is required')
    device_bearer_token = sys.argv[1]
    # Initialise the BMP280
    bus = SMBus(1)
    bmp280 = BMP280(i2c_dev=bus)

    while True:
        temperature = bmp280.get_temperature()
        pressure = bmp280.get_pressure()
        print('{:.2f}*C {:.2f}hPa'.format(temperature, pressure))
        post_record(device_bearer_token, round(
            temperature, 2), round(pressure, 2))
        time.sleep(1)
