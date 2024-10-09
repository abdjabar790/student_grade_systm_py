
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy
)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QPainterPath, QPainter, QIcon
import sqlite3

from student_window import StudentWindow
from teacher_window import TeacherWindow

 
###############################

db=sqlite3.connect("school.db")

class UI_MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Student Grades System')
        self.setGeometry(450, 150, 1000, 800)
        self.setWindowIcon(QIcon("icons/system.png"))
        self.setStyleSheet("background-color:black; padding:0; margin:0")

       
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0) 

        
        self.welcomelabel = QLabel("Welcome to the Student Grades System", self)
        self.welcomelabel.setGeometry(250, 0, 800, 100)
        font = QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(True)
        self.welcomelabel.setFont(font)
        self.welcomelabel.setStyleSheet("color: white; background-color: #125c83;")
        self.welcomelabel.setAlignment(Qt.AlignCenter)
        self.setContentsMargins(0, 0, 0, 0)

        
        self.sidebar_widget = QWidget(self)
        self.sidebar_widget.setStyleSheet("background-color: #054359;")
        self.sidebar_widget.setFixedWidth(250)
        self.sidebar_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)  
        
        sidebar_content = QVBoxLayout(self.sidebar_widget)
        sidebar_content.setContentsMargins(0, 0, 0, 0)  
        
        
        top_layout = QVBoxLayout()
        student_image = QLabel(self)
        pixmap = QPixmap('images/programmerjpg.jpg').scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        circular_pixmap = self.make_image_circular(pixmap)
        student_image.setPixmap(circular_pixmap)
        top_layout.addWidget(student_image, alignment=Qt.AlignCenter)

        sidebar_label = QLabel("", self)
        sidebar_label.setStyleSheet('color: white; font-size: 18px;')
        top_layout.addWidget(sidebar_label, alignment=Qt.AlignCenter)
        
        sidebar_content.addLayout(top_layout)
        sidebar_content.addSpacing(30)

        student_button = QPushButton('  Student List', self)
        student_button.setIcon(QIcon('icons/student.jpg'))
        student_button.setStyleSheet('color: white; font-size: 20px;')
        student_button.setFlat(True)
        student_button.setFixedHeight(60)
        student_button.clicked.connect(self.open_student_window)

        teacher_button = QPushButton('  Teacher List', self)
        teacher_button.setIcon(QIcon('icons/teacher.png'))
        teacher_button.setStyleSheet('color: white; font-size: 20px;')
        teacher_button.setFlat(True)
        teacher_button.setFixedHeight(150)
        teacher_button.clicked.connect(self.open_teacher_window)

        exit_button = QPushButton('  Exit', self)
        exit_button.setIcon(QIcon('icons/exit.jpg'))
        exit_button.setStyleSheet('color: white; font-size: 20px;')
        exit_button.setFlat(True)
        exit_button.setFixedHeight(100)
        exit_button.clicked.connect(exit)

        sidebar_content.addWidget(student_button)
        sidebar_content.addWidget(teacher_button)
        sidebar_content.addWidget(exit_button)
        sidebar_content.addStretch()

        main_layout.addWidget(self.sidebar_widget)

        content_layout = QVBoxLayout()
        sys_image = QLabel(self)
        pxmp = QPixmap('images/student.jpg').scaled(600, 330, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        sys_image.setPixmap(pxmp)
        content_layout.addWidget(sys_image, alignment=Qt.AlignCenter)

        main_layout.addLayout(content_layout)
    
        self.setLayout(main_layout)
        
    def open_student_window(self):
        self.student_window = StudentWindow()
        self.student_window.show()
        self.close()

    def open_teacher_window(self):
        self.teacher_window = TeacherWindow()
        self.teacher_window.show()   
        self.close()  
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


