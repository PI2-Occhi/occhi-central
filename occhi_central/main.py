from config import Configuration
from mqtt import MQTTClient
from threading import Thread
from gatt_profile import run_ble


def main():

    config = Configuration.load_json("../config.json")
    mqtt_client = MQTTClient(
        config.mqtt.broker,
        config.mqtt.port,
        config.mqtt.sensors_topic,
        config.mqtt.movement_topic,
        send_ble_message,
    )

    print("Iniciando MQTT ...")
    mqtt_subscriber = Thread(target=mqtt_client.run_mqtt())
    mqtt_subscriber.start()

    print("Iniciando BLE ...")
    ble_communication = Thread(target=run_ble, args=(mqtt_client.publish))
    ble_communication.start()

    mqtt_subscriber.join()
    ble_communication.join()


if __name__ == "__main__":
    main()
