from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from file_info import InfoWindow
from work_file import FileWindow
from json_file import JsonWindow
from PyQt5 import uic
import sys


class FirstWindow(QtWidgets.QDialog):
        def __init__(self):
            super(FirstWindow, self).__init__()
            uic.loadUi('FIRST_WIN.ui', self)

            self.btn_infa.clicked.connect(self.info)
            self.btn_file.clicked.connect(self.file)
            self.btn_json.clicked.connect(self.json_f)


        def info(self):
            self.info_file = InfoWindow()
            self.info_file.show()
            self.hide()
        
        def file(self):
            self.work_file = FileWindow()
            self.work_file.show()
            self.hide()

        def json_f(self):
            self.jsn_file = JsonWindow()
            self.jsn_file.show()
            self.hide()





if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        Login = FirstWindow()
        Login.show()
        sys.exit(app.exec_())
