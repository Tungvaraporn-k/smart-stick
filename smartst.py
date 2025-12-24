# Libraries
from sonic import HCSR04
from MPU6050 import MPU6050
from machine import Pin
from time import sleep
import time
import network
import urequests

# Initialize Ultrasensor
sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)
threadhold_ultrasonic = 30

# Initialize Gyro (MPU6050)
mpu = MPU6050()
threadhold_gyro_acc = 7
threadhold_gyro_axis = 60

# Initialize Buzzer
buzzer = Pin(2, Pin.OUT)

# Return distance in cm
def read_ultrasonic():
    distance = sensor.distance_cm()
    return distance;

# Function to read gyro axis
def read_axis():
    readgyro = mpu.read_gyro_data()
    read_x = readgyro["x"]
    read_y = readgyro["y"]
    read_z = readgyro["z"]
    return abs(read_x), abs(read_y), abs(read_z)

# Function to read gyro acc
def read_acc():
    readacc = mpu.read_accel_data()
    readacc_x = readacc["x"]
    readacc_y = readacc["y"]
    readacc_z = readacc["z"]
    return abs(readacc_x), abs(readacc_y), abs(readacc_z)

# Connect Wifi
def connect_wifi():
    count = 0
    ssid = '𝑡𝑡𝑎𝑛𝑦𝑜𝑛𝑔'  # Username
    password = 'yong1647'  # Password
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    while not wlan.isconnected():
        print('Connecting to WiFi...')
        time.sleep(1)
        count += 1
        if count >= 10:
            ssid = 'kanokrat_2.4G'  # Username
            password = 'venus128'  # Password
            wlan2 = network.WLAN(network.STA_IF)
            wlan2.active(True)
            wlan2.connect(ssid, password)
    
    print('Connected to WiFi:', wlan2.ifconfig())

# send the message to telegram
def send_telegram_message(message):
    telegram_token = '7867454562:AAGsANwbqGn_jywSj19lPd0_IJKaJZKYjBQ' # Telegram Token
    chat_id = '8182215707'
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        response = urequests.post(url, json=data)
        print("Message sent:", response.text)
        response.close()
        sleep(5)
    except Exception as e:
        print("Failed to send message:", e)
     
# Buzzer sound on
def buzz():
    buzzer.on()
    sleep(1)
    buzzer.off()
        
if __name__ == "__main__":
    # Connect to Wi-Fi
    try:
        connect_wifi()
    except Exception as e:
        print("WiFi connection failed:", e)

    # Main loop
    while True:
        distance = read_ultrasonic()
        x_axis, y_axis, z_axis = read_axis()
        x_acc, y_acc, z_acc = read_acc()

        # Ultrasonic condition
        if distance <= threadhold_ultrasonic:
            buzz()

        # Gyro and acceleration conditions
        if (
            (x_axis > threadhold_gyro_axis or y_axis > threadhold_gyro_axis or z_axis > threadhold_gyro_axis) and
            (x_acc > threadhold_gyro_acc or y_acc > threadhold_gyro_acc or z_acc > threadhold_gyro_acc)
        ):
            send_telegram_message("Bro help I fallen!!")
            buzz()
