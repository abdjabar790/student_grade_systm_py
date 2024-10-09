from ast import Lambda
from ctypes import alignment
from msilib import Dialog
import sys
from tkinter import messagebox
from tkinter.ttk import Style
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
     QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy
)
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QPixmap, QPainterPath, QPainter, QIcon
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QDateEdit, QSizePolicy, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from DBContext import add_lecturer


from lecturer import Lecturer  


class AddTeacherWindow(QWidget):  
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Teacher")  
        self.setGeometry(450, 150, 1000, 800)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.welcomelabel = QLabel("Add Teacher", self)  
        self.welcomelabel.setGeometry(325, 0, 800, 125)
        font = QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(True)
        self.welcomelabel.setFont(font)
        self.welcomelabel.setStyleSheet("color: white; background-color: #7dcea0")
        self.welcomelabel.setAlignment( Qt.AlignCenter)
        

        self.sidebar_widget = QWidget(self)
        self.sidebar_widget.setStyleSheet("background-color:#0b5345 ;")
        self.sidebar_widget.setFixedWidth(325)
        self.sidebar_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)  
        
        sidebar_content = QVBoxLayout(self.sidebar_widget)
        sidebar_content.setContentsMargins(0, 0, 0, 0)  
        
        
        top_layout = QVBoxLayout()
        

        sidebar_label = QLabel("", self)
        
        top_layout.addWidget(sidebar_label, alignment=Qt.AlignCenter)
        
        sidebar_content.addLayout(top_layout)
        sidebar_content.addSpacing(30)

        add_btn = QPushButton('  Add to database', self)
        add_btn.setIcon(QIcon('icons/teacher.jpg')) 
        add_btn.setStyleSheet("color:white ;font-size:20px;font-Weight:bold;font-family:arial ")
        add_btn.setFlat(True)
        add_btn.setFixedHeight(75)
        add_btn.clicked.connect(self.add_teacher)  

        clear_btn = QPushButton('  clear current data', self)
        clear_btn.setIcon(QIcon('icons/clear.png'))  
        clear_btn.setStyleSheet("color:white ;font-size:20px;font-Weight:bold;font-family:arial ")
        clear_btn.setFlat(True)
        clear_btn.setFixedHeight(75)
        clear_btn.clicked.connect(self.clear_current)
        
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine) 
        line2 = QtWidgets.QFrame()
        line2.setFrameShape(QtWidgets.QFrame.HLine) 
        line3 = QtWidgets.QFrame()
        line3.setFrameShape(QtWidgets.QFrame.HLine) 
        line4 = QtWidgets.QFrame()
        line4.setFrameShape(QtWidgets.QFrame.HLine) 
        
        home_btn = QPushButton('  back Main Page ', self)
        home_btn.setIcon(QIcon('icons/exit.jpg'))
        home_btn.setStyleSheet("color:white ;font-size:20px;font-Weight:bold;font-family:arial ")
        home_btn.setFlat(True)
        home_btn.setFixedHeight(100)
        # home_btn.clicked.connect(self.back_home)

        exit_button = QPushButton('  Exit ', self)
        exit_button.setIcon(QIcon('icons/exit.jpg'))
        exit_button.setStyleSheet('color:lightgreen ;font-size:20px;font-Weight:bold;font-family:arial ')
        exit_button.setFlat(True)
        exit_button.setFixedHeight(75)
        exit_button.clicked.connect(exit)
        
        teacher_label = QLabel("Teacher System")  
        teacher_label.setStyleSheet('color: lightgreen; font-size: 25px;')
        
        sidebar_content.addWidget(teacher_label, alignment= Qt.AlignCenter)
        sidebar_content.addSpacing(20)
        sidebar_content.addWidget(line3)
        sidebar_content.addSpacing(100)
        sidebar_content.addWidget(add_btn)
        sidebar_content.addWidget(line2)
        sidebar_content.addWidget(clear_btn)
        sidebar_content.addWidget(line)
        sidebar_content.addWidget(home_btn)
        sidebar_content.addSpacing(250)
        sidebar_content.addWidget(line4)
        sidebar_content.addWidget(exit_button)
        sidebar_content.addStretch()

        main_layout.addWidget(self.sidebar_widget , alignment=Qt.AlignLeft )
        css = """
    QLineEdit {
         background-color: rgba(255, 255, 255, 0.6);;
        color: #000000;
        border: 1px solid #cccccc;
        border-radius: 10px;
        font-size: 14px;
        padding: 5px;
    }
    QLineEdit:focus {
        border: 1px solid #007BFF;
        background-color: #e6f7ff;
    }
    QLineEdit::placeholder {
        color: #999999;
        font-style: italic;
    }
"""
        form_layout = QVBoxLayout()
        form_layout.addSpacing(200)
        name_label_layout = QHBoxLayout()
        name_input_layout = QHBoxLayout()
        
        first_name_label = QLabel("First Name")
        
        first_name_label.setStyleSheet("color:#0b5345 ;font-size:15px;font-Weight:bold;font-family:arial ")
        
        self.first_name_input = QLineEdit(self)
        self.first_name_input.setFixedHeight(30)
        self.first_name_input.setFixedWidth(200)
        self.first_name_input.setStyleSheet(css)
      
        
        last_name_label = QLabel("Last Name")
        last_name_label.setFont(QFont("Arial", 12))
        last_name_label.setStyleSheet("color:#0b5345 ;font-size:15px;font-Weight:bold;font-family:arial ")
        self.last_name_input = QLineEdit(self)
        self.last_name_input.setStyleSheet(css)
        self.last_name_input.setFixedHeight(30)
        self.last_name_input.setFixedWidth(200)
       
        name_label_layout.addWidget(first_name_label, alignment=Qt.AlignCenter| Qt.AlignLeft )
        name_label_layout.addWidget(last_name_label, alignment=Qt.AlignCenter| Qt.AlignLeft)
        
        name_input_layout.addWidget(self.first_name_input, alignment=Qt.AlignCenter| Qt.AlignLeft)
        name_input_layout.addWidget(self.last_name_input, alignment=Qt.AlignCenter| Qt.AlignLeft)
        form_layout.addLayout(name_label_layout)
        form_layout.addLayout(name_input_layout)
      
        
        
        email_date_label = QHBoxLayout()
        email_date_input = QHBoxLayout()
        email_label = QLabel("Email")
        email_label.setFont(QFont("Arial", 12))
        email_label.setStyleSheet("color:#0b5345 ;font-size:15px;font-Weight:bold;font-family:arial ")
        self.email_input = QLineEdit(self)
        self.email_input.setFixedHeight(30)
        self.email_input.setFixedWidth(200)
        self.email_input.setStyleSheet(css)
        email_date_label.addWidget(email_label, alignment=Qt.AlignCenter| Qt.AlignLeft)
        email_date_input.addWidget(self.email_input, alignment=Qt.AlignCenter| Qt.AlignLeft)
       
        
        birth_date_label = QLabel(" Hier_Date")
        birth_date_label.setFont(QFont("Arial", 12))
        birth_date_label.setStyleSheet("color:#0b5345 ;font-size:15px;font-Weight:bold;font-family:arial ")
        self.birth_date_input = QLineEdit(self)
        self.birth_date_input.setFixedHeight(30)
        self.birth_date_input.setFixedWidth(200)
        self.birth_date_input.setStyleSheet(css)
        email_date_label.addWidget(birth_date_label, alignment=Qt.AlignCenter| Qt.AlignLeft)
        email_date_input.addWidget(self.birth_date_input, alignment=Qt.AlignCenter| Qt.AlignLeft)
        
        form_layout.addLayout(email_date_label)
        form_layout.addLayout(email_date_input)
        
        enroll_date_label_layout = QHBoxLayout()
        enroll_date_input_input = QHBoxLayout()
        enroll_date_label = QLabel("Department")
        enroll_date_label.setFont(QFont("Arial", 12))
        enroll_date_label.setStyleSheet("color:#0b5345 ;font-size:15px;font-Weight:bold;font-family:arial ")
        self.enroll_date_input = QLineEdit(self)
        self.enroll_date_input.setFixedHeight(30)
        self.enroll_date_input.setFixedWidth(200)
        self.enroll_date_input.setStyleSheet(css)
        enroll_date_label_layout.addWidget(enroll_date_label, alignment=Qt.AlignCenter| Qt.AlignLeft)
        enroll_date_input_input.addWidget(self.enroll_date_input, alignment=Qt.AlignCenter| Qt.AlignLeft)
        form_layout.addLayout(enroll_date_label_layout)
        form_layout.addLayout(enroll_date_input_input)
        btn_layout = QHBoxLayout()
        
        
        btn = QPushButton("Teachers Table" ) 
        btn.setFixedHeight(80)
        btn.setFixedWidth(400)
        # btn.clicked.connect(self.open_teacher_table)  
        btn.setStyleSheet("""
        QPushButton{
            background-color: rgba(255, 255, 255, 0.8); 
        color: #0b5345;
        border: 1px solid #cccccc;
        border-radius: 33px;
        font-size: 19px;
        padding: 5px;
        font-Weight:bold;
        font-family:arial
    }
    QPushButton:focus {
        border: 1px solid #007BFF;
        background-color: rgba(230, 247, 255, 0.8);
    }
    QPushButton::placeholder {
        color: #999999;
        font-style: italic;
    }
""")
        btn_layout.addWidget(btn, alignment=Qt.AlignCenter | Qt.AlignLeft )
        form_layout.addSpacing(200)
        form_layout.addLayout(btn_layout)
        form_layout.addSpacing(100)
        main_layout.addLayout(form_layout)
        
        
        self.setLayout(main_layout)
        
    def add_teacher(self):
        fn = self.first_name_input.text()
        ln = self.last_name_input.text()
        em = self.email_input.text()
        hd = self.birth_date_input.text()
        dep=self.enroll_date_input.text()
        self.teacher = Lecturer(fn,ln,em,hd,dep)
        add_lecturer(self.teacher,self)  
    
    def clear_current(self):
        fn = self.first_name_input.clear()
        ln = self.last_name_input.clear()
        em = self.email_input.clear()
        bd = self.birth_date_input.clear()
        doe=self.enroll_date_input.clear()
    
    # def back_home(self):
    #     self.main = UI_MainWindow()
    #     self.main.show()

# app = QApplication([])
# window = AddTeacherWindow()
# window.show()
# app.exec_()
