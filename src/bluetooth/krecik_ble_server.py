from bluetooth.cputemp.ble_server import ble_server
from bluetooth.krecik_ble_config import KrecikService, KrecikAdvertisement

import threading
import json
from time import sleep
from cryptography.fernet import Fernet, InvalidToken


class KrecikBleServer:
    def __init__(
            self,
            bt_token
    ):
        self.fernet = None
        if bt_token is not None:
            try:
                self.fernet = Fernet(bt_token)
            except ValueError:
                raise

        print(f"Initializing Krecik BLE server with{'' if bt_token is not None else 'out'} encryption.")

        self.server = ble_server()

        self.service = KrecikService(0)

        self.server.add_service(self.service)
        self.server.add_advertisement(KrecikAdvertisement(0))
        self.server.register()

    def run(self):
        print("Krecik BLE server started.")
        t = threading.Thread(target=self.server.run, args=[])
        t.start()

    def get_data(self):
        try:
            data = self.service.get_data()
            if self.fernet is not None:
                data = bytes(data, encoding='utf-8')
                data = self.fernet.decrypt(data).decode('utf-8')
            json_data = json.loads(data)
            return json_data
        except InvalidToken:
            raise RuntimeError("T: Invalid token")
        except json.decoder.JSONDecodeError:
            raise RuntimeError("D: Invalid data")
        except RuntimeError:
            raise

    def set_message(self, message):
        try:
            self.service.set_message(message)
        except RuntimeError:
            raise

        if message not in ['R', 'S']:
            t = threading.Thread(target=self.__time_reset_msg, args=[5])
            t.start()

    def __time_reset_msg(self, delay=5):
        sleep(delay)
        self.service.set_message('R')

    def quit(self, delay=0):
        sleep(delay)
        print("Krecik BLE server stopped.")
        self.server.quit()
