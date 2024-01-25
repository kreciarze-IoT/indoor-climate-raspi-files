from krecik_iot_controller.services.bluetooth.cputemp.ble_server import ble_server
from krecik_iot_controller.services.bluetooth.krecik_ble_config import KrecikService, KrecikAdvertisement
from krecik_iot_controller.services.aes_cipher import AESCipher

import threading
import json
from time import sleep


class KrecikBleServer:
    def __init__(
            self,
            bt_token,
            bt_iv,
            device_id
    ):
        self.device_id = device_id
        self.crypto_service = None
        if bt_token is not None or bt_iv is not None:
            if bt_token is None or bt_iv is None:
                raise RuntimeError("D: Invalid encryption parameters")
            try:
                self.crypto_service = AESCipher(bt_token, bt_iv)
            except Exception:
                raise

        print(
            f"Initializing Krecik BLE server with{'' if bt_token is not None else 'out'} encryption.")

        self.valid_states = {
            'R': "Ready for config",
            'P': "Publish device_id",
            'S': "Success: configuring",
            'T': "Failed: invalid token",
            'D': "Failed: invalid data"
        }

        self.kill_threads = False

        self.server = ble_server()

        self.service = KrecikService(0)

        self.server.add_service(self.service)
        self.server.add_advertisement(KrecikAdvertisement(0))
        self.server.register()
        self.set_message('R')

    def run(self):
        print("Krecik BLE server started.")
        t = threading.Thread(target=self.server.run, args=[])
        t.start()

    def get_data(self):
        try:
            data = self.service.get_data()
            if self.crypto_service is not None:
                data = bytes(data, encoding='utf-8')
                data = self.crypto_service.decrypt(data)
            json_data = json.loads(data)
            return json_data
        except json.decoder.JSONDecodeError:
            raise RuntimeError("D: Invalid data")
        except ValueError:
            raise RuntimeError("T: Could not decrypt data")
        except RuntimeError:
            raise

    def set_message(self, message):
        if message not in self.valid_states.keys():
            raise RuntimeError("Invalid message")
        try:
            publish_message = message
            if message == 'P':
                if self.crypto_service is not None:
                    publish_message = self.crypto_service.encrypt(
                        self.device_id).decode('utf-8')
                self.service.set_device_message(publish_message)
                t = threading.Thread(
                    target=self.__time_reset_msg, args=[5, 'P'])
                t.start()
            else:
                if self.crypto_service is not None:
                    publish_message = self.crypto_service.encrypt(
                        message).decode('utf-8')
                print("publishin some bussin data ", message)
                self.service.set_message(publish_message)
        except RuntimeError:
            raise
        if message not in ['R', 'S', 'P']:
            t = threading.Thread(target=self.__time_reset_msg, args=[5])
            t.start()

    def __time_reset_msg(self, delay=5, message='R'):
        for _ in range(delay*10):
            sleep(.1)
            if self.kill_threads:
                return
        self.set_message(message)

    def quit(self, delay=0):
        sleep(delay)
        print("Krecik BLE server stopped.")
        self.kill_threads = True
        self.server.quit()
