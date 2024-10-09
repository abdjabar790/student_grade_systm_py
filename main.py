import sys
from DBContext import create_database
from MainWindow import UI_MainWindow
from PyQt5.QtWidgets import QApplication
def main():
    create_database() 
    app = QApplication(sys.argv)
    main_window = UI_MainWindow() 
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()