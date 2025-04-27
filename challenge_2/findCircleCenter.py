import cv2
import numpy as np


def detect_ball_position(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=50,
        param1=50,
        param2=30,
        minRadius=20,
        maxRadius=100
    )
    
    if circles is not None:
        circle = circles[0][0]
        x, y = int(circle[0]), int(circle[1])
        return (x, y)
    return None