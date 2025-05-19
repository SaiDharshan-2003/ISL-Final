
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QScrollArea, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

# Mapping letters to JPG images
letter_to_image = {
    'A': 'images/A.jpg',
    'B': 'images/B.jpg',
    'C': 'images/C.jpg',
    'D': 'images/D.jpg',
    'E': 'images/E.jpg',
    'F': 'images/F.jpg',
    'G': 'images/G.jpg',
    'H': 'images/H.jpg',
    'I': 'images/I.jpg',
    'J': 'images/J.jpg',
    'K': 'images/K.jpg',
    'L': 'images/L.jpg',
    'M': 'images/M.jpg',
    'N': 'images/N.jpg',
    'O': 'images/O.jpg',
    'P': 'images/P.jpg',
    'Q': 'images/Q.jpg',
    'R': 'images/R.jpg',
    'S': 'images/S.jpg',
    'T': 'images/T.jpg',
    'U': 'images/U.jpg',
    'V': 'images/V.jpg',
    'W': 'images/W.jpg',
    'X': 'images/X.jpg',
    'Y': 'images/Y.jpg',
    'Z': 'images/Z.jpg',
    '0': 'images/0.jpg',
    '1': 'images/1.jpg',
    '2': 'images/2.jpg',
    '3': 'images/3.jpg',
    '4': 'images/4.jpg',
    '5': 'images/5.jpg',
    '6': 'images/6.jpg',
    '7': 'images/7.jpg',
    '8': 'images/8.jpg',
    '9': 'images/9.jpg',
}

class TextToSignApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text to Sign Language")
        self.setStyleSheet("background-color: #ffffff;")
        self.setFixedSize(800, 400)
        self.setFont(QFont("Segoe UI", 14))

        # Title
        self.label = QLabel("Enter Text (A-Z, 0-9):")
        self.label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #333;")

        # Text input with black text
        self.text_input = QLineEdit()
        self.text_input.setFont(QFont("Segoe UI", 16))
        self.text_input.setStyleSheet("padding: 10px; color: black; border: 2px solid #2196F3; border-radius: 8px;")

        # Convert button
        self.convert_btn = QPushButton("🔤 Convert to Sign Language")
        self.convert_btn.setFont(QFont("Segoe UI", 16))
        self.convert_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 12px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.convert_btn.clicked.connect(self.convert_text_to_sign)

        # Scrollable image area (horizontal)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.image_container = QWidget()
        self.image_layout = QHBoxLayout()
        self.image_layout.setAlignment(Qt.AlignLeft)
        self.image_container.setLayout(self.image_layout)
        self.scroll_area.setWidget(self.image_container)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_input)
        layout.addWidget(self.convert_btn)
        layout.addSpacing(10)
        layout.addWidget(self.scroll_area)
        layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(layout)

    def convert_text_to_sign(self):
        text = self.text_input.text().upper()
        if not text:
            return

        # Clear previous images
        for i in reversed(range(self.image_layout.count())):
            widget = self.image_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Add images horizontally
        for char in text:
            if char in letter_to_image:
                img_path = letter_to_image[char]
                pixmap = QPixmap(img_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                label = QLabel()
                label.setPixmap(pixmap)
                self.image_layout.addWidget(label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextToSignApp()
    window.show()
    sys.exit(app.exec())

