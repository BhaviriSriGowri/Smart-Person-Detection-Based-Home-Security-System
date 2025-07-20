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
from datetime import datetime

# Allow PyTorch to safely unpickle DetectionModel
add_safe_globals([DetectionModel])

# Email Credentials
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "bhavirisrigowri@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "zjkv hiuo gmhs pyqs")
RECEIVER_EMAIL = "sgsgowri912@gmail.com"

# Webcam and YOLO model setup
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
model = YOLO("../Yolo-Weights/yolov8l.pt")

# Video file setup
video_filename = 'output.avi'
out = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (1280, 720))

# Sound setup
pygame.mixer.init()
alert_sound = "alert.wav"

# CSV file setup
csv_file = 'person_detections.csv'
csv_fields = ["Timestamp", "Class", "Confidence", "x1", "y1", "x2", "y2", "Video Clip"]
file_exists = os.path.isfile(csv_file)

# Email alert function
def send_email_alert(person_count):
    msg = EmailMessage()
    msg['Subject'] = 'Person Detected Alert'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECEIVER_EMAIL
    msg.set_content(f'{person_count} person(s) detected.\nCheck your logs and saved video.')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print('✅ Email alert sent!')
    except Exception as e:
        print(f'❌ Email failed: {e}')

# FPS and flags
prev_time = time.time()
person_class = "person"
alert_sent = False

# Open CSV for appending
with open(csv_file, 'a', newline='') as csv_file_handle:
    csv_writer = csv.writer(csv_file_handle)
    if not file_exists:
        csv_writer.writerow(csv_fields)

    # Main detection loop
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
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                class_name = model.names[cls]

                if class_name == person_class and conf > 0.5:
                    person_count += 1
                    cvzone.cornerRect(img, (x1, y1, w, h))
                    cvzone.putTextRect(img, f'{class_name} {conf:.2f}', (x1, max(35, y1)))

                    # Save to CSV
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    csv_writer.writerow([timestamp, class_name, f"{conf:.2f}", x1, y1, x2, y2, video_filename])
                    csv_file_handle.flush()  # Ensures it's written immediately

                    # Play alert sound
                    if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.load(alert_sound)
                        pygame.mixer.music.play()

        if person_count > 0 and not alert_sent:
            send_email_alert(person_count)
            alert_sent = True

        if person_count == 0:
            alert_sent = False

        # Display overlay info
        cv2.putText(img, f'FPS: {fps}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(img, f'Persons detected: {person_count}', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Image", img)
        out.write(img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Cleanup
cap.release()
out.release()
pygame.mixer.quit()
cv2.destroyAllWindows()
