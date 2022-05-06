#!/usr/bin/python3

import dbus
from advertisement import Advertisement
from ble_service import Application, Service, Characteristic, Descriptor

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 5000

class OcchiAdvertisement(Advertisement):
    def __init__(self, index):
        Advertisement.__init__(self, index, "peripheral")
        self.add_local_name("Cadeira Occhi")
        self.include_tx_power = True

class ControlService(Service):
    CONTROL_SVC_UUID = "4079e396-1c21-46fc-bd36-dc1886766b29"

    def __init__(self, index):
        Service.__init__(self, index, self.CONTROL_SVC_UUID, True)
        self.add_characteristic(CommandCharacteristic(self))

class CommandCharacteristic(Characteristic):
    COMMAND_CHARACTERISTIC_UUID = "ef00490b-5c12-44be-bc6b-546850faaa0a"

    def __init__(self, service):
        Characteristic.__init__(
                self, self.COMMAND_CHARACTERISTIC_UUID,
                ["write"], service)

    def WriteValue(self, value, options):
        val = str(value).upper()
        # send

class SensorsService(Service):
    SENSORS_SVC_UUID = "36752d4f-07d2-4b8c-b533-6dbc8f5cae92"

    def __init__(self, index):
        Service.__init__(self, index, self.SENSORS_SVC_UUID, True)
        self.add_characteristic(PowerCharacteristic(self))

class PowerCharacteristic(Characteristic):
    POWER_CHARACTERISTIC_UUID = "ac9c9ebf-3b91-4b4b-8c91-355d4d712eab"

    def __init__(self, service):
        self.notifying = True

        Characteristic.__init__(
                self, self.POWER_CHARACTERISTIC_UUID,
                ["notify", "read"], service)

    def get_power(self):
        strtemp = str("KAT")
        for c in strtemp:
            value.append(dbus.Byte(c.encode()))

        return value

    def set_temperature_callback(self):
        if self.notifying:
            value = self.get_power()
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        value = self.get_power()
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.set_temperature_callback)

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        value = self.get_power()

        return value


def run():
    app = Application()
    app.add_service(ControlService(0))
    app.add_service(SensorsService(1))
    app.register()

    adv = OcchiAdvertisement(0)
    adv.register()

    try:
        app.run()
    except KeyboardInterrupt:
        app.quit()

run()