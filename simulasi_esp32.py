import json
import random
import time
from datetime import datetime
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC_SENSOR = "iot/sensor"
TOPIC_KONTROL = "iot/kontrol"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[MQTT] Terhubung ke broker {BROKER}:{PORT}")
        client.subscribe(TOPIC_KONTROL)
        print(f"[MQTT] Mendengarkan perintah di topik: {TOPIC_KONTROL}")
    else:
        print(f"[MQTT] Gagal terhubung, kode: {rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    print(f"\n>>> [PERINTAH DITERIMA] Topik: {msg.topic} | Isi: {payload}\n")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_start()  # Wajib agar bisa menerima pesan saat loop publish berjalan

try:
    while True:
        data = {
            "suhu": round(random.uniform(25.0, 34.0), 1),
            "kelembaban": round(random.uniform(55.0, 80.0), 1),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        client.publish(TOPIC_SENSOR, json.dumps(data))
        print(f"[KIRIM] {data}")
        time.sleep(3)
except KeyboardInterrupt:
    print("\nSimulator dihentikan.")
    client.loop_stop()
    client.disconnect()