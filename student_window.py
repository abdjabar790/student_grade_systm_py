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
from DBContext import delete_student, get_student_between_two_dates,search_std_by_birth_date
from add_student import AddStudentWindow



###############################

db=sqlite3.connect("school.db")
class StudentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student List')
        self.setGeometry(450, 150, 1200, 600)
        self.setStyleSheet("background-color: #f1f1f1; color: black;")  
        self.setWindowIcon(QIcon("icons/system.png"))
       
        main_layout = QHBoxLayout(self)

        sidebar = QWidget(self)
        sidebar.setStyleSheet("background-color: #054359 ;")  
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar.setMaximumWidth(280)
        
        self.inp1 = QLineEdit(self)
        self.inp2 = QLineEdit(self)
        self.inp1.setPlaceholderText("Enter first date")
        self.inp2.setPlaceholderText("Enter second date")
        self.inp1.setStyleSheet("background-color: #e8f0f2; color: black; border-radius: 5px; padding: 5px;")
        self.inp2.setStyleSheet("background-color: #e8f0f2; color: black; border-radius: 5px; padding: 5px;")
        inps = QHBoxLayout()
        inps.addWidget(self.inp1)
        inps.addSpacing(10)
        inps.addWidget(self.inp2)
        
        
        std_image = QLabel(self)
        pyxmp = QPixmap('icons/students.jpg').scaled(75, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        circlstd = self.make_image_circular(pyxmp)
        std_image.setPixmap(circlstd)       
        sidebar_layout.addWidget(std_image , alignment=Qt.AlignTop | Qt.AlignCenter)
        
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText('Search Student')
        self.search_input.setStyleSheet("background-color: #e8f0f2; color: black; border-radius: 5px; padding: 5px;")
        
        self.search_button = QPushButton('Search Student by birth date', self)
        self.search_button.setStyleSheet("background-color: #57A6A1; color: white; border-radius: 5px; padding: 10px;")
        self.search_button.clicked.connect(self.search_std_by_birth)
        
        self.search_button_two_dates = QPushButton('Search Student between two dates', self)
        self.search_button_two_dates.setStyleSheet("background-color: #2e86c1; color: white; border-radius: 5px; padding: 10px;")
        self.search_button_two_dates.clicked.connect(self.search_by_two_dates)
        
        self.add_std = QPushButton('Add student' ,self)
        self.add_std.setStyleSheet("background-color: green; color: white; border-radius: 5px; padding: 10px;")
        self.add_std.clicked.connect(self.add_student)
        
        self.ref_btn = QPushButton("Refresh table", self)
        self.ref_btn.setStyleSheet("background-color: orange; color: white; border-radius: 5px; padding: 10px;")
        self.ref_btn.clicked.connect(self.load_student_data)
        
        self.delete_button = QPushButton('Delete Student', self)
        self.delete_button.setStyleSheet("background-color: red; color: white; border-radius: 5px; padding: 10px;")
        self.delete_button.clicked.connect(self.del_std) 
        
        std_label = QLabel('Search or delete Student', self)
        std_label.setStyleSheet("color : white; font-size:22;font-weight: bold;")
        
        sidebar_layout.addWidget(std_label, alignment=Qt.AlignCenter)
        sidebar_layout.addSpacing(30) 
        sidebar_layout.addWidget(self.search_input)
        sidebar_layout.addSpacing(30) 
        sidebar_layout.addWidget(self.search_button)
        sidebar_layout.addSpacing(30)
        sidebar_layout.addLayout(inps)
        sidebar_layout.addSpacing(20)
        sidebar_layout.addWidget(self.search_button_two_dates)
        sidebar_layout.addSpacing(30)
        sidebar_layout.addWidget(self.add_std)
        sidebar_layout.addSpacing(30)
        sidebar_layout.addWidget(self.ref_btn)
        sidebar_layout.addSpacing(30)
        sidebar_layout.addWidget(self.delete_button)
        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)
        
        self.student_table = QTableWidget(self)

       
        self.load_student_data()
        
        main_layout.addWidget(self.student_table)
        self.setLayout(main_layout)
    
    def load_student_data(self):
        
        self.student_table.setRowCount(0)
        std_cursor = db.cursor()
        command = ''' SELECT * FROM students ''' 
        res = std_cursor.execute(command)
        
        column_count = len(std_cursor.description)  
        self.student_table.setColumnCount(column_count)
        
        headers = [desc[0] for desc in std_cursor.description]
        self.student_table.setHorizontalHeaderLabels(headers)
        
        for row_count, row_data in enumerate(res):
            self.student_table.insertRow(row_count)
            for column_count, data in enumerate(row_data):
                self.student_table.setItem(row_count, column_count, QTableWidgetItem(str(data)))
        
        header = self.student_table.horizontalHeader()
        header.setStyleSheet(
            """
            QHeaderView::section {
                background-color: #154360; 
                color: white;  
                font-weight: bold;  
            }
            """
        )
        
        self.student_table.setStyleSheet(
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
    
    def del_std(self):
       
        selected_items = self.student_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Student Selected", "Please select a student to delete.")
            return
        
        row = selected_items[0].row()
        student_id_item = self.student_table.item(row, 0)  
        if student_id_item:
            student_id = student_id_item.text()  
            delete_student(student_id,self)

    def search_std_by_birth(self):
            search_std_by_birth_date(self.student_table, self.search_input.text().lower().strip() ,4,self)
    def search_by_two_dates(self):
        fd = self.inp1.text()
        sd = self.inp2.text()
        get_student_between_two_dates(fd,sd,self.student_table,self)
    def add_student(self):
        self.st = AddStudentWindow()
        self.st.show()
        
         
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