from ast import Lambda
from ctypes import alignment
from msilib import Dialog
import sys
from tkinter import messagebox
from tkinter.ttk import Style
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QLineEdit, QMainWindow, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy
)
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QPainterPath, QPainter, QIcon
import sqlite3
from DBContext import del_lec, get_all_lecturers, get_lecturer_by_name_or_email, search_by_input
from add_teacher import AddTeacherWindow
from assignment_window import AssignmentsWindow


 
###############################

db=sqlite3.connect("school.db")
class TeacherWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Teacher List')
        self.setGeometry(450, 150, 1000, 600)
        self.setStyleSheet(" color: white;")
        self.setWindowIcon(QIcon("icons/system.png"))
    
        main_layout = QHBoxLayout(self)
        sidebar = QWidget(self)
        sidebar.setStyleSheet("background-color: #21618c ;")  
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar.setMaximumWidth(self.width() * 0.30)
        
        tech_image = QLabel(self)
        txmp = QPixmap('icons/tech.png').scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        circlstd = self.make_image_circular(txmp)
        tech_image.setPixmap(circlstd)       
        sidebar_layout.addWidget(tech_image , alignment=Qt.AlignTop | Qt.AlignCenter)
        
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText('Search by name or email')
        self.search_input.setStyleSheet("background-color: #e8f0f2; color: black; border-radius: 5px; padding: 5px;")
        
        self.search_button = QPushButton('Search Teacher', self)
        self.search_button.setStyleSheet("background-color: #57A6A1;  ; color: white; border-radius: 5px; padding: 10px;")
        self.search_button.clicked.connect(self.search_teacher)
        self.add_lect =QPushButton("Add New Teacher")
        self.add_lect.setStyleSheet("background-color: #57A6A1;  ; color: white; border-radius: 5px; padding: 10px;")
        self.add_lect.clicked.connect(self.add_lecturer)
        self.ref_btn = QPushButton("Refresh table", self)
        self.ref_btn.setStyleSheet("background-color: orange; color: white; border-radius: 5px; padding: 10px;")
        self.ref_btn.clicked.connect(self.load_teacher_data)
        
        self.assignment_button = QPushButton('Open Assignments', self)
        self.assignment_button.setStyleSheet("background-color: green;  ; color: white; border-radius: 5px; padding: 10px;")
        self.assignment_button.clicked.connect(self.open_assignments_window_by_teacher_id)
        
        self.delete_button = QPushButton('Delete Teacher', self)
        self.delete_button.setStyleSheet("background-color: red; color: white; border-radius: 5px; padding: 10px;")
        self.delete_button.clicked.connect(self.del_lect)  
        
        tech_lbl = QLabel('Search or delete Teacher', self)
        tech_lbl.setStyleSheet("color : white; font-size:22;font-weight: bold;")
        
        sidebar_layout.addWidget(tech_lbl, alignment=Qt.AlignCenter)
        sidebar_layout.addSpacing(30)
        sidebar_layout.addWidget(self.search_input)
        sidebar_layout.addSpacing(30)
        sidebar_layout.addWidget(self.search_button)
        sidebar_layout.addSpacing(30)
        sidebar_layout.addWidget(self.add_lect)
        sidebar_layout.addSpacing(30)
        sidebar_layout.addWidget(self.assignment_button)
        sidebar_layout.addSpacing(30)
        sidebar_layout.addWidget(self.ref_btn)
        sidebar_layout.addSpacing(30)
        sidebar_layout.addWidget(self.delete_button)
        sidebar_layout.addStretch()
        
        main_layout.addWidget(sidebar)

        self.lecturer_table = QTableWidget(self)
        
       
        self.load_teacher_data()
        
        main_layout.addWidget(self.lecturer_table)
        self.setLayout(main_layout)
    
    def load_teacher_data(self):
        get_all_lecturers(self)
        
        
        header = self.lecturer_table.horizontalHeader()
        header.setStyleSheet(
            """
            QHeaderView::section {
                background-color: #154360; 
                font-weight: bold;                
            }
            """
        )
      
        self.lecturer_table.setStyleSheet(
            """
            QTableWidget::item {
                background-color: #f0f0f0; 
                color: #000000;  
                padding: 5px;  
                border: 1px solid #ddd; 
            }
            QTableWidget::item:selected {
                background-color: #b0bec5;                   
            }
            """
        )
    
    def del_lect(self):
       
        selected_items = self.lecturer_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Teacher Selected", "Please select a teacher to delete.")
            return
        
        row = selected_items[0].row()
        teacher_id_item = self.lecturer_table.item(row, 0)  
        if teacher_id_item:
            teacher_id = teacher_id_item.text()  
            del_lec(teacher_id,self)

    def get_selected_teacher_id(self):
  
        selected_row = self.lecturer_table.currentRow()

        if selected_row >= 0: 
       
                teacher_name = self.lecturer_table.item(selected_row, 1).text()  

                lec_cursor = db.cursor()
                query = "SELECT id FROM lecturers WHERE first_name = ?"
                lec_cursor.execute(query, (teacher_name,))
                result = lec_cursor.fetchone()

                if result:
                        teacher_id = result[0]
                        return teacher_id
                else:
                        self.show_error()
                        return None
    def open_assignments_window_by_teacher_id(self):
    
        teacher_id = self.get_selected_teacher_id()

        if teacher_id:
                assignments_window = AssignmentsWindow(teacher_id)
                assignments_window.show()
                assignments_window.exec_()
        else:
              self.show_error()
    
    def search_teacher(self):
         search_by_input(self.lecturer_table,   self.search_input.text())    
    def add_lecturer(self):
        self.t = AddTeacherWindow()
        self.t.show()
    def show_error(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Error")
        msg_box.setText("Teacher not found in the database.")
        msg_box.setStyleSheet("color:black")
        msg_box.exec_()       
    
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
  