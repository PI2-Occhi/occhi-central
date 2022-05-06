from config import Configuration
from mqtt import MQTTClient
from threading import Thread
from gatt_profile import run_ble


def main():
    # fetching configuration from config file
    config = Configuration.load_json("../config.json")
    sensors_data = []
    mqtt_client = MQTTClient(
        config.mqtt.broker_url,
        config.mqtt.port,
        config.mqtt.sensors_topic,
        config.mqtt.movement_topic,
        sensors_data,
    )

    # starting threads for MQTT consumer and BLE communicator

    print("Iniciando MQTT ...")
    mqtt_subscriber = Thread(target=mqtt_client.run_mqtt)
    mqtt_subscriber.start()

    print("Iniciando BLE ...")
    ble_communication = Thread(
        target=run_ble,
        args=(
            mqtt_client.publish,
            sensors_data,
        ),
    )
    ble_communication.start()

    mqtt_subscriber.join()
    ble_communication.join()


if __name__ == "__main__":
    main()
