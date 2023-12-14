import dbus

try:
  from gi.repository import GObject
except ImportError:
    import gobject as GObject

from bluetooth.cputemp.constants import BLUEZ_SERVICE_NAME, DBUS_OM_IFACE, LE_ADVERTISING_MANAGER_IFACE

class BleTools(object):
    @classmethod
    def get_bus(self):
         bus = dbus.SystemBus()

         return bus

    @classmethod
    def find_adapter(self, bus):
        remote_om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, "/"),
                               DBUS_OM_IFACE)
        objects = remote_om.GetManagedObjects()

        for o, props in objects.items():
            if LE_ADVERTISING_MANAGER_IFACE in props:
                return o

        return None

    @classmethod
    def power_adapter(self):
        raise RuntimeError("I have absolutely no idea what is 'bus' here. Please don't use this method :)")

        adapter = self.get_adapter()

        adapter_props = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, adapter),
                "org.freedesktop.DBus.Properties");
        adapter_props.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))
