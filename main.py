import cv2
import numpy as np
import mediapipe as mp
from pygame import mixer
from ultralytics import YOLO
import time

# ========== Settings ==========
DRIVER_NAME = "vishwas rallapalli"  # 🔁 Change driver name here
ALERT_SOUND = "alert.wav"  # 🔁 Sound file
PHONE_CLASS_ID = 67        # COCO phone class
EYE_AR_THRESH = 0.25
EYE_AR_CONSEC_FRAMES = 15
HEAD_DOWN_THRESHOLD = 0.6  # Proportion of frame height for head down
# ==============================

# Initialize
mixer.init()
mixer.music.load(ALERT_SOUND)

# Initialize YOLOv8 model
model = YOLO('yolov8n.pt')  # Replace with better trained model if needed

# Mediapipe face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)

# Video Capture
cap = cv2.VideoCapture(0)

# Eye indices
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]
NOSE = 1  # Tip of the nose

# Sleep detection counter
sleep_counter = 0

def eye_aspect_ratio(landmarks, left_ids, right_ids):
    def get_eye(eye_ids):
        points = [landmarks[i] for i in eye_ids]
        eye = np.array([(p.x, p.y) for p in points])
        A = np.linalg.norm(eye[1] - eye[5])
        B = np.linalg.norm(eye[2] - eye[4])
        C = np.linalg.norm(eye[0] - eye[3])
        return (A + B) / (2.0 * C)

    left_ear = get_eye(left_ids)
    right_ear = get_eye(right_ids)
    return (left_ear + right_ear) / 2.0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    sleepy = False
    head_down = False
    phone_detected = False

    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0].landmark

        # Eye aspect ratio
        ear = eye_aspect_ratio(face_landmarks, LEFT_EYE, RIGHT_EYE)
        if ear < EYE_AR_THRESH:
            sleep_counter += 1
        else:
            sleep_counter = 0

        if sleep_counter >= EYE_AR_CONSEC_FRAMES:
            sleepy = True

        # Head down detection
        nose_y = face_landmarks[NOSE].y * h
        if nose_y > h * HEAD_DOWN_THRESHOLD:
            head_down = True

    # Phone detection using YOLO
    results_yolo = model(frame, imgsz=320, verbose=False)[0]
    for det in results_yolo.boxes:
        cls = int(det.cls[0])
        conf = det.conf[0]
        if cls == PHONE_CLASS_ID and conf > 0.5:
            phone_detected = True
            break

    # Set status
    status = "Normal"
    color = (0, 255, 0)

    if sleepy or head_down or phone_detected:
        status = "ALERT! Drowsy/Phone"
        color = (0, 0, 255)
        if not mixer.music.get_busy():
            mixer.music.play(-1)  # 🔁 Loop sound
    else:
        if mixer.music.get_busy():
            mixer.music.stop()

    # Display info
    cv2.putText(frame, f"Driver: {DRIVER_NAME}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
    cv2.putText(frame, f"Status: {status}", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

    cv2.imshow("Driver Monitoring System", frame)

    if cv2.waitKey(1) == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
