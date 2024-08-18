import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QWidget, QMessageBox

TASKS_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file)

class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tasks = load_tasks()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('To-Do List')
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        self.task_input = QLineEdit(self)
        self.layout.addWidget(self.task_input)
        
        self.add_button = QPushButton('Add Task', self)
        self.add_button.clicked.connect(self.add_task)
        self.layout.addWidget(self.add_button)
        
        self.task_list = QListWidget(self)
        self.load_task_list()
        self.layout.addWidget(self.task_list)
        
        self.complete_button = QPushButton('Mark as Completed', self)
        self.complete_button.clicked.connect(self.complete_task)
        self.layout.addWidget(self.complete_button)
        
        self.delete_button = QPushButton('Delete Task', self)
        self.delete_button.clicked.connect(self.delete_task)
        self.layout.addWidget(self.delete_button)
        
        self.show()

    def load_task_list(self):
        self.task_list.clear()
        for task in self.tasks:
            self.task_list.addItem(f"{task['id']}. {task['description']} - {task['status']}")

    def add_task(self):
        description = self.task_input.text()
        if description:
            task_id = len(self.tasks) + 1
            self.tasks.append({'id': task_id, 'description': description, 'status': 'pending'})
            save_tasks(self.tasks)
            self.load_task_list()
            self.task_input.clear()
        else:
            QMessageBox.warning(self, "Warning", "Task description cannot be empty.")

    def complete_task(self):
        selected_items = self.task_list.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            task_id = int(selected_item.text().split('.')[0])
            for task in self.tasks:
                if task['id'] == task_id:
                    task['status'] = 'completed'
                    save_tasks(self.tasks)
                    self.load_task_list()
                    return
        else:
            QMessageBox.warning(self, "Warning", "Please select a task to mark as completed.")

    def delete_task(self):
        selected_items = self.task_list.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            task_id = int(selected_item.text().split('.')[0])
            self.tasks = [task for task in self.tasks if task['id'] != task_id]
            save_tasks(self.tasks)
            self.load_task_list()
        else:
            QMessageBox.warning(self, "Warning", "Please select a task to delete.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TodoApp()
    sys.exit(app.exec_())
