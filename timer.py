import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QTimer
import pygame

class PomodoroTimer(QMainWindow):
    def __init__(self,user_id):
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

    def init_ui(self,user_id):

        self.user_id = user_id

        self.status_label = QLabel("🎯Focus Mode", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
            font-family: 'Times New Roman';
            font-size: 30px;
            margin: 0px;
        } """)

        self.time_display = QLabel(self.format_time(self.time_left), self)
        self.time_display.setAlignment(Qt.AlignCenter)
        self.time_display.setStyleSheet("""
            QLabel {
            font-family: 'Times New Roman';
            font-weight: bold;
            font-size: 80px;
            margin: 0px;
            } """)

        self.start_button = QPushButton("Start ▶️", self)
        self.start_button.clicked.connect(self.start_timer)

        self.stop_button = QPushButton("Stop ⏸️", self)
        self.stop_button.clicked.connect(self.stop_timer)

        self.reset_button = QPushButton("Reset 🔁", self)
        self.reset_button.clicked.connect(self.reset_timer)

        self.home_button = QPushButton("Back To Home 🏠", self)
        self.home_button.clicked.connect(self.show_home)

        button_style = """
        QPushButton {
            background-color: #52A958;
            border-radius: 15px;
            padding: 7px 50px;
            font-size: 20px;
            font-family: 'Times New Roman';
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #F29987;
        }
        """
        for btn in [self.start_button, self.stop_button, self.reset_button, self.home_button]:
            btn.setStyleSheet(button_style)

        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(20, 15, 20, 15)

        layout.addWidget(self.time_display)
        layout.addWidget(self.status_label)
        layout.addSpacing(10)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.home_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setWindowTitle("Pomodoro Timer")
        self.setGeometry(1200, 20, 200, 100)
        self.setWindowIcon(QIcon("logo/logoProjet.png"))
        self.setStyleSheet("background-color: #F5E9DD;")

        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        
        self.show()

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
        self.status_label.setText("Focus Mode 🎯")
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
                self.status_label.setText("Focus Mode 🎯")
            else:
                self.on_break = True
                self.time_left = self.break_duration
                self.status_label.setText("Relax Mode 🧘‍♂️")
            self.time_display.setText(self.format_time(self.time_left))
            self.timer.start(1000)

    def show_home(self,user_id):
        from home import HomeWindow
        self.new_window = HomeWindow(self.user_id)
        self.new_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication([])
    user_id = 1
    window = PomodoroTimer(user_id)
    app.exec()
