#!/usr/bin/python3

import dbus
from ble_services.advertisement import Advertisement
from ble_services.ble_service import Application, Service, Characteristic, Descriptor
from translator import translate_message

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 5000


class OcchiAdvertisement(Advertisement):
    """
    Class for Occhi GATT profile
    """

    def __init__(self, index, send_mqtt_message, sensors_data):
        Advertisement.__init__(self, index, "peripheral")
        self.add_local_name("Cadeira Occhi")
        self.include_tx_power = True
        self.send_mqtt_message = send_mqtt_message
        self.sensors_data = sensors_data


class ControlService(Service):
    """
    Dedicated to receive movement control commands from BLE
    """

    CONTROL_SVC_UUID = "4079e396-1c21-46fc-bd36-dc1886766b29"

    def __init__(self, index):
        Service.__init__(self, index, self.CONTROL_SVC_UUID, True)
        self.add_characteristic(CommandCharacteristic(self))


class CommandCharacteristic(Characteristic):
    """
    Receives the command, translates it, and sends to MQTTClient
    """

    COMMAND_CHARACTERISTIC_UUID = "ef00490b-5c12-44be-bc6b-546850faaa0a"

    def __init__(self, service):
        Characteristic.__init__(
            self, self.COMMAND_CHARACTERISTIC_UUID, ["write"], service
        )

    def WriteValue(self, value, options):
        command = str(value).upper()
        translated_command = translate_message(command)
        self.send_mqtt_message(translated_command)


class SensorsService(Service):
    """
    Service that updates the BLE receiver with new sensors data
    """

    SENSORS_SVC_UUID = "36752d4f-07d2-4b8c-b533-6dbc8f5cae92"

    def __init__(self, index):
        Service.__init__(self, index, self.SENSORS_SVC_UUID, True)
        self.add_characteristic(PowerCharacteristic(self))
        self.add_characteristic(ColisionCharacteristic(self))
        self.add_characteristic(OverturnCharacteristic(self))
        self.add_characteristic(ChairCharacteristic(self))


class PowerCharacteristic(Characteristic):
    """
    Power remaining on the chair
    """

    POWER_CHARACTERISTIC_UUID = "ac9c9ebf-3b91-4b4b-8c91-355d4d712eab"

    def __init__(self, service):
        self.notifying = True

        Characteristic.__init__(
            self, self.POWER_CHARACTERISTIC_UUID, ["notify", "read"], service
        )

    def get_power(self):
        value = []
        for sensor, value in self.sensors_data:
            if sensor == "power":
                sensor_value = value

        for c in sensor_value:
            value.append(dbus.Byte(c.encode()))

        return value

    def get_power_callback(self):
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
        self.add_timeout(NOTIFY_TIMEOUT, self.get_power_callback)

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        value = self.get_power()

        return value


class ColisionCharacteristic(Characteristic):
    """
    Risk of colision in one of the directions
    """

    COLISION_CHARACTERISTIC_UUID = "7d9c1b66-5e0c-4470-98fe-e9b4e4cdace5"

    def __init__(self, service):
        self.notifying = True

        Characteristic.__init__(
            self, self.COLISION_CHARACTERISTIC_UUID, ["notify", "read"], service
        )

    def get_colision(self):
        value = []
        for sensor, value in self.sensors_data:
            if sensor == "colision":
                sensor_value = value

        for c in sensor_value:
            value.append(dbus.Byte(c.encode()))

        return value

    def get_colision_callback(self):
        if self.notifying:
            value = self.get_colision()
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        value = self.get_colision()
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.get_colision_callback)

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        value = self.get_colision()

        return value


class OverturnCharacteristic(Characteristic):
    """
    Indicates if there was a overturn
    """

    OVERTURN_CHARACTERISTIC_UUID = "2bddc853-a011-438c-b26c-ae39a8d54e6e"

    def __init__(self, service):
        self.notifying = True

        Characteristic.__init__(
            self, self.OVERTURN_CHARACTERISTIC_UUID, ["notify", "read"], service
        )

    def get_overturn(self):
        value = []
        for sensor, value in self.sensors_data:
            if sensor == "overturn":
                sensor_value = value

        for c in sensor_value:
            value.append(dbus.Byte(c.encode()))

        return value

    def get_overturn_callback(self):
        if self.notifying:
            value = self.get_overturn()
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        value = self.get_overturn()
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.get_overturn_callback)

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        value = self.get_overturn()

        return value


class ChairCharacteristic(Characteristic):
    """
    Indicates if the user is seated on the chair
    """

    CHAIR_CHARACTERISTIC_UUID = "2c5e098a-d69b-44e2-b721-af9a405d9063"

    def __init__(self, service):
        self.notifying = True

        Characteristic.__init__(
            self, self.CHAIR_CHARACTERISTIC_UUID, ["notify", "read"], service
        )

    def get_chair(self):
        value = []
        for sensor, value in self.sensors_data:
            if sensor == "chair":
                sensor_value = value

        for c in sensor_value:
            value.append(dbus.Byte(c.encode()))

        return value

    def get_chair_callback(self):
        if self.notifying:
            value = self.get_chair()
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        value = self.get_chair()
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.get_chair_callback)

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        value = self.get_chair()

        return value


def run_ble(send_mqtt_message, sensors_data):
    app = Application()
    app.add_service(ControlService(0))
    app.add_service(SensorsService(1))
    app.register()

    adv = OcchiAdvertisement(0, send_mqtt_message, sensors_data)
    adv.register()

    try:
        app.run()
    except KeyboardInterrupt:
        app.quit()
