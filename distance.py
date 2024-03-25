import RPi.GPIO as GPIO
import time

from values import trigger_pin
from values import sensor_pins


# Setup GPIO
def distance_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trigger_pin, GPIO.OUT)
    for echo_pin in sensor_pins:
        GPIO.setup(echo_pin, GPIO.IN)



def distance_get():
    sensor_indices=[0,1,2,3,4]
    distances = []
    for index in sensor_indices:
        echo_pin = sensor_pins[index]

        # Senden eines 10us langen Pulses zum Trigger-Pin
        GPIO.output(trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(trigger_pin, False)

        start_time = time.time()
        stop_time = time.time()

        # Warte bis der Echo-Pin hoch wird
        while GPIO.input(echo_pin) == 0:
            start_time = time.time()

        # Warte bis der Echo-Pin wieder niedrig wird
        while GPIO.input(echo_pin) == 1:
            stop_time = time.time()

        # Berechne die Zeit, die der Schall für die Hin- und Rückreise benötigt
        elapsed_time = stop_time - start_time

        # Berechne die Entfernung (in Zentimetern) unter Verwendung der Schallgeschwindigkeit (34300 cm/s)
        distance = (elapsed_time * 34300) / 2
        distances.append(distance)

    return distances

try:
    while True:
        sensor_indices = [0,1,2,3,4]  # Liste von Zahlen von 0 bis 4
        distances = distance_get(sensor_indices)
        for i, distance in enumerate(distances):
            print(f"Sensor {i+1}: {distance:.2f} cm")
        time.sleep(1)  # Warte 1 Sekunde zwischen den Messungen

except KeyboardInterrupt:
    GPIO.cleanup()
