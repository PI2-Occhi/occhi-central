import random
import time
from paho.mqtt import client as mqtt_client
import json

broker = '192.168.0.70'
port = 1883
subscribe_topic1 = "/sensors/#"
subscribe_topic2 = "/movement/app"
publishing_topic = "/movement/instructions"
client_id = f'central_server_{random.randint(0, 100)}'


def connect_mqtt() -> mqtt_client:
  def on_connect(client, userdata, flags, rc):
    if rc != 0:
      print("Failed to connect, return code %d\n", rc)

  client = mqtt_client.Client(client_id)
  client.on_connect = on_connect
  client.connect(broker, port)
  return client

def publish(client, message):
  result = client.publish(publishing_topic, message)
  status = result[0]
  if status == 0:
    print(f"Comando `{message}` enviado ao MQTT`")
  else:
    print(f"Failed to command: {message}")

def subscribe(client: mqtt_client):
  def on_message(client, userdata, msg):
    if('sensors' in msg.topic):
      print("Repassando estado do sensor: {}".format(str(msg.payload.decode())))
    if('/movement/app' == msg.topic):
      command = str(msg.payload.decode())
      if command == "FW":
        print("Recebido comando, para frente.")
        command = json.dumps({
            'forward': True,
            'backward': False,
            'left': False,
            'right': False,
            'stop': False,
            'turn': False,
        })
      if command == "BW":
        print("Recebido comando, para trás.")
        command = json.dumps({
            'forward': False,
            'backward': True,
            'left': False,
            'right': False,
            'stop': False,
            'turn': False,
        })     
      if command == "RT":
        print("Recebido comando, para direita.")
        command = json.dumps({
            'forward': False,
            'backward': False,
            'left': False,
            'right': True,
            'stop': False,
            'turn': False,
        })
      if command == "LT":
        print("Recebido comando, para esquerda.")
        command = json.dumps({
            'forward': False,
            'backward': False,
            'left': True,
            'right': False,
            'stop': False,
            'turn': False,
        })
      if command == "ST":
        print("Recebido comando, parar.")
        command = json.dumps({
            'forward': False,
            'backward': False,
            'left': False,
            'right': False,
            'stop': True,
            'turn': False,
        })
      if command == "TR":
        print("Recebido comando, virar 180 graus.")
        command = json.dumps({
            'forward': False,
            'backward': False,
            'left': False,
            'right': False,
            'stop': False,
            'turn': True,
        })
      publish(client, command)

  client.subscribe(subscribe_topic1)
  client.subscribe(subscribe_topic2)
  client.on_message = on_message

def run_mqtt():
  client = connect_mqtt()
  subscribe(client)
  client.loop_forever()