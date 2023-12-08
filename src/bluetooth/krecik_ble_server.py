from .cputemp.ble_server import ble_server
from .krecik_ble_config import ThermometerService, ThermometerAdvertisement

import threading


class krecik_ble_server:
    def __init__(self):
        self.server = ble_server()

        # @TODO: zaktualizować serwisy i advertisment
        self.server.add_service(ThermometerService(0))
        self.server.add_advertisement(ThermometerAdvertisement(0))
        self.server.register()

    def run(self):
        # self.server.run()
        t = threading.Thread(target=self.server.run, args=[])
        t.start()
        # return t

    def quit(self):
        self.server.quit()
