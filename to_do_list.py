from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QMessageBox, QHBoxLayout,QListWidgetItem
from PySide6.QtGui import QFont, QColor, QIcon
from PySide6.QtCore import Qt
from database import User, Task
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://root:@localhost/projectpy_db"

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class TodoListApp(QWidget):
    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id

        self.setWindowTitle("Todo List")
        self.setGeometry(400, 150, 700, 450)
        self.setWindowIcon(QIcon("logo/logoProjet.png"))
        
        self.layout = QVBoxLayout()

        # Input field for tasks
        self.task_input = QLineEdit(self)
        self.task_input.setFont(QFont("Arial", 14))
        self.task_input.setPlaceholderText("Enter your todo here...")
        self.task_input.setStyleSheet(self.get_button_styles())
        self.layout.addWidget(self.task_input)
        
        # Add Task Button
        self.add_button = QPushButton("Add 📝", self)
        self.add_button.clicked.connect(self.add_task)
        self.add_button.setStyleSheet(self.get_button_styles())
        self.layout.addWidget(self.add_button)
        
        # Pomodoro Timer Button
        self.timer_button = QPushButton("Pomodoro Timer ⏱️", self)
        self.timer_button.clicked.connect(self.show_timer)
        self.timer_button.setStyleSheet(self.get_button_styles())
        self.layout.addWidget(self.timer_button)

        # Task list display
        self.task_list = QListWidget(self)
        self.task_list.setStyleSheet("""
            QListWidget {
                border: none;
                font-size: 20px;
                font-family: 'Times New Roman';
            }
        """)
        self.layout.addWidget(self.task_list)

        # Button Layout
        button_layout = QHBoxLayout()

        # Done Button
        self.done_button = QPushButton("Done ✅", self)
        self.done_button.clicked.connect(self.mark_done)
        self.done_button.setStyleSheet(self.get_button_styles())
        button_layout.addWidget(self.done_button)

        # Delete Button
        self.delete_button = QPushButton("Delete 🗑️", self)
        self.delete_button.clicked.connect(self.delete_task)
        self.delete_button.setStyleSheet(self.get_button_styles())
        button_layout.addWidget(self.delete_button)

        # Stats Button
        self.stats_button = QPushButton("View Stats 🗂️", self)
        self.stats_button.clicked.connect(self.view_stats)
        self.stats_button.setStyleSheet(self.get_button_styles())
        button_layout.addWidget(self.stats_button)

        # Add button layout to the main layout
        self.layout.addLayout(button_layout)

        # Back To Home Button
        self.home_button = QPushButton("Back To Home 🏠", self)
        self.home_button.setStyleSheet(self.get_button_styles())
        self.home_button.clicked.connect(self.show_home)
        self.layout.addWidget(self.home_button)

        # Set the main layout
        self.setLayout(self.layout)

        # Load existing tasks
        self.load_tasks()

        # Set background color
        self.setStyleSheet("background-color: #F5E9DD;")

    def get_button_styles(self):
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

    def show_timer(self,user_id):
        from todo_timer import PomodoroTimer
        self.new_window = PomodoroTimer(self.user_id)
        self.new_window.show()

    def show_home(self,user_id):
        from home import HomeWindow
        self.new_window = HomeWindow(self.user_id)
        self.new_window.show()
        self.close()

    def add_task(self):
        task = self.task_input.text().strip()
        if task:
            new_task = Task(text=task, user_id=self.user_id, color="black")
            session.add(new_task)
            session.commit()
            self.load_tasks()
            self.task_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a task.")

    def mark_done(self):
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Selection Error", "Please select a task to mark as done.")
            return

        for item in selected_items:
            task_id_data = item.data(Qt.UserRole)
            if task_id_data is None:
                print("No task ID associated with item.")
                continue

            try:
                task_id = int(task_id_data)
                task = session.query(Task).filter(Task.id == task_id).first()
            
                if not task:
                    print("Task not found in database.")
                    continue

                # Mise à jour de la tâche
                task.done = True
                session.commit()
                print(f"Task marked as done: {task.text}")
            
                # Mise à jour visuelle
                item.setForeground(QColor("green"))
            
            except ValueError:
                print(f"Invalid task ID: {task_id_data}")
            except Exception as e:
                session.rollback()
                print(f"Error updating task: {str(e)}")
                QMessageBox.critical(self, "Database Error", f"Could not update task: {str(e)}")

        self.load_tasks()  # Recharger pour synchronisation

    def delete_task(self):
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Selection Error", "Please select a task to delete.")
            return

        for item in selected_items:
            task_id_data = item.data(Qt.UserRole)
            if task_id_data is None:
                print("No task ID associated with item.")
                continue

            try:
                task_id = int(task_id_data)
                task = session.query(Task).filter(Task.id == task_id).first()
            
                if not task:
                    print("Task not found in database.")
                    continue

                # Suppression de la tâche
                session.delete(task)
                session.commit()
                print(f"Task deleted: {task.text}")
            
                # Suppression visuelle
                row = self.task_list.row(item)
                self.task_list.takeItem(row)
            
            except ValueError:
                print(f"Invalid task ID: {task_id_data}")
            except Exception as e:
                session.rollback()
                print(f"Error deleting task: {str(e)}")
                QMessageBox.critical(self, "Database Error", f"Could not delete task: {str(e)}")

        self.load_tasks()  # Recharger pour synchronisation

    def load_tasks(self):
        self.task_list.clear()
    
        try:
            tasks = session.query(Task).filter(Task.user_id == self.user_id).all()
        
            if not tasks:
                print("No tasks found in database.")
                return

            for task in tasks:
                item = QListWidgetItem(task.text)
                item.setForeground(QColor("green") if task.done else QColor("black"))
                item.setData(Qt.UserRole, task.id)
                self.task_list.addItem(item)
            
                # Debug output
                print(f"Loaded Task - ID: {task.id}, Text: {task.text}, Done: {task.done}")
            
        except Exception as e:
            print(f"Error loading tasks: {str(e)}")
            QMessageBox.critical(self, "Database Error", f"Could not load tasks: {str(e)}")

    def view_stats(self):
        tasks = session.query(Task).filter(Task.user_id == self.user_id).all()  # Récupérer toutes les tâches de l'utilisateur
        total_tasks = len(tasks)  # Nombre total de tâches
        done_tasks = sum(1 for task in tasks if task.done)  # Nombre de tâches terminées
        QMessageBox.information(self, "Stats", f"Total tasks: {total_tasks}\nDone tasks: {done_tasks}")
        return total_tasks, done_tasks


if __name__ == "__main__":
    app = QApplication([])
    user_id = 1
    window = TodoListApp(user_id)
    window.show()
    app.exec()
