import sqlite3
from student import Student
from PyQt5.QtWidgets import QMessageBox,QTableWidget,QTableWidgetItem
def get_connection():
    return sqlite3.connect('school.db')
##
def create_database():
    conn = get_connection()
    cursor = conn.cursor()

  
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            date_of_birth TEXT NOT NULL,
            date_of_enroll TEXT NOT NULL
        )
    ''')

   
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lecturers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            hierDate TEXT NOT NULL,
            department TEXT NOT NULL
        )
    ''')

   
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            lectureId INTEGER,
            FOREIGN KEY (lectureId) REFERENCES lecturers (id)
        )
    ''')

    # إنشاء جدول الدرجات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grade INTEGER NOT NULL DEFAULT 0,
            assignmentId INTEGER,
            studentId INTEGER,
            FOREIGN KEY (assignmentId) REFERENCES assignments (id),
            FOREIGN KEY (studentId) REFERENCES students (id)
        )
    ''')

    conn.commit()
    conn.close()
##
def add_student(student,self):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO students (first_name, last_name, email, date_of_birth, date_of_enroll)
        VALUES (?, ?, ?, ?, ?)
    ''', (student.Fname, student.Lname, student.email, student.DateOfBirth, student.DateOfEnroll))
    QMessageBox.information(self,"Added successfully" , "Student was added Sccessfully to database")    
    conn.commit()
    conn.close()
##
def add_lecturer(lecturer,self):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO lecturers (first_name, last_name, email, hierDate, department)
        VALUES (?, ?, ?, ?, ?)
    ''', (lecturer.Fname, lecturer.Lname, lecturer.email, lecturer.hierDate, lecturer.department))
    QMessageBox.information(self,"Added successfully" , "Teacher was added Sccessfully to database")    

    conn.commit()
    conn.close()
##  
def add_assignment(assignment,self):
    conn = get_connection()
    cursor = conn.cursor()
    if not assignment.name or not assignment.description :
            QMessageBox.critical(self, "Error", "Please fill in all fields.")
            return
    try:
        cursor.execute('''
        INSERT INTO assignments (name, description, lectureId)
        VALUES (?, ?, ?)
        ''',    (assignment.name, assignment.description, assignment.lectureId))
    
   
        cursor.execute('SELECT id FROM students')
        students = cursor.fetchall()
    
        for student_id in students:
            cursor.execute('''
            INSERT INTO grades (grade, assignmentId, studentId)
            VALUES (?, ?, ?)
        ''', (0, cursor.lastrowid, student_id[0]))
    
        
        QMessageBox.information(self, "Assignment Added", "Assignment successfully added.")
        conn.commit()
        self.accept()
    except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error adding assignment: {e}")    
        
##    
def search_std_by_birth_date(table ,birth_date, column_index ,self):
   
    
    conn = get_connection()
    cursor = conn.cursor()

    try:
       
        query = "SELECT * FROM students WHERE date_of_birth = ?"
        cursor.execute(query, (birth_date,))
        results = cursor.fetchall()

        if results:
            
            table.clearSelection()  

            row_count = table.rowCount()
            found = False

            
            for row in range(row_count):
                item = table.item(row, column_index)
                
               
                if item and item.text() == birth_date:
                    table.selectRow(row)  
                    found = True
                    break  

            if not found:
                QMessageBox.critical(self, "Error", f"Error Student Not found: {e}")   
        else:
            QMessageBox.critical(self,"Not found" ,f"No student found in the database with birth date: {birth_date}")

    except sqlite3.Error as e:
        print("An error occurred while querying the database:", e)

    finally:
       
        conn.close()
