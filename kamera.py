import cv2
import imutils
import numpy as np
import logging
from picamera2 import Picamera2

from values import color_bounds

# Initialize logging to output to both the console and a file for better monitoring and debugging
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
# Create and configure a file handler to save log messages to a file
fh = logging.FileHandler('app.log', mode='w')
fh.setLevel(logging.INFO)
# Create and configure a console handler to print log messages
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# Define a formatter to structure log messages uniformly
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# Add the file and console handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


#todo: endbox finden
def camera_calculate_distance(radius_pixels):
    """
    Calculate the distance to the ball based on its radius in pixels.
    """
    # Focal length of the camera (you need to calibrate this)
    FOCAL_LENGTH_PIXELS = 1000  
    # Known diameter of the golf ball in centimeters
    BALL_DIAMETER_CM = 4.27  
    
    return (BALL_DIAMETER_CM * FOCAL_LENGTH_PIXELS) / (2 * radius_pixels)

def camera_find_contours(mask):
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    return cnts

def camera_process_frame(frame, color_bounds, chosen_color):
    """
    Apply Gaussian blur to the frame, convert it to the HSV color space, create a mask based on
    specified color bounds, and find contours within this mask.
    """
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, color_bounds[chosen_color]["lower"], color_bounds[chosen_color]["upper"])
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    return mask


def camera_get_position(cnts,min_contour_area):
    circles = []
    
    for c in cnts:
        if cv2.contourArea(c) > min_contour_area:
            (x, y), radius = cv2.minEnclosingCircle(c)
            circles.append((x, y, radius, camera_calculate_distance(radius)))
    return circles
            
            
            
#Not in use cause not needed for the project but can be used as visualization
def camera_draw_contours(frame, cnts, min_contour_area):
    """
    Iterate through each contour detected and draw it on the frame if it is above the minimum
    area threshold. Also, log the center coordinates of significant contours.
    """
    for c in cnts:
        area = cv2.contourArea(c)
        if area > min_contour_area:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 5)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                logger.info(f"Center coordinates: {center}")
                 
                distance_cm = camera_calculate_distance(radius)
                logger.info(f"Distance to the ball: {distance_cm} cm")
    return frame


def camera_start():
    """
    Main function to set up video capture, process and display video frames in a loop,
    and handle user input to quit. Processes frames to detect and annotate specified
    color objects and logs their information.
    """
    
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (640,480)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()
    chosen_color = 'orange'  # Change this based on the desired color to detect
    while True:
        frame = picam2.capture_array()
        frame2= frame
        if frame is None:
            break

        # Resize frame for faster processing and get dynamic contour area
        frame = cv2.resize(frame, (640, 480))

        # Process the frame and draw contours
        mask = camera_process_frame(frame, color_bounds, chosen_color)
        
        cnts = camera_find_contours(mask)
        
        camera_get_position(cnts, (frame.shape[1] * frame.shape[0]) / 1000);