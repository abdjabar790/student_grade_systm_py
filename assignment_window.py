from ast import Lambda
from ctypes import alignment
from msilib import Dialog
import sys
from tkinter import messagebox
from tkinter.ttk import Style
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
   QDialog, QDialogButtonBox, QApplication, QLineEdit, QMainWindow, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy
)
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QPainterPath, QPainter, QIcon
import sqlite3

from DBContext import add_assignment, delete_assignment, get_assignments_by_lecturer

from assignment import Assignment
from grades_window import GradesWindow


 
###############################


db = sqlite3.connect("school.db")

class AddAssignmentDialog(QDialog):
    def __init__(self, teacher_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add Assignment')
        self.setWindowIcon(QIcon("icons/homework.png"))
        self.teacher_id = teacher_id

        layout = QVBoxLayout(self)
       
        self.assignment_name_input = QLineEdit(self)
        self.assignment_name_input.setPlaceholderText('Assignment Name')
        
        self.assignment_description = QLineEdit(self)
        self.assignment_description.setPlaceholderText('assignment_description')
        
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.add_assign)
        button_box.rejected.connect(self.reject)

        layout.addWidget(QLabel('Assignment Details'))
       
        layout.addWidget(self.assignment_name_input)
        layout.addWidget(self.assignment_description)
       
        layout.addWidget(button_box)

    def add_assign(self):
        
        assignment_name = self.assignment_name_input.text()
        des = self.assignment_description.text()
       
        assign = Assignment(assignment_name,des,self.teacher_id)
        add_assignment(assign,self)
    

class AssignmentsWindow(QDialog):
    def __init__(self, teacher_id):
        super().__init__()
        self.setWindowTitle('Assignments for Teacher ID: ' + str(teacher_id))
        self.setGeometry(450, 150, 800, 400)
        self.setWindowIcon(QIcon("icons/homework.png"))

        main_layout = QHBoxLayout(self)

        sidebar_widget = QWidget(self)
        sidebar_widget.setStyleSheet("background-color: #054359; color:white ")
        sidebar_widget.setFixedWidth(200)

        sidebar_content = QVBoxLayout(sidebar_widget)
        sidebar_content.setContentsMargins(0, 0, 0, 0)

        std_image = QLabel(self)
        pyxmp = QPixmap('icons/asmn.jpg').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        circlstd = self.make_image_circular(pyxmp)
        std_image.setPixmap(circlstd)

        add_button = QPushButton('Add Assignment', self)
        add_button.clicked.connect(self.add_assignment_dialog)
        add_button.setStyleSheet("background-color: #57A6A1; color: black; border-radius:5px; padding: 5px; margin:5px")

    

        delete_button = QPushButton('Delete Assignment', self)
        delete_button.clicked.connect(self.del_assign)
        delete_button.setStyleSheet("background-color: red; color: black; border-radius:5px; padding: 5px; margin:5px")

        grades_button = QPushButton('Show Grades', self)
        grades_button.setStyleSheet("background-color: #f39c12; color: black; border-radius:5px; padding: 5px; margin:5px")
        grades_button.clicked.connect(self.show_grades)
        
        
        sidebar_content.addWidget(std_image, alignment=Qt.AlignCenter)
        sidebar_content.addSpacing(30)
        sidebar_content.addWidget(add_button)
        sidebar_content.addSpacing(20)
        sidebar_content.addWidget(grades_button)
        sidebar_content.addSpacing(20)
        sidebar_content.addWidget(delete_button)
        sidebar_content.addStretch()

        sidebar_widget.setLayout(sidebar_content)
        main_layout.addWidget(sidebar_widget)

        self.teacher_id = teacher_id
        self.assignments_table = QTableWidget(self)

        self.load_assignments_data()

        main_layout.addWidget(self.assignments_table)
        self.setLayout(main_layout)

    def load_assignments_data(self):
        self.assignments_table.setRowCount(0)
        assig_cursor = db.cursor()
        command = '''SELECT * FROM assignments WHERE lectureID = ?'''
        res = assig_cursor.execute(command, (self.teacher_id,))

        col_count = len(assig_cursor.description)
        self.assignments_table.setColumnCount(col_count)

        headers = [desc[0] for desc in assig_cursor.description]
        self.assignments_table.setHorizontalHeaderLabels(headers)
        self.assignments_table.setRowCount(0)

        for row_count, row_data in enumerate(res):
            self.assignments_table.insertRow(row_count)
            for column_count, data in enumerate(row_data):
                self.assignments_table.setItem(row_count, column_count, QTableWidgetItem(str(data)))

        self.assignments_table.move(100, 100)
        self.assignments_table.horizontalHeader().setStyleSheet(
            """
            QHeaderView::section {
                background-color: #154360;
                color: white;
                font-weight: bold;
            }
            """
        )
        self.assignments_table.setStyleSheet(
            """
            QTableWidget::item {
                background-color: #f0f0f0;
                color: #000000;
                padding: 5px;
                border: 1px solid #ddd;
            }
            QTableWidget::item:selected {
                background-color: #b0bec5;
                color: #000000;
            }
            """
        )

    def add_assignment_dialog(self):
        dialog = AddAssignmentDialog(self.teacher_id, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_assignments_data()


    def del_assign(self):
       
        selected_items = self.assignments_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Assignment Selected", "Please select an assignment to delete.")
            return
        row = selected_items[0].row()
        assignment_id_item = self.assignments_table.item(row, 0) 
        if assignment_id_item:
            assignment_id = assignment_id_item.text() 
            delete_assignment(assignment_id, self)
     
    def show_grades(self):
        
        assign_id= get_assignments_by_lecturer(self)
        if assign_id:
            self.grades_window = GradesWindow(assign_id)
            self.grades_window.show()
            self.grades_window.exec_()
     
    def make_image_circular(self, pixmap):

        size = min(pixmap.width(), pixmap.height())
        mask = QPixmap(size, size)
        mask.fill(Qt.transparent)

        path = QPainterPath()
        path.addEllipse(0, 0, size, size)

        painter = QPainter(mask)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        return mask   