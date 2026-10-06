import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                              QLabel, QLineEdit, QPushButton, QMessageBox, 
                              QSpacerItem, QSizePolicy)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from home import HomeWindow
from database import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from werkzeug.security import check_password_hash

DATABASE_URL = "mysql+pymysql://root:@localhost/projectpy_db"
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(450, 200, 530, 250)  # Légèrement plus haut pour mieux s'adapter
        self.setWindowIcon(QIcon("logo/logoProjet.png"))

        # Main layout vertical
        self.main_layout = QVBoxLayout()
        
        # Layout pour le formulaire
        self.form_layout = QVBoxLayout()
        
        # Configuration des champs
        self.username_label = QLabel("Username:")
        self.username_label.setStyleSheet("""
            QLabel {
                font-family: 'Times New Roman';
                font-weight: bold;
                font-size: 23px;
            }
        """)
        
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet("""
            padding: 10px 5px;
            font-family: 'Times New Roman';
            font-size: 18px;
        """)
        
        self.password_label = QLabel("Password:")
        self.password_label.setStyleSheet(self.username_label.styleSheet())
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.username_input.styleSheet())
        
        # Ajout des widgets au formulaire
        self.form_layout.addWidget(self.username_label)
        self.form_layout.addWidget(self.username_input)
        self.form_layout.addWidget(self.password_label)
        self.form_layout.addWidget(self.password_input)
        
        # Layout horizontal pour les boutons (centrés)
        self.button_layout = QHBoxLayout()
        
        # Spacer gauche pour centrage
        self.button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Bouton Back
        self.button_back = QPushButton("Back")
        self.button_back.setFixedWidth(150)
        self.button_back.setStyleSheet("""
            QPushButton {
                background-color: #F29987;
                font-family: 'Times New Roman';
                font-weight: bold;
                font-size: 18px;
                border-radius: 15px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #52A958; 
            }
        """)
        
        # Bouton Login
        self.button_login = QPushButton("Login")
        self.button_login.setFixedWidth(150)
        self.button_login.setStyleSheet(self.button_back.styleSheet())
        
        # Ajout des boutons avec espacement
        self.button_layout.addWidget(self.button_back)
        self.button_layout.addSpacing(20)  # Espace entre les boutons
        self.button_layout.addWidget(self.button_login)
        
        # Spacer droit pour centrage
        self.button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Assemblage des layouts
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.button_layout)
        
        self.setLayout(self.main_layout)
        self.setStyleSheet("background-color: #F5E9DD;")

        # Connexions des signaux
        self.button_login.clicked.connect(lambda: self.verifier_users(
            self.username_input.text(), 
            self.password_input.text()
        ))
        self.button_back.clicked.connect(self.back)
    
    def back(self):
        from main import PomodoroApp
        self.login_window = PomodoroApp()
        self.login_window.show()
        self.close()
    
    def verifier_users(self, username, password):
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password")
            return
            
        user = session.query(User).filter(User.username == username).first()

        if user and self.check_password(password, user.password):
            self.open_home_page(user.id)
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

    def check_password(self, input_password, stored_hashed_password):
        return check_password_hash(stored_hashed_password, input_password)

    def open_home_page(self, user_id):
        self.home_window = HomeWindow(user_id)
        self.home_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())