import os
from ultralytics import YOLO
import torch
from torch.serialization import add_safe_globals
from ultralytics.nn.tasks import DetectionModel

import cv2
import cvzone
import time
import csv
import pygame
import smtplib
from email.message import EmailMessage

# Allow PyTorch to safely unpickle DetectionModel (required for torch>=2.6)
add_safe_globals([DetectionModel])

# Load credentials from environment variables or fallback values
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "bhavirisrigowri@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "zjkv hiuo gmhs pyqs")  # App Password
RECEIVER_EMAIL = "sgsgowri912@gmail.com"

# Initialize webcam and YOLOv8 model
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
model = YOLO("../Yolo-Weights/yolov8l.pt")

# Define the person class
person_class = "person"

# Setup FPS and CSV writer
prev_time = time.time()
file = open('person_detections.csv', 'w', newline='')
writer = csv.writer(file)
writer.writerow(["Class", "Confidence", "x1", "y1", "x2", "y2"])

# Video writer setup
out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (1280, 720))

# Setup pygame for sound
pygame.mixer.init()
alert_sound = "C:/Users/sgsgo/Downloads/GOWRI - Personal/Smart-Person-Detection-Based-Home-Security-System/Home/alert.wav"

# Email alert function
def send_email_alert(person_count):
    msg = EmailMessage()
    msg['Subject'] = 'Person Detected Alert'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECEIVER_EMAIL
    msg.set_content(f'{person_count} person(s) detected by the camera.')
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print('Alert email sent successfully!')
    except Exception as e:
        print(f'Failed to send email: {e}')

alert_sent = False

# Main loop
while True:
    success, img = cap.read()
    if not success:
        break

    current_time = time.time()
    fps = int(1 / (current_time - prev_time))
    prev_time = current_time

    results = model(img)
    person_count = 0

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w, h = x2 - x1, y2 - y1
            conf = box.conf[0]
            cls = int(box.cls[0])
            class_name = model.names[cls]

            if class_name == person_class and conf > 0.5:
                person_count += 1
                cvzone.cornerRect(img, (x1, y1, w, h))
                cvzone.putTextRect(img, f'{class_name} {conf:.2f}', (x1, max(35, y1)))
                writer.writerow([class_name, conf.item(), x1, y1, x2, y2])

                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load(alert_sound)
                    pygame.mixer.music.play()

    if person_count > 0 and not alert_sent:
        send_email_alert(person_count)
        alert_sent = True

    if person_count == 0:
        alert_sent = False

    cv2.putText(img, f'FPS: {fps}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(img, f'Persons detected: {person_count}', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Image", img)
    out.write(img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
file.close()
pygame.mixer.quit()
cv2.destroyAllWindows()
