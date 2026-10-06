import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                              QVBoxLayout, QWidget, QHBoxLayout)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QTimer
import pygame

class PomodoroTimer(QMainWindow):
    def __init__(self, user_id):
        super().__init__()

        pygame.mixer.init()

        self.user_id = user_id

        self.study_duration = 25 * 60  # 25 minutes
        self.break_duration = 5 * 60   # 5 minutes
        self.time_left = self.study_duration

        self.on_break = False  # Pour savoir si on est en break ou en session de focus

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        try:
            self.sound = pygame.mixer.Sound("sounds/alarm.wav")
        except pygame.error as e:
            print(f"Erreur lors du chargement du fichier son : {e}")
        
        self.init_ui(self.user_id)

    def init_ui(self, user_id):
        self.user_id = user_id

        self.status_label = QLabel("🎯 Focus Mode", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                font-family: 'Times New Roman';
                font-size: 20px;
                margin: 0px;
            }
        """)

        self.time_display = QLabel(self.format_time(self.time_left), self)
        self.time_display.setAlignment(Qt.AlignCenter)
        self.time_display.setStyleSheet("""
            QLabel {
                font-family: 'Times New Roman';
                font-weight: bold;
                font-size: 40px;
                margin: 0px;
            }
        """)

        # Création des boutons
        self.start_button = QPushButton("▶️", self)
        self.start_button.clicked.connect(self.start_timer)

        self.stop_button = QPushButton("⏸️", self)
        self.stop_button.clicked.connect(self.stop_timer)

        self.reset_button = QPushButton("🔁", self)
        self.reset_button.clicked.connect(self.reset_timer)

        # Style des boutons
        button_style = """
        QPushButton {
            background-color: #52A958;
            border-radius: 10px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #F29987;
        }
        QPushButton:disabled {
            background-color: #cccccc;
        }
        """
        for btn in [self.start_button, self.stop_button, self.reset_button]:
            btn.setStyleSheet(button_style)
            btn.setFixedHeight(30)

        # Layout horizontal pour les boutons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.reset_button)
        button_layout.setSpacing(5)
        button_layout.setContentsMargins(0, 0, 0, 0)

        # Layout principal vertical
        main_layout = QVBoxLayout()
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        main_layout.addWidget(self.time_display)
        main_layout.addWidget(self.status_label)
        main_layout.addSpacing(5)
        main_layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.setWindowTitle("Pomodoro Timer")
        self.setGeometry(1290, 20, 200, 100)
        self.setWindowIcon(QIcon("logo/logoProjet.png"))
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5E9DD;
                border-radius: 5px;
            }
        """)

        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        
        # Désactiver les boutons au démarrage
        self.stop_button.setEnabled(False)
        self.reset_button.setEnabled(False)

    def format_time(self, seconds):
        minutes, sec = divmod(seconds, 60)
        return f"{minutes:02}:{sec:02}"

    def start_timer(self):
        self.timer.start(1000)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.reset_button.setEnabled(False)

    def stop_timer(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.reset_button.setEnabled(True)

    def reset_timer(self):
        self.stop_timer()
        self.on_break = False
        self.time_left = self.study_duration
        self.status_label.setText("🎯 Focus Mode")
        self.time_display.setText(self.format_time(self.time_left))
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.reset_button.setEnabled(True)

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.time_display.setText(self.format_time(self.time_left))
        else:
            self.timer.stop()
            self.sound.play()
            if self.on_break:
                self.on_break = False
                self.time_left = self.study_duration
                self.status_label.setText("🎯 Focus Mode")
            else:
                self.on_break = True
                self.time_left = self.break_duration
                self.status_label.setText("🧘‍♂️ Relax Mode")
            self.time_display.setText(self.format_time(self.time_left))
            self.timer.start(1000)


if __name__ == "__main__":
    app = QApplication([])
    user_id = 1
    window = PomodoroTimer(user_id)
    app.exec()