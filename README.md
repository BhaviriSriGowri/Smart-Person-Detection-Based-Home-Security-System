# Smart Person Detection-Based Home Security System



A robust, real-time home security solution using AI and computer vision. This system leverages YOLOv8 for person detection, OpenCV for video capture, Pygame for audio alerts, and SMTP for email notifications. Detections are logged to CSV and recorded to video.



---



\## 🔍 Table of Contents



1\. \[Features](#-features)

2\. \[Project Structure](#-project-structure)

3\. \[Installation](#-installation)

4\. \[Configuration](#-configuration)

5\. \[Usage](#-usage)

6\. \[Logs \& Outputs](#-logs--outputs)

7\. \[GitHub Commands](#-github-commands)



---



\## 🚀 Features



\* \*\*Real-time Detection:\*\* Uses YOLOv8 (Ultralytics) to detect persons via webcam.

\* \*\*Audio \& Email Alerts:\*\* Plays an alert sound and sends email notifications on detection.

\* \*\*Video Recording:\*\* Saves detection footage to `output.avi` for review.

\* \*\*CSV Logging:\*\* Appends each detection to `person\_detections.csv` with timestamp, confidence, and bounding box.

\* \*\*Modular \& Extensible:\*\* Easily integrate additional object classes or alert methods.



---



\## 📁 Project Structure



```

Smart-Person-Detection-Based-Home-Security-System/

├── person.py                  # Core detection script

├── alert.wav                  # Sound played on detection

├── output.avi                 # Recorded video of detections

├── person\_detections.csv      # Detection log file

├── requirements.txt           # Python dependencies

├── .gitignore                 # Ignore unnecessary files

├── Procfile                   # For deployment (Render)

├── runtime.txt                # Python version spec

├── start.sh                   # Shell script for launching app

├── templates/                 # Flask HTML templates (unused currently)

│   └── index.html

└── Yolo-Weights/              # YOLOv8 pretrained weights

&nbsp;   └── yolov8l.pt

```



---



\## 📦 Installation



1\. \*\*Clone the repository\*\*:



&nbsp;  ```bash

&nbsp;  git clone https://github.com/BhaviriSriGowri/Smart-Person-Detection-Based-Home-Security-System.git

&nbsp;  cd Smart-Person-Detection-Based-Home-Security-System

&nbsp;  ```



2\. \*\*Create a virtual environment\*\* (recommended):



&nbsp;  ```bash

&nbsp;  python -m venv venv

&nbsp;  source venv/bin/activate   # On Windows: venv\\Scripts\\activate

&nbsp;  ```



3\. \*\*Install dependencies\*\*:



&nbsp;  ```bash

&nbsp;  pip install -r requirements.txt

&nbsp;  ```



4\. \*\*Download YOLO weights\*\* if not present:



&nbsp;  ```bash

&nbsp;  # Place yolov8l.pt into Yolo-Weights/ or download:

&nbsp;  wget https://github.com/ultralytics/ultralytics/releases/download/v8.2.14/yolov8l.pt -P Yolo-Weights/

&nbsp;  ```



---



\## ⚙️ Configuration



1\. \*\*Email Alerts\*\*: In `person.py`, set environment variables or directly update the values (use environment variables in production):



&nbsp;  ```python

&nbsp;  EMAIL\_ADDRESS = os.getenv("EMAIL\_ADDRESS", "your\_email@gmail.com")

&nbsp;  EMAIL\_PASSWORD = os.getenv("EMAIL\_PASSWORD", "your\_app\_password")

&nbsp;  RECEIVER\_EMAIL = "receiver\_email@gmail.com"

&nbsp;  ```



&nbsp;  \* Use Gmail App Passwords for secure access.



2\. \*\*Paths\*\*: Ensure:



&nbsp;  \* `alert.wav` is present and properly referenced.

&nbsp;  \* YOLOv8 model path is correct inside the script.



---



\## ▶️ Usage



\### Run Detection Script



```bash

python person.py

```



\* Webcam window will display with bounding boxes around detected persons.

\* Audio alert plays (`alert.wav`), and email notification is sent.

\* Detection is logged into `person\_detections.csv`.

\* Recorded video is saved as `output.avi`.



\### Quit



\* Press `q` in the OpenCV window to stop detection.



---



\## 📊 Logs \& Outputs



\* \*\*person\\\_detections.csv\*\*:



&nbsp; | Timestamp           | Class  | Confidence | x1  | y1  | x2  | y2  | Video      |

&nbsp; | --------------------- | -------- | ------------ | ----- | ---- | ---- | ---- | ----------- |

&nbsp; | 2025-07-20 10:00:01 | Person | 0.87       | 100 | 150 | 300 | 450 | output.avi |



\* \*\*output.avi\*\*: MP4/AVI format video file containing detection footage.



---



\## 💻 GitHub Commands



\### After creating or modifying files:



```bash

git add .

git commit -m "Added new files and logs"

git push origin main  # or 'master' depending on your branch name

```



\### Clone the repo (in a new machine or setup):



```bash

git clone https://github.com/BhaviriSriGowri/Smart-Person-Detection-Based-Home-Security-System.git

cd Smart-Person-Detection-Based-Home-Security-System

```



\### Run project again:



```bash

python person.py

```



---



✅ Project setup complete.



