



from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
     QLineEdit, QTableWidget, QTableWidgetItem,  QVBoxLayout,  QPushButton, 
)
from PyQt5.QtWidgets import QMessageBox, QInputDialog

from PyQt5.QtGui import  QIcon
import sqlite3
from DBContext import update_grade


###############################
db = sqlite3.connect("school.db")
class GradesWindow(QtWidgets.QDialog):
    def __init__(self, assignmentId):
        super().__init__()
        self.setWindowTitle(f'Grades for Assignment ID: {str(assignmentId)}')
        self.setGeometry(450, 150, 800, 400)
        self.setWindowIcon(QIcon("icons/grades.jpg"))

        self.grades_table = QTableWidget(self)

        grades_cursor = db.cursor()
        command = '''SELECT * FROM grades WHERE assignmentId = ?'''
        res = grades_cursor.execute(command, (assignmentId,))
        
        col_count = len(grades_cursor.description)
        self.grades_table.setColumnCount(col_count)

        headers = [desc[0] for desc in grades_cursor.description]
        self.grades_table.setHorizontalHeaderLabels(headers)
        self.grades_table.setRowCount(0)

        for row_count, row_data in enumerate(res):
            self.grades_table.insertRow(row_count)
            for column_count, data in enumerate(row_data):
                self.grades_table.setItem(row_count, column_count, QTableWidgetItem(str(data)))

        # Add the table's style (header and row style)

        layout = QVBoxLayout()
        layout.addWidget(self.grades_table)

        # Add Grade Input and Update Button
        self.grade_input = QLineEdit(self)
        layout.addWidget(self.grade_input)

        update_button = QPushButton('Update Grade', self)
        update_button.clicked.connect(self.update_grades)
        layout.addWidget(update_button)

        # Add a button to open the 'Add New Grade' dialog
        add_grade_button = QPushButton('Add New Grade', self)
        add_grade_button.clicked.connect(self.open_add_grade_dialog)
        layout.addWidget(add_grade_button)

        self.setLayout(layout)

        self.assignmentId = assignmentId

    def update_grades(self):
        grade_value = self.grade_input.text()
        selected_row = self.grades_table.currentRow()

        if selected_row >= 0:
            student_id = self.grades_table.item(selected_row, 3).text()  
            try:
                update_grade(self.assignmentId, student_id, grade_value)
                QMessageBox.information(self, "Grade Updated", "Grade successfully updated.")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Error", f"Error updating grade: {e}")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a student from the table.")
    
    # Open the Add Grade Dialog
    def open_add_grade_dialog(self):
        dialog = AddGradeDialog(self.assignmentId)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.refresh_grades_table()

    def refresh_grades_table(self):
        """Refresh the grades table after adding or updating grades."""
        self.grades_table.setRowCount(0)  # Clear the table
        grades_cursor = db.cursor()
        command = '''SELECT * FROM grades WHERE assignmentId = ?'''
        res = grades_cursor.execute(command, (self.assignmentId,))

        for row_count, row_data in enumerate(res):
            self.grades_table.insertRow(row_count)
            for column_count, data in enumerate(row_data):
                self.grades_table.setItem(row_count, column_count, QTableWidgetItem(str(data)))
class AddGradeDialog(QtWidgets.QDialog):
    def __init__(self, assignmentId):
        super().__init__()
        self.assignmentId = assignmentId
        self.setWindowTitle("Add New Grade")
        self.setGeometry(500, 200, 400, 200)

        layout = QVBoxLayout()

        # Student ID input
        self.student_id_input = QLineEdit(self)
        self.student_id_input.setPlaceholderText("Enter Student ID")
        layout.addWidget(self.student_id_input)

        # Grade Value input
        self.grade_value_input = QLineEdit(self)
        self.grade_value_input.setPlaceholderText("Enter Grade Value")
        layout.addWidget(self.grade_value_input)

        # Assignment ID (already set, so just display it)
        self.assignment_id_display = QtWidgets.QLabel(f"Assignment ID: {self.assignmentId}")
        layout.addWidget(self.assignment_id_display)

        # Add button
        add_button = QPushButton("Add Grade", self)
        add_button.clicked.connect(self.add_grade)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def add_grade(self):
        student_id = self.student_id_input.text().strip()
        grade_value = self.grade_value_input.text().strip()

        if not student_id.isdigit() or not grade_value.isdigit():
            QMessageBox.warning(self, "Input Error", "Student ID and Grade Value must be numbers.")
            return

        try:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO grades (assignmentId, studentId, grade) VALUES (?, ?, ?)",
                (self.assignmentId, student_id, grade_value)
            )
            db.commit()
            QMessageBox.information(self, "Success", "Grade added successfully!")
            self.accept()  # Close the dialog
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Failed to add grade: {e}")
