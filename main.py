import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from PySide6.QtGui import QIcon,QFont
from PySide6.QtCore import Qt
from login import LoginWindow
from signup import SignupWindow


class PomodoroApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PomoNote")
        self.setGeometry(400, 150, 700, 450)
        self.setWindowIcon(QIcon("logo/logoProjet.png"))


        
        # Création d'un layout vertical pour organiser les widgets
        main_layout = QVBoxLayout()
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Ajouter un label
        label = QLabel("Welcome in PomoNote")
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)
        label.setStyleSheet("""
                            QLabel{
                            color: black;
                            font-family: 'Times New Roman';
                            font-size: 50px;
                            font-weight: bold;
                            padding-bottom : 10px;
                            }
                                  """)
        self.subtitle = QLabel("Boost your productivity with focused sessions")
        self.subtitle.setFont(QFont("Arial", 12))
        self.subtitle.setStyleSheet("color: #6B6B6B;")
        self.subtitle.setAlignment(Qt.AlignCenter)


        title_layout = QVBoxLayout()
        title_layout.setSpacing(10)
        title_layout.setAlignment(Qt.AlignCenter) 


        # Créer un layout horizontal pour centrer les boutons
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)
        button_layout.setAlignment(Qt.AlignCenter)

        button1=QPushButton("LogIn 🔓")
        button1.setFixedSize(400, 45)
        button1.setStyleSheet("""
                            QPushButton {
                                background-color: #F29987;
                                border-radius: 15px;
                                padding: 10px 20px;
                                font-family: 'Times New Roman';
                                font-size: 20px;
                                font-weight: bold;
                                transition: background-color 0.3s ease;
                            }
                            QPushButton:hover {
                                background-color: #52A958; 
                            }
                                    """)
        button_layout.addWidget(button1)


        button2=QPushButton("SignUp 📝")
        button2.setFixedSize(400, 45)
        button2.setStyleSheet("""
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

        button_layout.addWidget(button2)

        title_layout.addWidget(label)
        title_layout.addWidget(self.subtitle)

        main_layout.addSpacing(50)
        main_layout.addLayout(title_layout)
        main_layout.addSpacing(100)
        main_layout.addLayout(button_layout)

        #Assure que le layout est effectivement appliqué à la fenêtre
        self.setLayout(main_layout)

        self.setStyleSheet("background-color: #F5E9DD;")

        button1.clicked.connect(self.show_login_window)
        button2.clicked.connect(self.show_signup_window)

        # Footer
        footer = QLabel("© 2025 PomoNote - All rights reserved")
        footer.setFont(QFont("Arial", 9))
        footer.setStyleSheet("color: #999999;")
        footer.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(footer)
    
    def show_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def show_signup_window(self):
        self.signup_window = SignupWindow()
        self.signup_window.show()
        self.close()


        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PomodoroApp()
    window.show()
    sys.exit(app.exec())