import random
import time
import sys
from paho.mqtt import client as mqtt_client


broker = 'mqtteste.cloud.shiftr.io'
port = 1883
topic = "MENSAGEM"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'mqtteste'
password = 'testes'
flag = 0
msg_flag=0

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Conectado ao MQTT Broker!")
        else:
            print("Falha na conexão, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Recebido `{msg.payload.decode()}` de `{msg.topic}` topic")
        msg_flag=msg.payload.decode()
        print(msg_flag)
    global msg_flag
    client.subscribe(topic)
    client.on_message = on_message
    if msg_flag == '-1':
        client.disconect()

def publish(client):
    while True:
        time.sleep(1)
        msg = str (input("Digite a mensagem a ser enviada(-1 para sair) "))
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        if msg == '-1':
            break

def run():
    client = connect_mqtt()
    global msg_flag
    flag = int (input("Digite 0 para subs ou 1 para pub: "))
    if flag == 0: 
        subscribe(client)
        client.loop_forever()
        if msg_flag == '-1':
            client.loop_stop()
    elif flag == 1:
        publish(client)
        client.loop_start()
    else:
        print ("Comando inválido")
    


if __name__ == '__main__':
    run()
