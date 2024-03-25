from kamera import *
from motor_encoder import *
from distance import *
import threading



def setup():
    encoder_setup()
    motor_setup()
    distance_setup()
    
distance_turn=5        

def moveto_wall():
    motor_forward([0,1,2,3])
    distances = distance_get()
    while distances[2] > distance_turn and distances[3] > distance_turn:
        distances = distance_get()
    motor_turn(90)

#todo wenn schief ausgleichen
def stay_wall():
    motor_forward([0,1,2,3])
    distances = distance_get()
    while True:
        right_new= distances[1] - distance_turn
        if right_new > 0:
            motor_turn(-90)
        if distances[2] < distance_turn or distances[3] < distance_turn:
            motor_turn(90)
        
    
    
def search():
    motor_turn(360)
    moveto_wall()
    stay_wall()

def driveAroundBox():
    distances = distance_get()
    while True:
        right_new= distances[1] - distance_turn
        if right_new > 0:
            motor_turn(-90)
        if distances[2] < distance_turn or distances[3] < distance_turn:
            motor_turn(360)
            #todo: add that the it should turn around and find the other sides of the und lehrer fragen ob möglich an der wand

def box():
    #erster richtig drehen funktion machen
    moveto_wall()
    driveAroundBox()
    
    
    

def main():
    event = threading.Event()
    setup()
    background_thread = threading.Thread(target=camera_start)
    background_thread.start()
    


if __name__ == "__main__":
    main()