import json


class Datasource:
    def __init__(
            self,
            bt_token,
            bt_iv,
            conf_file
    ):
        self._BT_TOKEN = bt_token
        self._BT_IV = bt_iv
        self.conf_file = conf_file

        data = self.load_data_from_file()

        self.wifi_ssid = data['wifi_ssid']
        self.wifi_password = data['wifi_password']

        self.host = data['host']
        self.aes_key = data['aes_key']

    def load_data_from_json(self, data, save=True):

        if 'wifi_ssid' not in data \
                or 'wifi_password' not in data \
                or 'host' not in data \
                or 'aes_key' not in data:
            raise RuntimeError("D: Invalid data")

        self.wifi_ssid = data['wifi_ssid']
        self.wifi_password = data['wifi_password']

        self.host = data['host']
        self.aes_key = data['aes_key']

        if save:
            self.save_data_to_file()

    def load_data_from_file(self):
        try:
            with open(self.conf_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'wifi_ssid': None,
                'wifi_password': None,
                'host': None,
                'aes_key': None
            }

    def save_data_to_file(self):
        with open(self.conf_file, 'w') as f:
            data = {
                'wifi_ssid': self.wifi_ssid,
                'wifi_password': self.wifi_password,
                'host': self.host,
                'aes_key': self.aes_key
            }
            json.dump(data, f, indent=4)
            f.write('\n')

    def reset_data(self):
        self.wifi_ssid = None
        self.wifi_password = None
        self.host = None
        self.aes_key = None
        self.save_data_to_file()

    def is_configured(self):
        return self.wifi_ssid is not None \
            and self.wifi_password is not None \
            and self.host is not None \
            and self.aes_key is not None

    def get_bt_token(self):
        return self._BT_TOKEN

    def get_bt_iv(self):
        return self._BT_IV

    def get_wifi_ssid(self):
        return self.wifi_ssid

    def get_wifi_password(self):
        return self.wifi_password

    def set_wifi_password(self, wifi_password):
        self.wifi_password = wifi_password
        self.save_data_to_file()

    def set_wifi_ssid(self, wifi_ssid):
        self.wifi_ssid = wifi_ssid
        self.save_data_to_file()

    def set_aes_key(self, aes_key):
        self.aes_key = aes_key
        self.save_data_to_file()

    def get_aes_key(self):
        return self.aes_key

    def get_host(self):
        return self.host

    def set_host(self, host):
        self.host = host
        self.save_data_to_file()

    def __stringify_none(self, value):
        if value is None:
            return "None"
        else:
            return value

    def __str__(self):
        return "wifi_ssid: " + self.__stringify_none(self.wifi_ssid) + "\n" + \
            "wifi_password: " + self.__stringify_none(self.wifi_password) + "\n" + \
            "host: " + self.__stringify_none(self.host) + "\n" + \
            "aes_key: " + self.__stringify_none(self.aes_key)
