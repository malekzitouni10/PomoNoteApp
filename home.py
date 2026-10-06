import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout,QHBoxLayout, QTextEdit, QPushButton, QLabel, QLineEdit
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from timer import PomodoroTimer
from to_do_list import TodoListApp
from take_note import NotesApp


class HomeWindow(QWidget):
    def __init__(self,user_id):
        super().__init__()

        self.user_id = user_id

        self.setWindowTitle("Home")
        self.setGeometry(400, 150, 700, 450)
        self.setWindowIcon(QIcon("logo/logoProjet.png"))

        self.layout=QVBoxLayout()
        self.layout.setSpacing(20)

        self.qoute=QLabel("Success is the sum of small efforts, repeated day \n in and day out.")
        self.qoute.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.qoute.setStyleSheet("""
                                QLabel{
                                    color: black;
                                    font-family: 'Times New Roman';
                                    font-size: 30px;
                                    font-weight: bold;
                                }
                                """)

        self.qouteacture=QLabel("- Robert Collier -")
        self.qouteacture.setAlignment(Qt.AlignCenter)
        self.qouteacture.setStyleSheet("""
                                QLabel{
                                    color: black;
                                    font-family: 'Times New Roman';
                                    font-size: 20px;
                                }
                                """)
        self.layoutbotton=QVBoxLayout()
        self.layoutbotton.setSpacing(10)
        self.layoutbotton.setAlignment(Qt.AlignCenter)

        self.timer_botton=QPushButton("Pomodoro Timer 🍅")
        self.timer_botton.setFixedSize(400, 45)
        self.timer_botton.setStyleSheet("""
                            QPushButton {
                                background-color: #F29987;
                                border-radius: 15px;
                                padding: 10px 20px;
                                font-size: 20px;
                                font-family: 'Times New Roman';
                                font-weight: bold;
                                transition: background-color 0.3s ease;
                            }
                            QPushButton:hover {
                                background-color: #52A958;
                            }
                                    """)
        self.notes_botton=QPushButton("Take Notes 📄")
        self.notes_botton.setFixedSize(400, 45)
        self.notes_botton.setStyleSheet("""
                            QPushButton {
                                background-color: #F29987;
                                border-radius: 15px;
                                padding: 10px 20px;
                                font-size: 20px;
                                font-family: 'Times New Roman';
                                font-weight: bold;
                                transition: background-color 0.3s ease;
                            }
                            QPushButton:hover {
                                background-color: #52A958;
                            }
                                    """)
        self.todo_botton=QPushButton("To Do List ✏️")
        self.todo_botton.setFixedSize(400, 45)
        self.todo_botton.setStyleSheet("""
                            QPushButton {
                                background-color: #F29987;
                                border-radius: 15px;
                                padding: 10px 20px;
                                font-size: 20px;
                                font-family: 'Times New Roman';
                                font-weight: bold;
                                transition: background-color 0.3s ease;
                            }
                            QPushButton:hover {
                                background-color: #52A958;
                            }
                                    """)

        self.layout.addWidget(self.qoute)
        self.layout.addWidget(self.qouteacture)
        self.layoutbotton.addWidget(self.timer_botton)
        self.layoutbotton.addWidget(self.notes_botton)
        self.layoutbotton.addWidget(self.todo_botton)
        self.layout.addLayout(self.layoutbotton)

        self.setLayout(self.layout)
        self.setStyleSheet("background-color: #F5E9DD;")

        self.timer_botton.clicked.connect(self.show_timer)
        self.notes_botton.clicked.connect(self.show_notes)
        self.todo_botton.clicked.connect(self.show_todo)


    def show_timer(self,user_id):
        self.timer_window = PomodoroTimer(self.user_id)
        self.timer_window.show()
        self.close()

    def show_notes(self,user_id):
        self.notes_window = NotesApp(self.user_id)
        self.notes_window.show()
        self.close()

    def show_todo(self,user_id):
        self.todo_window = TodoListApp(self.user_id)
        self.todo_window.show()
        self.close()

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    user_id = 1
    window = HomeWindow(user_id)
    window.show()
    sys.exit(app.exec())