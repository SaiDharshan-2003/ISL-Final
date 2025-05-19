import sys
import cv2
import copy
import numpy as np
import pandas as pd
from tensorflow import keras
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QGridLayout, QHBoxLayout
)
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtCore import QTimer, Qt
import mediapipe as mp
from collections import Counter
import string

# Load model
model = keras.models.load_model("model.h5")
alphabet = ['1', '2', '3', '4', '5', '6', '7', '8', '9'] + list(string.ascii_uppercase)

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Landmark processing functions
def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]
    landmark_point = []
    for _, landmark in enumerate(landmarks.landmark):
        x = min(int(landmark.x * image_width), image_width - 1)
        y = min(int(landmark.y * image_height), image_height - 1)
        landmark_point.append([x, y])
    return landmark_point

def pre_process_landmark(landmark_list):
    temp = copy.deepcopy(landmark_list)
    base_x, base_y = temp[0]
    for i in range(len(temp)):
        temp[i][0] -= base_x
        temp[i][1] -= base_y
    flat = []
    for sublist in temp:
        flat.extend(sublist)
    max_val = max(map(abs, flat))
    return [n / max_val for n in flat]

class SignLanguageApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Indian Sign Language Detection")
        self.showFullScreen()

        # Webcam display (Top Left) - 1/4th of the screen
        self.webcam_label = QLabel()
        self.webcam_label.setFixedSize(640, 360)
        self.webcam_label.setStyleSheet("background-color: black; border-radius: 10px;")

        # Prediction display (Top Right)
        self.prediction_label = QLabel("Prediction: ")
        self.prediction_label.setFont(QFont("Arial", 36, QFont.Bold))
        self.prediction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prediction_label.setStyleSheet("color: #2196F3; font-weight: bold; padding: 10px;")

        # ISL chart image (Bottom Left)
        self.isl_image_label = QLabel()
        self.isl_image_label.setFixedSize(640, 360)
        self.isl_image_label.setStyleSheet("background-color: white; border-radius: 10px;")
        self.load_isl_chart("isl_chart.jpg")

        # Buttons (Bottom Right)
        self.start_btn = QPushButton("Start Prediction")
        self.start_btn.setFont(QFont("Arial", 18))
        self.start_btn.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            padding: 15px;
            border-radius: 12px;
            font-weight: bold;
        """)
        self.start_btn.clicked.connect(self.start_prediction)

        self.exit_btn = QPushButton("Exit")
        self.exit_btn.setFont(QFont("Arial", 18))
        self.exit_btn.setStyleSheet("""
            background-color: #F44336;
            color: white;
            padding: 15px;
            border-radius: 12px;
            font-weight: bold;
        """)
        self.exit_btn.clicked.connect(self.close)

        # Layouts
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.exit_btn)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        grid = QGridLayout()
        grid.addWidget(self.webcam_label, 0, 0)
        grid.addWidget(self.prediction_label, 0, 1)
        grid.addWidget(self.isl_image_label, 1, 0)
        grid.addLayout(button_layout, 1, 1)

        self.setLayout(grid)

        # Initialize webcam, timer, and mediapipe hands
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.hands = mp_hands.Hands(
            model_complexity=0,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # Set webcam resolution to 360p
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

        # Initialize sentence formation variables
        self.prediction_queue = []
        self.sentence = ""
        self.inactive_timer = 0
        self.inactive_threshold = 100  # 0.1 second of inactivity to clear the queue
        self.sentence_ready = False
        self.predicted_letters = []

    def load_isl_chart(self, path):
        image = QPixmap(path).scaled(self.isl_image_label.width(), self.isl_image_label.height(), Qt.AspectRatioMode.KeepAspectRatio)
        self.isl_image_label.setPixmap(image)

    def start_prediction(self):
        if not self.cap:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
        self.timer.start(10)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_image)

        if results.multi_hand_landmarks:
            self.inactive_timer = 0
            for hand_landmarks in results.multi_hand_landmarks:
                landmark_list = calc_landmark_list(frame, hand_landmarks)
                processed = pre_process_landmark(landmark_list)
                df = pd.DataFrame(processed).transpose()
                predictions = model.predict(df, verbose=0)
                predicted_label = alphabet[np.argmax(predictions)]

                self.predicted_letters.append(predicted_label)

                if len(self.predicted_letters) > 40:
                    self.predicted_letters.pop(0)

                if len(self.predicted_letters) == 40:
                    most_common_prediction = Counter(self.predicted_letters).most_common(1)[0][0]
                    self.sentence += most_common_prediction
                    self.predicted_letters = []

                self.prediction_label.setText(f"Prediction: {predicted_label}\nSentence: {self.sentence}")

        else:
            self.inactive_timer += 10
            if self.inactive_timer > self.inactive_threshold:
                self.predicted_letters = []
                self.prediction_label.setText(f"Prediction: \nSentence: {self.sentence}")

        h, w, ch = frame.shape
        qt_image = QImage(frame.data, w, h, ch * w, QImage.Format.Format_BGR888)
        self.webcam_label.setPixmap(QPixmap.fromImage(qt_image).scaled(
            self.webcam_label.width(), self.webcam_label.height(), Qt.AspectRatioMode.KeepAspectRatio))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignLanguageApp()
    window.show()
    sys.exit(app.exec())
