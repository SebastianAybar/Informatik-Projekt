import sys
import tkinter as tk
import paho.mqtt.client as mqtt
import json


with open('Client/config.json', 'r') as file:
    data = json.load(file)

# Fill variables with the data given from the json
mqtt_start = data["mqtt_start"]
mqtt_status = data["mqtt_status"]
mqtt_error = data["mqtt_error"]
mqttBroker = data["mqttBroker"]
client_id = data["client_id"]


def onConnect(client, userdata, flags, rc, properties):
    # This will be called once the client connects
    # If printed every few seconds, there is another client with the same client_id. Change Name for client_id!
    print(f"Auslesetrigger verbunden result code {rc}")
    sys.stdout.flush()

    # Subscribe here!
    client.subscribe(mqtt_start)


def onMessage(client, userdata, msg):
    print("Hier")
    print(f"Message received [{msg.topic}]: {msg.payload}")
    print("Hier2")
    sys.stdout.flush()
    print("Hier3")
    payload = str(msg.payload)
    print("Hier4")
    # should be a string in the format  b'XX:XX:XX:XX:XX:XX'
    print(payload)
    status_var.set(payload)

    if str(payload[4]) != ':' or str(payload[7]) != ':' or str(payload[10]) != ':' or str(payload[13]) != ':' or str(payload[16]) != ':':
        print("Ungültige Geräte-ID!")
        sys.stdout.flush()
        client.publish(mqtt_status, "Ungültige Geräte-ID!", qos=1)
        client.loop()
        client.publish(mqtt_error, "1", qos=1)
        client.loop()
    else:
        id = str(payload[2:19])
        print(id)
        client.publish(mqtt_status, "Lese Gerät mit ID " + id, qos=1)
        # ensure packet is published, subprocess can take a while to answer
        # qos=1 means one handshake and this is only processed in loop()
        client.loop()


def start_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id)
    client.subscribe(mqtt_start)
    # client.on_connect = onConnect
    client.on_message = onMessage
    # client.username_pw_set("myusername", "mypassword")
    client.connect(mqttBroker, 1883, 60)
    client.loop_start()  # Start networking daemon


# Main program runs in an endless loop with 2 seconds repetition time of a connection attempt.
# Reason: If this script is started via systemd at system startup, the docker container with the mqtt broker may not be ready yet.
root = tk.Tk()
root.title("Receiver")
root.geometry("1000x600")
root.configure(bg="#99aab5")

status_var = tk.StringVar(value="Waiting")
label = tk.Label(root, textvariable=status_var)
label.pack(pady=20)

# start_mqtt()
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id)
# client.subscribe(mqtt_start)
client.on_connect = onConnect
client.on_message = onMessage
# client.username_pw_set("myusername", "mypassword")
client.connect(mqttBroker, 1883, 60)
client.loop_start()

root.mainloop()
