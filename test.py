from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                              QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy)
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtCore import Qt

class WelcomePage(QWidget):
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre
        self.setWindowTitle("PomoNote")
        self.setGeometry(400, 200, 600, 400)
        self.setStyleSheet("background-color: #F5F5F5;")
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 20, 40, 40)
        main_layout.setSpacing(30)
        
        # Logo/Titre
        title_layout = QVBoxLayout()
        title_layout.setAlignment(Qt.AlignCenter)
        
        # Logo (remplacez par votre propre image)
        self.logo = QLabel()
        pixmap = QPixmap("logo.png").scaled(120, 120, Qt.KeepAspectRatio)  # Ajoutez votre logo
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignCenter)
        
        # Titre principal
        self.title = QLabel("PomoNote")
        self.title.setFont(QFont("Arial", 28, QFont.Bold))
        self.title.setStyleSheet("color: #2E86AB;")
        self.title.setAlignment(Qt.AlignCenter)
        
        # Sous-titre
        self.subtitle = QLabel("Boost your productivity with focused sessions")
        self.subtitle.setFont(QFont("Arial", 12))
        self.subtitle.setStyleSheet("color: #6B6B6B;")
        self.subtitle.setAlignment(Qt.AlignCenter)
        
        title_layout.addWidget(self.logo)
        title_layout.addWidget(self.title)
        title_layout.addWidget(self.subtitle)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        
        # Bouton Login
        self.login_btn = QPushButton("Login")
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #2E86AB;
                color: white;
                border-radius: 8px;
                padding: 12px 30px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1B6B93;
            }
        """)
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.setFixedHeight(50)
        
        # Bouton SignUp
        self.signup_btn = QPushButton("Sign Up")
        self.signup_btn.setStyleSheet("""
            QPushButton {
                background-color: #F18F01;
                color: white;
                border-radius: 8px;
                padding: 12px 30px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D97E00;
            }
        """)
        self.signup_btn.setCursor(Qt.PointingHandCursor)
        self.signup_btn.setFixedHeight(50)
        
        # Centrer les boutons
        buttons_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        buttons_layout.addWidget(self.login_btn)
        buttons_layout.addWidget(self.signup_btn)
        buttons_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Footer
        footer = QLabel("© 2023 PomoNote - All rights reserved")
        footer.setFont(QFont("Arial", 9))
        footer.setStyleSheet("color: #999999;")
        footer.setAlignment(Qt.AlignCenter)
        
        # Assemblage
        main_layout.addLayout(title_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(buttons_layout)
        main_layout.addStretch(1)
        main_layout.addWidget(footer)
        
        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication([])
    window = WelcomePage()
    window.show()
    app.exec()