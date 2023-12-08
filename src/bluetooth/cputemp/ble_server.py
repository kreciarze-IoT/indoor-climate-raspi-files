import dbus
import dbus.service

try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject

from .system_tools import BleTools
from .constants import DBUS_OM_IFACE, BLUEZ_SERVICE_NAME, GATT_MANAGER_IFACE

class ble_server(dbus.service.Object):
    def __init__(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.mainloop = GObject.MainLoop()
        self.bus = BleTools.get_bus()
        self.path = "/"
        self.services = []
        self.next_index = 0
        self.advertisement = None
        dbus.service.Object.__init__(self, self.bus, self.path)

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_service(self, service):
        self.services.append(service)

    def add_advertisement(self, advertisement):
        self.advertisement = advertisement

    @dbus.service.method(DBUS_OM_IFACE, out_signature="a{oa{sa{sv}}}")
    def GetManagedObjects(self):
        response = {}

        for service in self.services:
            response[service.get_path()] = service.get_properties()
            chrcs = service.get_characteristics()
            for chrc in chrcs:
                response[chrc.get_path()] = chrc.get_properties()
                descs = chrc.get_descriptors()
                for desc in descs:
                    response[desc.get_path()] = desc.get_properties()

        return response

    def register_app_callback(self):
        print("GATT application registered")

    def register_app_error_callback(self, error):
        print("Failed to register application: " + str(error))

    def register(self):
        if self.advertisement is None:
            raise RuntimeError("No advertisement added")

        adapter = BleTools.find_adapter(self.bus)

        service_manager = dbus.Interface(
            self.bus.get_object(BLUEZ_SERVICE_NAME, adapter),
            GATT_MANAGER_IFACE)

        service_manager.RegisterApplication(self.get_path(), {},
                                            reply_handler=self.register_app_callback,
                                            error_handler=self.register_app_error_callback)

        self.advertisement.register()


    def run(self):
        self.mainloop.run()

    def quit(self):
        print("\nGATT application terminated")
        self.mainloop.quit()
