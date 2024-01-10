import json

from krecik_iot_controller.services.bluetooth.krecik_ble_server import KrecikBleServer
from krecik_iot_controller.services.krecik_sensor import KrecikSensor
from krecik_iot_controller.services.datasource import Datasource

from time import sleep
import subprocess
import requests

from queue import Queue


class KrecikIOTController:

    def __init__(
            self,
            bt_token,
            bt_iv,
            datasource_config_file="conf/datasource.json",
    ):
        self.ble_server = None
        self.request_queue = Queue()

        print("Szczesc Boze!")
        self.datasource = Datasource(
            bt_token=bt_token,
            bt_iv=bt_iv,
            conf_file=datasource_config_file
        )

        self.sensor_service = KrecikSensor()

        needs_configuration = True
        while needs_configuration:
            needs_configuration = False

            # init datasource
            needs_test = False
            if not self.datasource.is_configured():
                print("Data source not configured.")
                needs_test = True
                self._initialize_datasource()

            # init wifi
            if not self._is_connected_to_wifi():
                print("Chosen wifi not connected.")
                try:
                    self._connect_to_wifi()
                    sleep(5)
                    print("Connected to wifi.")
                except RuntimeError:
                    print("Wifi not configured.")
                    needs_configuration = True
                    continue
            else:
                print("Wifi connected.")

            if needs_test:
                print("First use test...", end=" ")
                data = self.sensor_service.get_data()
                status = self._send_data_to_server(data, verbose=False)
                success = status == 0
                if not success:
                    print(f"Failed. Could not connect to server on initial run ({status}). Resetting data source.")
                    self.datasource.reset_data()
                    needs_configuration = True
                else:
                    print("Success!")
                    needs_configuration = False

        print("Krecik IOT controller initialized.")

    def _initialize_datasource(self):

        print("Started datasource initialization process.")

        if self.ble_server is None:
            self.ble_server = KrecikBleServer(
                bt_token=self.datasource.get_bt_token(),
                bt_iv=self.datasource.get_bt_iv(),
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
                    print("Received data... Success!")
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
        ssid = '\\ '.join(ssid.split(' '))

        print("Connecting to wifi...")

        connect_to_wifi_cmd = "sudo nmcli d wifi c".split(' ')
        connect_to_wifi_cmd += [f"{ssid}"]
        connect_to_wifi_cmd += f"password {password}".split(' ')
        try:
            cmd_output = subprocess.check_output(
                ' '.join(connect_to_wifi_cmd),
                shell=True
            ).decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            return

        if cmd_output.startswith('Error:'):
            return

    def _is_connected_to_wifi(self):
        check_connection_cmd = "nmcli -t -f name connection show --active"

        cmd_output = subprocess.check_output(
            check_connection_cmd,
            shell=True
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

    def _send_data_to_server(self, data_dict, verbose=True):
        url = self.__get_backend_url("/records")
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.datasource.get_auth_token()}"
        }

        if not self._is_connected_to_wifi():
            self._connect_to_wifi()
            sleep(.5)
            if not self._is_connected_to_wifi():
                if verbose:
                    print("Not connected to wifi.")
                return 1

        data = json.loads(json.dumps(data_dict))

        try:
            response = requests.post(url, headers=headers, json=data)
        except Exception as e:
            if verbose:
                print("Error sending data to server.")
            return 2

        if response.status_code <= 100 or response.status_code >= 300:
            if verbose:
                print("Error response: " + str(response.json()) + f"(code {response.status_code}).")
            return 3

        return 0

    def run(self, sleep_interval_s):
        print("Imma send some temperature to server now idk...")
        try:
            while True:
                data = self.sensor_service.get_data()
                print("Sending data...", end=" ")
                success = self._send_data_to_server(data) == 0
                if success:
                    print("Success!")
                else:
                    print("Failed. Putting data to queue.")
                    self.request_queue.put(data)

                while success and (not self.request_queue.empty()):
                    try:
                        print("Sending data from queue...")
                        data = self.request_queue.get()
                        success = self._send_data_to_server(data) == 0
                        if not success:
                            print("Failed. Putting data back to queue.")
                            self.request_queue.put(data)
                            break
                    except RuntimeError:
                        print("Failed. Putting data back to queue.")
                        self.request_queue.put(data)
                        break

                sleep(sleep_interval_s)
        except KeyboardInterrupt:
            return
