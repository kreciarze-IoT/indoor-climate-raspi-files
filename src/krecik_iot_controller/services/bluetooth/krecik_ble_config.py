import dbus

from krecik_iot_controller.services.bluetooth.cputemp.advertisement import Advertisement
from krecik_iot_controller.services.bluetooth.cputemp.service import Service
from krecik_iot_controller.services.bluetooth.cputemp.descriptor import Descriptor
from krecik_iot_controller.services.bluetooth.cputemp.characteristic import Characteristic

NOTIFY_TIMEOUT = 5000


class KrecikAdvertisement(Advertisement):
    def __init__(self, index):
        Advertisement.__init__(self, index, "peripheral")
        self.add_local_name("KrecikIOT")
        self.include_tx_power = True


class KrecikService(Service):
    SERVICE_UUID = "00000001-710e-4a5b-8d75-3e5b444bc3cf"

    def __init__(self, index):
        self.data = ""

        Service.__init__(self, index, self.SERVICE_UUID, True)
        self.characteristic = KrecikCharacteristic(self)
        self.add_characteristic(self.characteristic)

    def get_data(self):
        if self.data != "":
            data = self.data
            self.data = ""
            return data
        raise RuntimeError("No data")

    def set_message(self, message):
        self.characteristic.message = message



class KrecikCharacteristic(Characteristic):
    UNIT_CHARACTERISTIC_UUID = "00000004-710e-4a5b-8d75-3e5b444bc3cf"

    def __init__(self, service):
        Characteristic.__init__(
            self, self.UNIT_CHARACTERISTIC_UUID,
            ["read", "write"], service)

        self.add_descriptor(KrecikDescriptor(self))

        self.message = ""

    def WriteValue(self, value, options):
        data = ""
        for v in value:
            data += chr(v)

        self.service.data = data

    def ReadValue(self, options):

        value = []

        for c in self.message:
            value.append(dbus.Byte(c.encode()))

        return value


class KrecikDescriptor(Descriptor):
    UNIT_DESCRIPTOR_UUID = "2901"
    UNIT_DESCRIPTOR_VALUE = (
        "Krecik IOT unit.\n"
        "Write configuration data to this characteristic."
    )

    def __init__(self, characteristic):
        Descriptor.__init__(
            self, self.UNIT_DESCRIPTOR_UUID,
            ["read"],
            characteristic)

        # self.UNIT_DESCRIPTOR_VALUE

    def ReadValue(self, options):
        value = []

        for c in self.UNIT_DESCRIPTOR_VALUE:
            value.append(dbus.Byte(c.encode()))

        return value


class ThermometerAdvertisement(Advertisement):
    def __init__(self, index):
        Advertisement.__init__(self, index, "peripheral")
        self.add_local_name("Thermometer")
        self.include_tx_power = True
