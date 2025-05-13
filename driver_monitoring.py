import cv2
import mediapipe as mp
import time
import math
import threading
from pygame import mixer
import datetime
import os

# Initialize mixer for alert sound
mixer.init()
mixer.music.load("alert.wav")  # make sure alert.wav is in the same folder

# Create a logs folder
if not os.path.exists("logs"):
    os.mkdir("logs")

def log_event(event):
    with open(f"logs/log_{datetime.date.today()}.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - {event}\n")

def play_alert():
    mixer.music.play()

# MediaPipe setup
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2)

cap = cv2.VideoCapture(0)
blink_counter = 0
blink_start = None
yawn_counter = 0
prev_y = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(frame_rgb)
    hand_results = hands.process(frame_rgb)

    status_text = "Status: Active 🙂"
    phone_using = False
    yawning = False

    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            for lm in hand_landmarks.landmark:
                x, y = int(lm.x * w), int(lm.y * h)
                if w//3 < x < 2*w//3 and h//4 < y < h//2:
                    phone_using = True
                    break

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Yawning Detection: based on mouth landmarks (13 - upper lip, 14 - lower lip)
            upper_lip = face_landmarks.landmark[13]
            lower_lip = face_landmarks.landmark[14]
            lip_distance = abs(upper_lip.y - lower_lip.y)

            if lip_distance > 0.05:
                yawn_counter += 1
                if yawn_counter > 5:
                    status_text = "Status: Yawning 🤭"
                    log_event("Yawning detected")
                    threading.Thread(target=play_alert).start()
            else:
                yawn_counter = 0

            # Eye blink detection (159 - left, 145 - right)
            left_eye_top = face_landmarks.landmark[159]
            left_eye_bottom = face_landmarks.landmark[145]
            eye_distance = abs(left_eye_top.y - left_eye_bottom.y)

            if eye_distance < 0.01:
                if blink_start is None:
                    blink_start = time.time()
                elif time.time() - blink_start > 1.5:
                    status_text = "Status: Drowsy 💤"
                    log_event("Drowsiness detected")
                    threading.Thread(target=play_alert).start()
            else:
                blink_start = None

            # Head Pose Estimation (very basic using nose tip)
            nose_tip = face_landmarks.landmark[1]
            if nose_tip.x < 0.3:
                status_text = "Status: Looking Left 👈"
            elif nose_tip.x > 0.7:
                status_text = "Status: Looking Right 👉"

    if phone_using:
        status_text = "Status: Using Phone 📱"
        log_event("Phone usage detected")
        threading.Thread(target=play_alert).start()

    # Draw and show
    cv2.putText(frame, status_text, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("Driver Monitoring", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
