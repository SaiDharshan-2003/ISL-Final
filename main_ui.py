
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from isl_predict import SignLanguageApp
from text_to_sign import TextToSignApp

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign Language Translator")
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: #ffffff;")
        self.setFont(QFont("Segoe UI", 12))

        # Title Label
        self.label = QLabel("Welcome to Sign Language Translator")
        self.label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: #333333;")

        # Horizontal divider
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #cccccc; margin: 10px 20px;")

        # Button: Start Sign Prediction
        self.prediction_btn = QPushButton("🖐  Start Sign Prediction")
        self.prediction_btn.setFont(QFont("Segoe UI", 16))
        self.prediction_btn.setStyleSheet(self.button_style("#4CAF50"))
        self.prediction_btn.setCursor(Qt.PointingHandCursor)
        self.prediction_btn.clicked.connect(self.open_sign_prediction)

        # Button: Convert Text to Sign
        self.text_to_sign_btn = QPushButton("🔤  Convert Text to Sign")
        self.text_to_sign_btn.setFont(QFont("Segoe UI", 16))
        self.text_to_sign_btn.setStyleSheet(self.button_style("#2196F3"))
        self.text_to_sign_btn.setCursor(Qt.PointingHandCursor)
        self.text_to_sign_btn.clicked.connect(self.open_text_to_sign)

        # Layout setup
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.label)
        layout.addWidget(line)
        layout.addSpacing(20)
        layout.addWidget(self.prediction_btn)
        layout.addWidget(self.text_to_sign_btn)
        layout.setSpacing(20)
        layout.setContentsMargins(60, 40, 60, 40)
        layout.addStretch()
        self.setLayout(layout)

    def button_style(self, color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                padding: 15px;
                border: none;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: darken({color}, 10%);
                opacity: 0.9;
            }}
        """

    def open_sign_prediction(self):
        self.sign_window = SignLanguageApp()
        self.sign_window.show()

    def open_text_to_sign(self):
        self.text_sign_window = TextToSignApp()
        self.text_sign_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
