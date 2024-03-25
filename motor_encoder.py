import RPi.GPIO as GPIO
import time
import math
from values import encoder_pins
from values import motor_pins
# GPIO-Pins für die Encoder


# Radumfang in Metern
wheel_circumference = 22  # Anpassen für deine tatsächlichen Reifen

# Drehzähler für die Reifen
wheel_rotations = [0, 0, 0, 0]

# Zurückgelegte Strecken der Reifen
wheel_distances = [0.0, 0.0, 0.0, 0.0]

# 1:Vorwärts, 2:Rückwärts
wheel_directions=[1,1,1,1];


# Callback-Funktion für den Encoder-Interrupt

def encoder_callback(channel):
    wheel_index = encoder_pins.index(channel)
    wheel_rotations[wheel_index] += 0.05 * wheel_directions
    wheel_distances[wheel_index] = wheel_rotations[wheel_index] * wheel_circumference

def encoder_setup():
    for pin in encoder_pins:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin, GPIO.RISING, callback=encoder_callback)

# GPIO-Modus einstellen und Motoren konfigurieren
def motor_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)  # Warnungen für GPIO deaktivieren
    for motor, pins in motor_pins.items():
        GPIO.setup(pins["input1_pin"], GPIO.OUT)
        GPIO.setup(pins["input2_pin"], GPIO.OUT)
        # Setze alle Pins zu Beginn auf "low", um sicherzustellen, dass die Motoren nicht unerwartet starten
        GPIO.output(pins["input1_pin"], GPIO.LOW)
        GPIO.output(pins["input2_pin"], GPIO.LOW)
        

# Funktionen zum Steuern der Motoren definieren
def motor_forward(motors):
    for motor in motors:
        wheel_directions[motor]=1;
        pins = motor_pins[motor]
        GPIO.output(pins["input1_pin"], GPIO.HIGH)
        GPIO.output(pins["input2_pin"], GPIO.LOW)

def motor_backward(motors):
    for motor in motors:
        wheel_directions[motor]=-1;
        pins = motor_pins[motor]
        GPIO.output(pins["input1_pin"], GPIO.LOW)
        GPIO.output(pins["input2_pin"], GPIO.HIGH)

def motor_stop(motors):
    for motor in motors:
        pins= motor_pins[motor]
        GPIO.output(pins["input1_pin"], GPIO.LOW)
        GPIO.output(pins["input2_pin"], GPIO.LOW)


#negativ: rechtsdrehung;  positiv: linksdrehung
def motor_turn(degree):
    temp= wheel_distances
    if(degree > 0):
        motor_forward([1,3])
        motor_backward([0,2])
    elif(degree < 0):
        motor_forward([0,2])
        motor_backward([1,3])
    
    l= 2#noch einstellen distanz zwischen räder
    while True:
        d_rechts = ((temp[0]-wheel_distances[0]) +(temp[2]-wheel_distances[2]))/2
        d_links = ((temp[1]-wheel_distances[1]) +(temp[3]-wheel_distances[3]))/2
        if(math.abs(degree+(360 * (d_rechts - d_links)) / (2 * math.pi * l))>=360):
            break
    motor_forward([0,1,2,3])
     


try:
    while True:
        # Ausgabe der zurückgelegten Strecken
        print("Strecken in Metern:")
        for i, distance in enumerate(wheel_distances):
            print(f"Reifen {i + 1}: {distance:.2f} m")
        time.sleep(1)  # Wartezeit von 1 Sekunde

except KeyboardInterrupt:
    pass






GPIO.cleanup()