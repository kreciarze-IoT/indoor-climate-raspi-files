import array
import dbus

from krecik_iot_controller.services.bluetooth.cputemp.exceptions import InvalidArgsException, NotSupportedException, NotPermittedException
from krecik_iot_controller.services.bluetooth.cputemp.constants import DBUS_PROP_IFACE, GATT_DESC_IFACE

class Descriptor(dbus.service.Object):
    def __init__(self, uuid, flags, characteristic):
        index = characteristic.get_next_index()
        self.path = characteristic.path + '/desc' + str(index)
        self.uuid = uuid
        self.flags = flags
        self.chrc = characteristic
        self.bus = characteristic.get_bus()
        dbus.service.Object.__init__(self, self.bus, self.path)

    def get_properties(self):
        return {
            GATT_DESC_IFACE: {
                'Characteristic': self.chrc.get_path(),
                'UUID': self.uuid,
                'Flags': self.flags,
            }
        }

    def get_path(self):
        return dbus.ObjectPath(self.path)

    @dbus.service.method(DBUS_PROP_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface):
        if interface != GATT_DESC_IFACE:
            raise InvalidArgsException()

        return self.get_properties()[GATT_DESC_IFACE]

    @dbus.service.method(GATT_DESC_IFACE,
                         in_signature='a{sv}',
                         out_signature='ay')
    def ReadValue(self, options):
        print('Default ReadValue called, returning error')
        raise NotSupportedException()

    @dbus.service.method(GATT_DESC_IFACE, in_signature='aya{sv}')
    def WriteValue(self, value, options):
        print('Default WriteValue called, returning error')
        raise NotSupportedException()


class CharacteristicUserDescriptionDescriptor(Descriptor):
    CUD_UUID = '2901'

    def __init__(self, bus, index, characteristic):
        self.writable = 'writable-auxiliaries' in characteristic.flags
        self.value = array.array('B', b'This is a characteristic for testing')
        self.value = self.value.tolist()
        Descriptor.__init__(
            self, bus, index,
            self.CUD_UUID,
            ['read', 'write'],
            characteristic)

    def ReadValue(self, options):
        return self.value

    def WriteValue(self, value, options):
        if not self.writable:
            raise NotPermittedException()
        self.value = value
