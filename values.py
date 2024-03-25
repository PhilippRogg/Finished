import numpy as np

trigger_pin = 8  # Trigger-Pin für alle Sensoren

sensor_pins = [
    7,   # Echo-Pin für Sensor 1: GPIO7
    12,  # Echo-Pin für Sensor 2: GPIO12
    27,  # Echo-Pin für Sensor 3: GPIO27
    22,  # Echo-Pin für Sensor 4: GPIO22
    10   # Echo-Pin für Sensor 5: GPIO10
]
encoder_pins = [14, 15, 9, 11]

motor_pins = {
    0: {
        "input1_pin": 18,
        "input2_pin": 23
    },
    1: {
        "input1_pin": 2,
        "input2_pin": 3
    },
    2: {
        "input1_pin": 24,
        "input2_pin": 25
    },
    3: {
        "input1_pin": 4,
        "input2_pin": 17
    }
}



color_bounds = {
    'blue': {'lower': np.array([100, 50, 50]), 'upper': np.array([130, 255, 255])},
    'red': {'lower': np.array([0, 100, 100]), 'upper': np.array([10, 255, 255])},
    'green': {'lower': np.array([40, 50, 50]), 'upper': np.array([80, 255, 255])},
    'yellow': {'lower': np.array([20, 100, 100]), 'upper': np.array([30, 255, 255])},
    'orange': {'lower': np.array([5, 100, 100]), 'upper': np.array([15, 255, 255])},
    'black': {'lower': np.array([0, 0, 0]), 'upper': np.array([180, 255, 30])},
    'white': {'lower': np.array([0, 0, 200]), 'upper': np.array([180, 30, 255])}
}
