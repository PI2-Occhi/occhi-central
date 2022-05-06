from paho.mqtt import client as mqtt_client
import random
import json


class MQTTClient:
    """
    Client to send MQTT messages to movement topic
    and to subscribe to sensors topic and foward messages to BLE
    """

    def __init__(self, broker, port, sensors_topic, movement_topic, sensors_data):
        self.client_id = f"central_server_{random.randint(0, 100)}"
        self.broker = broker
        self.port = port
        self.sensors_topic = sensors_topic
        self.movement_topic = movement_topic
        self.sensors_data = sensors_data
        self.client = None

    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc != 0:
                print("Failed to connect, return code %d\n", rc)

        self.client = mqtt_client.Client(self.client_id)
        self.client.on_connect = on_connect
        self.client.connect(self.broker, self.port)

    def publish(self, message):
        result = self.client.publish(self.movement_topic, message)
        status = result[0]
        if status == 0:
            print(f"Comando `{message}` enviado ao MQTT`")
        else:
            print(f"Falha ao enviar comando: {message}")

    def subscribe(self):
        def on_message(self, userdata, msg):
            if "sensors" in msg.topic:
                print(
                    "Repassando estado do sensor: {}".format(str(msg.payload.decode()))
                )
                sensor = msg.topic.split('/')[-1]
                self.sensors_data.append({sensor, msg})

        self.client.subscribe(self.sensors_topic)
        self.client.on_message = on_message

    def run_mqtt(self):
        self.connect_mqtt()
        self.subscribe()
        self.client.loop_forever()
