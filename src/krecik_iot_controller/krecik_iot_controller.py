import json

import numpy as np

from bluetooth.krecik_ble_server import KrecikBleServer
from sensors.krecik_sensor import KrecikSensor
from services.datasource import Datasource

from time import sleep
import subprocess
import requests

from queue import Queue


class KrecikIOTController:

    def __init__(
            self,
            bt_token,
            encrypt=True,
            datasource_config_file="conf/datasource.json",
    ):
        self.encrypt_bt = encrypt
        self.ble_server = None
        self.request_queue = Queue()

        print("Szczesc Boze!")
        self.datasource = Datasource(
            bt_token=bt_token,
            conf_file=datasource_config_file
        )

        self.sensor_service = KrecikSensor()

        # init datasource
        if not self.datasource.is_configured():
            print("Data source not configured.")
            self._initialize_datasource()

        # init wifi
        print("Chosen wifi not connected.")
        try:
            self._connect_to_wifi()
            print("Connected to wifi.")
        except RuntimeError:
            print("Wifi not configured.")
            return

    def _initialize_datasource(self):

        print("Started datasource initialization process.")

        if self.ble_server is None:
            self.ble_server = KrecikBleServer(
                bt_token=self.datasource.get_bt_token()
            )
        ble = self.ble_server
        ble.run()
        print("Krecik BLE server running. Waiting for data...")

        try:

            awaiting_data = True
            while awaiting_data:
                try:
                    data_from_phone = ble.get_data()

                    self.datasource.load_data_from_json(
                        data_from_phone,
                        save=True
                    )
                    ble.set_message("S")

                    awaiting_data = False
                except RuntimeError as e:
                    if str(e)[1] == ':':
                        print("Received data...", end=" ")
                        ble.set_message(str(e)[0])
                        print(str(e)[3:])
                    sleep(1)
            ble.quit(delay=5)  # time to read accepted state
            print("Data source configured.")

        except KeyboardInterrupt:
            ble.quit()
            exit()

    def _connect_to_wifi(self):
        ssid = self.datasource.get_wifi_ssid()
        password = self.datasource.get_wifi_password()

        if ssid is None or password is None:
            raise RuntimeError("Wifi not configured.")

        print("Connecting to wifi...")

        connect_to_wifi_cmd = "nmcli d wifi c".split(' ')
        connect_to_wifi_cmd += [f"{ssid}"]
        connect_to_wifi_cmd += f"password {password}".split(' ')
        try:
            cmd_output = subprocess.check_output(
                connect_to_wifi_cmd
            ).decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            return

        if cmd_output.startswith('Error:'):
            return

    def _is_connected_to_wifi(self):
        check_connection_cmd = "nmcli -t -f name connection show --active"

        cmd_output = subprocess.check_output(
            check_connection_cmd.split(' ')
        )
        cmd_output = cmd_output.decode('utf-8').strip()
        cmd_output = cmd_output.split('\n')
        cmd_output = [c.strip() for c in cmd_output]

        if self.datasource.get_wifi_ssid() not in cmd_output:
            return False

        return True

    def __get_backend_url(self, endpoint="/"):
        host = self.datasource.get_host()
        if host is None:
            raise RuntimeError("Datasource not configured.")
        if host[-1] == '/':
            host = host[:-1]
        if endpoint[0] == '/':
            endpoint = endpoint[1:]
        return f"{host}/{endpoint}"

    def _send_data_to_server(self, data_dict):
        url = self.__get_backend_url("/records")  # mock @TODO: change
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.datasource.get_auth_token()}"
        }

        if not self._is_connected_to_wifi():
            self._connect_to_wifi()
            sleep(.5)
            if not self._is_connected_to_wifi():
                print("Not connected to wifi. Putting data to queue.")
                self.request_queue.put(data_dict)
                return

        data = json.loads(json.dumps(data_dict))

        response = requests.post(url, headers=headers, json=data)

        if response.status_code <= 100 or response.status_code >= 300:
            print("Error response: " + str(response.json()) + f"(code {response.status_code}). Putting data to queue.")
            self.request_queue.put(data_dict)
            return

        print("Success response: " + str(response.json()))

    def run(self, sleep_interval_s):
        print("Imma send some temperature to server now idk...")
        try:
            while True:
                data = self.sensor_service.get_data()
                try:
                    self._send_data_to_server(data)
                except RuntimeError:
                    return

                while not self.request_queue.empty():
                    try:
                        print("Sending data from queue...")
                        data = self.request_queue.get()
                        self._send_data_to_server(data)
                    except RuntimeError:
                        break

                sleep(sleep_interval_s)
        except KeyboardInterrupt:
            return