##
def update_grade(assignment_id, student_id, new_grade):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE grades
        SET grade = ?
        WHERE assignmentId = ? AND studentId = ?
    ''', (new_grade, assignment_id, student_id))
    
    conn.commit()
    conn.close()
##
def get_all_lecturers(self):
    db = get_connection()
    self.lecturer_table.setRowCount(0)
    lec_cursor = db.cursor()
    command = ''' SELECT * FROM lecturers ''' 
    res = lec_cursor.execute(command)
        
    column_count = len(lec_cursor.description)  
    self.lecturer_table.setColumnCount(column_count)
        
    headers = [desc[0] for desc in lec_cursor.description]
    self.lecturer_table.setHorizontalHeaderLabels(headers)
        
    for row_count, row_data in enumerate(res):
            self.lecturer_table.insertRow(row_count)
            for column_count, data in enumerate(row_data):
                self.lecturer_table.setItem(row_count, column_count, QTableWidgetItem(str(data)))
##
def get_all_students(self):
    db = get_connection()
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
##
def get_assignments_by_lecturer(self):
    selected_row = self.assignments_table.currentRow()

    if selected_row >= 0: 
        
                assignment_id_item = self.assignments_table.item(selected_row, 0)  
        
                if assignment_id_item:
                     assign_id = assignment_id_item.text()  
                     return assign_id
                else:
                        QMessageBox.warning(self, "Error", "Assignment ID not found in the selected row.")
                        return None
    else:
                QMessageBox.warning(self, "Error", "Please select an Assignment.")
                return None

##
def show(teacher_id):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Teacher Deleted")
        msg_box.setText(f"Teacher with ID {teacher_id} has been deleted.")
        msg_box.setStyleSheet("color:black")
        msg_box.exec_() 
##              
def delete_student(student_id,self):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
                cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
               
                cursor.execute('DELETE FROM grades WHERE studentId = ?', (student_id,))
                conn.commit()
                QMessageBox.information(self, "Student Deleted", f"Student with ID {student_id} has been deleted.")
                self.load_student_data()  
    except sqlite3.Error as e:
                QMessageBox.critical(self, "Error", f"Error deleting student: {e}")
    finally:
                conn.close()
                
##                
def del_lec(teacher_id,self):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
                cursor.execute('DELETE FROM lecturers WHERE id = ?', (teacher_id,))
               
                cursor.execute('DELETE FROM assignments WHERE lectureId = ?', (teacher_id,))
                conn.commit()
                show(teacher_id)
                self.load_teacher_data()  
    except sqlite3.Error as e:
                QMessageBox.critical(self, "Error", f"Error deleting teacher: {e}")
    finally:
                conn.close()


##
def search_by_input(table, input_value,self):
   
    if "@gmail.com" in input_value:
        email = input_value
        first_name = None
        last_name = None
    else:
       
        parts = input_value.split()
        if len(parts) == 2:
            first_name = parts[0]
            last_name = parts[1]
            email = None
        else:
            QMessageBox.critical(self, "Error", "Not valid name or email:")
            return


    get_lecturer_by_name_or_email(table, first_name, last_name, email)

##
def get_lecturer_by_name_or_email(table, first_name=None, last_name=None, email=None):
    conn = get_connection()
    cursor = conn.cursor()


    if (first_name and last_name) or email:
        command = 'SELECT id, first_name, last_name, email, hierDate, department FROM lecturers WHERE 1=1'
        params = []

       
        if first_name and last_name:
            command += ' AND first_name LIKE ? AND last_name LIKE ?'
            params.append(f'%{first_name}%')
            params.append(f'%{last_name}%')
        
       
        elif email:
            command += ' AND email LIKE ?'
            params.append(f'%{email}%')

       
        cursor.execute(command, params)
        rows = cursor.fetchall()

     
        if rows:
            
            table.clearSelection()
            

            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]} {row[2]}, Email: {row[3]}, Hierarchy Date: {row[4]}, Department: {row[5]}")
                
                # المرور عبر جميع الصفوف في الجدول وتحديد الصف المطابق الأول فقط
                row_count = table.rowCount()
                for i in range(row_count):
                    
                    item_first_name = table.item(i, 1)  # عمود الاسم الأول
                    item_last_name = table.item(i, 2)   # عمود الاسم الأخير
                    item_email = table.item(i, 3)      # عمود البريد الإلكتروني
                    if item_first_name and item_first_name.text() ==  params:
                        table.selectRow(row)
                    if (first_name and last_name and 
                        item_first_name and first_name.lower() in item_first_name.text().lower() and 
                        item_last_name and last_name.lower() in item_last_name.text().lower()) or \
                       (email and item_email and email.lower() in item_email.text().lower()):
                        table.selectRow(i)
                        break  
                break 
        else:
            print("Lecturer not found.")
    else:
        print("Please provide either both first and last names or an email address.")

    
    conn.close()
##
def get_student_between_two_dates(start_date, end_date,table,self):
    conn =get_connection()
    cursor = conn.cursor()


    query = '''
        SELECT id, first_name, last_name, email, date_of_birth
        FROM students
        WHERE date_of_birth BETWEEN ? AND ?
    '''
    cursor.execute(query, (start_date, end_date))

    rows = cursor.fetchall()

    if rows:       
        table.clearSelection()
        row_count = table.rowCount() 
        for student in rows:
            student_id = student[0]
            first_name = student[1]
            last_name = student[2]
     
            for row in range(row_count):
                item_id = table.item(row, 0)  
                item_first_name = table.item(row, 1)  
                item_last_name = table.item(row, 2)  

                if (item_id and item_first_name and item_last_name and
                    item_id.text() == str(student_id) and
                    item_first_name.text() == first_name and
                    item_last_name.text() == last_name):
                 
                    table.selectRow(row)

    else:
        QMessageBox.critical(self,"Error","No students found between the specified dates.")

    
    conn.close()
##
def delete_assignment(assignment_id,self):
    assignment_id = int(assignment_id)
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
                 cursor.execute('DELETE FROM assignments WHERE id = ?', (assignment_id,))
                 cursor.execute('DELETE FROM grades WHERE assignmentId = ?', (assignment_id,))
                 conn.commit()
                 show(assignment_id)
                 self.load_assignments_data()  
    except sqlite3.Error as e:
                QMessageBox.critical( "Error", f"Error deleting assignment: {e}")
    finally:
                conn.close()

def print_grades():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT students.first_name, students.last_name, assignments.name, grades.grade
        FROM grades
        JOIN students ON grades.studentId = students.id
        JOIN assignments ON grades.assignmentId = assignments.id
    ''')
    
    rows = cursor.fetchall()
    for row in rows:
        print(f"Student: {row[0]} {row[1]}, Assignment: {row[2]}, Grade: {row[3]}")
    
    conn.close()

def print_assignments_for_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT assignments.name, grades.grade
        FROM grades
        JOIN assignments ON grades.assignmentId = assignments.id
        WHERE grades.studentId = ?
    ''', (student_id,))
    
    rows = cursor.fetchall()
    for row in rows:
        print(f"Assignment: {row[0]}, Grade: {row[1]}")
    
    conn.close()

def print_students_by_birth_date(date_of_birth):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, first_name, last_name, email
        FROM students
        WHERE date_of_birth = ?
    ''', (date_of_birth,))
    
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]} {row[2]}, Email: {row[3]}")
    
    conn.close()

def add_students(students):
    conn = get_connection()
    cursor = conn.cursor()
    
   
    query = '''
        INSERT INTO students (first_name, last_name, email, date_of_birth, date_of_enroll)
        VALUES (?, ?, ?, ?, ?)
    '''
    
    try:
        cursor.executemany(query, students)
        conn.commit()
        print(f"{cursor.rowcount} students added successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()





