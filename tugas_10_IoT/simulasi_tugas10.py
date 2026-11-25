import random
import time
import paho.mqtt.client as mqtt

# Ganti jika NIM berbeda
NIM = "2410010128"
BROKER = "localhost"
PORT = 1883

TOPIC_SUHU = f"iot/{NIM}/sensor/suhu"
TOPIC_RELAY = f"iot/{NIM}/aktuator/relay"
TOPIC_PWM = f"iot/{NIM}/aktuator/pwm"

# Status simulasi pin GPIO ESP32
gpio_26_relay = "OFF"
gpio_2_pwm = 0

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[MQTT] Terhubung ke broker {BROKER}:{PORT}")
        client.subscribe([(TOPIC_RELAY, 0), (TOPIC_PWM, 0)])
        print(f"[MQTT] Subscribe: {TOPIC_RELAY} & {TOPIC_PWM}")
    else:
        print(f"[MQTT] Gagal terhubung, kode: {rc}")

def on_message(client, userdata, msg):
    global gpio_26_relay, gpio_2_pwm
    payload = msg.payload.decode("utf-8").strip()

    if msg.topic == TOPIC_RELAY:
        if payload.upper() in ["ON", "OFF"]:
            gpio_26_relay = payload.upper()
            print(f"\n>>> [GPIO 26 - RELAY] Status diubah menjadi: {gpio_26_relay}\n")
    elif msg.topic == TOPIC_PWM:
        try:
            nilai = int(float(payload))
            if 0 <= nilai <= 255:
                gpio_2_pwm = nilai
                persen = round((nilai / 255) * 100)
                print(f"\n>>> [GPIO 2 - LED PWM] Nilai: {gpio_2_pwm}/255 (Kecerahan: {persen}%)\n")
        except ValueError:
            print(f"\n>>> [GPIO 2 - LED PWM] Nilai tidak valid: {payload}\n")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    while True:
        suhu = round(random.uniform(24.0, 36.0), 1)
        client.publish(TOPIC_SUHU, str(suhu))
        print(f"[DHT22 -> {TOPIC_SUHU}] Suhu: {suhu} °C | Relay(GPIO26): {gpio_26_relay} | LED(GPIO2): {gpio_2_pwm}")
        time.sleep(3)
except KeyboardInterrupt:
    print("\nSimulator dihentikan.")
    client.loop_stop()
    client.disconnect()