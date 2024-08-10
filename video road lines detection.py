import cv2
import numpy as np
import pyttsx3
import time
import random

# Initialize text-to-speech engine
engine = pyttsx3.init()

def provide_audio_feedback(message):
    engine.say(message)
    engine.runAndWait()

# Video capture
video = cv2.VideoCapture("road_car_view.mp4")

# Initialize variables
last_feedback_time = 0
feedback_interval = random.randint(2, 3)  # Random interval between 2 and 3 seconds

while True:
    ret, orig_frame = video.read()
    if not ret:
        video = cv2.VideoCapture("road_car_view.mp4")
        continue

    frame = cv2.GaussianBlur(orig_frame, (5, 5), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    low_yellow = np.array([18, 94, 140])
    up_yellow = np.array([48, 255, 255])
    mask = cv2.inRange(hsv, low_yellow, up_yellow)
    edges = cv2.Canny(mask, 75, 150)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=50)
    feedback_text = "Good, go ahead"
    audio_feedback_needed = False
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
            
            # Sample logic for generating feedback based on detected lines
            if x1 < 100 and x2 < 100:
                feedback_text = "Vehicle drifting left"
                audio_feedback_needed = True
            elif x1 > 500 and x2 > 500:
                feedback_text = "Vehicle drifting right"
                audio_feedback_needed = True
            else:
                feedback_text = "Good, go ahead"

    # Display textual feedback on the video frame
    cv2.putText(frame, feedback_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    # Provide audio feedback at random intervals
    current_time = time.time()
    if audio_feedback_needed and (current_time - last_feedback_time > feedback_interval):
        provide_audio_feedback(feedback_text)
        last_feedback_time = current_time
        feedback_interval = random.randint(2, 3)  # Reset random interval

    cv2.imshow("frame", frame)
    cv2.imshow("edges", edges)

    key = cv2.waitKey(1)
    if key == 27:  # ESC key to exit
        break

video.release()
cv2.destroyAllWindows()
