from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                              QTabWidget, QTextEdit, QLineEdit, QMessageBox, QHBoxLayout)
from PySide6.QtGui import QIcon
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from database import Note

# Configuration de la base de données
DATABASE_URL = "mysql+pymysql://root:@localhost/projectpy_db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

class NotesApp(QWidget):
    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id
        
        self.setWindowTitle("Notes")
        self.setGeometry(400, 150, 700, 450)
        self.setWindowIcon(QIcon("logo/logoProjet.png"))
        
        # Layout principal
        self.layout = QVBoxLayout()
        
        # Widget des onglets
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)
        
        # Charger les notes
        self.load_notes()
        
        # Créer un layout horizontal pour les boutons
        self.button_layout = QHBoxLayout()
        
        # Bouton Nouvelle Note
        self.new_button = QPushButton("New Note ➕")
        self.new_button.clicked.connect(self.add_note)
        self.new_button.setStyleSheet(self.get_button_style())
        self.button_layout.addWidget(self.new_button)
        
        # Bouton Supprimer Note
        self.delete_button = QPushButton("Delete Note 🗑️")
        self.delete_button.clicked.connect(self.delete_note)
        self.delete_button.setStyleSheet(self.get_button_style())
        self.button_layout.addWidget(self.delete_button)

        # Bouton Retour à l'accueil
        self.home_button = QPushButton("Back To Home 🏠")
        self.home_button.setStyleSheet(self.get_button_style())
        self.home_button.clicked.connect(self.show_home)
        self.button_layout.addWidget(self.home_button)
        
        # Ajouter le layout des boutons au layout principal
        self.layout.addLayout(self.button_layout)
        
        # Définir le layout principal
        self.setLayout(self.layout)
        self.setStyleSheet("background-color: #F5E9DD;")
    
    def get_button_style(self):
        return """
            QPushButton {
                background-color: #F29987;
                border-radius: 15px;
                padding: 5px 20px;
                font-size: 20px;
                font-family: 'Times New Roman';
                font-weight: bold;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #52A958;
            }
        """
    
    def load_notes(self):
        try:
            # Charger seulement les notes de l'utilisateur connecté
            notes = session.query(Note).filter_by(user_id=self.user_id).all()
            for note in notes:
                self.add_note_tab(note.title, note.content, note.id)
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Could not load notes: {str(e)}")
    
    def add_note(self):
        new_tab = QWidget()
        layout = QVBoxLayout()
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter title...")
        self.title_input.setStyleSheet("""
            QLineEdit {
                color: black;
                font-family: 'Times New Roman';
                font-size: 18px;
                padding: 10px;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(self.title_input)
        
        self.content_input = QTextEdit()
        self.content_input.setStyleSheet("""
            QTextEdit {
                color: black;
                font-family: 'Times New Roman';
                font-size: 18px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.content_input)
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(lambda: self.save_note(new_tab))
        save_button.setStyleSheet(self.get_button_style())
        layout.addWidget(save_button)
        
        new_tab.setLayout(layout)
        self.tabs.addTab(new_tab, "New Note")
        self.tabs.setCurrentIndex(self.tabs.count() - 1)
    
    def save_note(self, tab):
        title = self.title_input.text().strip()
        content = self.content_input.toPlainText().strip()
        
        if not title:
            QMessageBox.warning(self, "Error", "Title cannot be empty!")
            return
        
        try:
            # Créer une nouvelle note avec l'user_id
            new_note = Note(
                title=title, 
                content=content,
                user_id=self.user_id
            )
            session.add(new_note)
            session.commit()
            
            index = self.tabs.indexOf(tab)
            self.tabs.removeTab(index)
            self.add_note_tab(title, content, new_note.id)
            
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Database Error", f"Could not save note: {str(e)}")
    
    def add_note_tab(self, title, content, note_id=None):
        note_tab = QWidget()
        layout = QVBoxLayout()
        
        content_display = QTextEdit()
        content_display.setText(content)
        content_display.setReadOnly(True)
        content_display.setStyleSheet("""
            QTextEdit {
                color: black;
                font-family: 'Times New Roman';
                font-size: 18px;
                padding: 10px;
            }
        """)
        layout.addWidget(content_display)
        
        note_tab.setLayout(layout)
        self.tabs.addTab(note_tab, title)
        if note_id:
            note_tab.note_id = note_id
    
    def delete_note(self):
        current_tab = self.tabs.currentWidget()
        if not hasattr(current_tab, 'note_id'):
            self.tabs.removeTab(self.tabs.currentIndex())
            return
            
        confirm = QMessageBox.question(
            self, 
            "Delete Note", 
            "Are you sure you want to delete this note?", 
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            try:
                # Vérifier que la note appartient bien à l'utilisateur avant suppression
                note = session.query(Note).filter(
                    Note.id == current_tab.note_id,
                    Note.user_id == self.user_id
                ).first()
                
                if note:
                    session.delete(note)
                    session.commit()
                    self.tabs.removeTab(self.tabs.currentIndex())
                else:
                    QMessageBox.warning(self, "Error", "Note not found or access denied")
            except Exception as e:
                session.rollback()
                QMessageBox.critical(self, "Database Error", f"Could not delete note: {str(e)}")

    def show_home(self,user_id):
        from home import HomeWindow
        self.new_window = HomeWindow(self.user_id)
        self.new_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    # Exemple: user_id = 1 pour le test
    window = NotesApp(user_id=1)
    window.show()
    app.exec()