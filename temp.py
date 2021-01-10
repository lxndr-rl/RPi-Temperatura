import RPi.GPIO as GPIO
import dht11
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

while True:
    instance = dht11.DHT11(pin = 14)
    result = instance.read()
    if result.is_valid():
        
        print("Temperatura: %-3.1f C" % result.temperature)
        print("Humedad: %-3.1f %%" % result.humidity)
    else:
        print(f"Error: {result}")
    time.sleep(2)
