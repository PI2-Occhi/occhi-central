from paho.mqtt import client as mqtt_client
import random
import json


class MQTTClient:
    """
    Client to send MQTT messages to movement topic
    and to subscribe to sensors topic and foward messages to BLE
    """

    def __init__(self, broker, port, sensors_topic, movement_topic, send_ble_message):
        self.client_id = f"central_server_{random.randint(0, 100)}"
        self.broker = broker
        self.port = port
        self.sensors_topic = sensors_topic
        self.movement_topic = movement_topic
        self.send_ble_message = send_ble_message

    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc != 0:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(self.client_id)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def publish(self, client, message):
        result = client.publish(self.movement_topic, message)
        status = result[0]
        if status == 0:
            print(f"Comando `{message}` enviado ao MQTT`")
        else:
            print(f"Falha ao enviar comando: {message}")

    def subscribe(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            if "sensors" in msg.topic:
                print(
                    "Repassando estado do sensor: {}".format(str(msg.payload.decode()))
                )

                if "power" in msg.topic:
                    self.send_ble_message("power", msg)
                elif "overturn" in msg.topic:
                    self.send_ble_message("overturn", msg)
                elif "chair" in msg.topic:
                    self.send_ble_message("chair", msg)
                elif "colision" in msg.topic:
                    self.send_ble_message("colision", msg)

        client.subscribe(self, sensors_topic)
        client.on_message = on_message

    def run_mqtt(self):
        client = connect_mqtt()
        subscribe(client)
        client.loop_forever()
