import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                              QLabel, QLineEdit, QPushButton, QMessageBox, QSpacerItem,
                              QSizePolicy)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash
from database import User, engine

class SignupWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Signup")
        self.setGeometry(450, 200, 530, 300)
        self.setWindowIcon(QIcon("logo/logoProjet.png"))

        # Main vertical layout
        self.main_layout = QVBoxLayout()
        
        # Form layout
        self.form_layout = QVBoxLayout()
        
        # Label and input fields
        self.fullname_label = QLabel("Fullname:")
        self.fullname_label.setStyleSheet("""
            QLabel{
                font-family: 'Times New Roman';
                font-weight: bold;
                font-size: 23px;
            }
        """)
        self.fullname_input = QLineEdit()
        self.fullname_input.setStyleSheet("""
            padding: 10px 5px;
            font-family: 'Times New Roman';
            font-size: 18px;
        """)
        
        self.username_label = QLabel("Username:")
        self.username_label.setStyleSheet(self.fullname_label.styleSheet())
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet(self.fullname_input.styleSheet())
        
        self.password_label = QLabel("Password:")
        self.password_label.setStyleSheet(self.fullname_label.styleSheet())
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.fullname_input.styleSheet())
        
        # Add widgets to form layout
        self.form_layout.addWidget(self.fullname_label)
        self.form_layout.addWidget(self.fullname_input)
        self.form_layout.addWidget(self.username_label)
        self.form_layout.addWidget(self.username_input)
        self.form_layout.addWidget(self.password_label)
        self.form_layout.addWidget(self.password_input)
        
        # Button layout (horizontal with centering)
        self.button_layout = QHBoxLayout()
        
        # Add left spacer
        self.button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Create buttons
        self.button_back = QPushButton("Back")
        self.button_back.setFixedWidth(150)  # Fixed width for both buttons
        self.button_back.setStyleSheet("""
            QPushButton {
                background-color: #F29987;
                font-family: 'Times New Roman';
                font-weight: bold;
                font-size: 18px;
                border-radius: 15px;
                padding: 8px 15px;
                margin-top: 15px;
            }
            QPushButton:hover {
                background-color: #52A958; 
            }
        """)
        
        self.button_create = QPushButton("Create account")
        self.button_create.setFixedWidth(150)  # Same width as back button
        self.button_create.setStyleSheet(self.button_back.styleSheet())
        
        # Add buttons with spacing between them
        self.button_layout.addWidget(self.button_back)
        self.button_layout.addSpacing(20)  # Space between buttons
        self.button_layout.addWidget(self.button_create)
        
        # Add right spacer
        self.button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Add form and button layouts to main layout
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.button_layout)
        
        self.setLayout(self.main_layout)
        self.setStyleSheet("background-color: #F5E9DD;")

        # Connect signals
        self.button_create.clicked.connect(lambda: self.save_user(
            self.fullname_input.text(), 
            self.username_input.text(), 
            self.password_input.text()
        ))
        self.button_back.clicked.connect(self.back)
    
    def back(self):
        from main import PomodoroApp
        self.login_window = PomodoroApp()
        self.login_window.show()
        self.close()

    def save_user(self, fullname, username, password):
        if not fullname or not username or not password:
            QMessageBox.warning(self, "Input Error", "Please fill all fields.")
            return
        
        hashed_password = generate_password_hash(password)
        result, message = signup(fullname, username, hashed_password)
        
        if result:
            QMessageBox.information(self, "Signup Success", "Account created successfully! Please login.")
            from login import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Signup Failed", message)

def signup(fullname, username, hashed_password):
    Session = sessionmaker(bind=engine)
    session = Session()

    existing_user = session.query(User).filter(User.username == username).first()
    if existing_user:
        return False, "Username already taken."

    new_user = User(fullname=fullname, username=username, password=hashed_password)

    try:
        session.add(new_user)
        session.commit()
        return True, "User registered successfully!"
    except Exception as e:
        session.rollback()
        return False, f"Error registering user: {str(e)}"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignupWindow()
    window.show()
    sys.exit(app.exec())