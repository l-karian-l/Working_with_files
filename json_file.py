import json
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5 import uic

class JsonWindow(QtWidgets.QDialog):
    def __init__(self):
        super(JsonWindow, self).__init__()
        uic.loadUi('JSON_FILE.ui', self)

        self.create_info = ""
        home_path = os.path.expanduser("~")

        self.lE_create_filepath.setReadOnly(True) # задача "Создать файл"
        self.lE_create_filepath.setText(home_path)
        self.lE_write_text.setReadOnly(True) # задача "Записать в файл"
        self.lE_write_text2.setReadOnly(True)
        self.lE_read_filepath.setReadOnly(True) # задача "Прочитать файл"
        self.lE_delete_filepath.setReadOnly(True) # задача "Удалить файл" 

        self.btn_create.clicked.connect(self.create_json_file) # Создание файла
        self.cB_create.stateChanged.connect(self.cB_open) # Состояние чек бокса
        self.tB_create_filepath.clicked.connect(lambda: self.all_dir(self.lE_create_filepath))

    #Выбор директории
    def all_dir(self, line_edit):
        try:
            path_dir = QFileDialog.getExistingDirectory(self, "Выберите директорию", self.home_path)
            if path_dir:
                line_edit.setText(path_dir)
        except Exception as e:
            self.show_error(f"Ошибка при выборе директории: {e}")

    
    
    # 1. Создание файла JSON с использованием данных, введенных пользователем
    def create_json_file(self):
        try:
            author = self.lE_write_text.text().strip()
            picture = self.lE_write_text2.text().strip()
            path = self.lE_create_filepath.text().strip()
            name = self.lE_create_name.text().strip()

            if not name:
                self.show_error("Не задано имя файла.")
                return
            
            filepath = os.path.join(path, f"'{name}'.json") 

            data = {}
            if author or picture:
                data = {
                    "authors": author ,
                    "paintings": picture,
                }
            
            self.write_json_file(filepath, data)
        
        except Exception as e:
            self.show_error(f"Ошибка при создании файла: {e}")

    def write_json_file(self, filepath, data):
            # Сериализация объекта в JSON и запись в файл
        try:
            with open(filepath, "w", encoding="utf-8") as json_file:
                json.dump(data, json_file, indent=4, ensure_ascii=False)
                self.log_action(f"Файл '{filepath}' успешно создан.")
                self.lE_write_text.setText("")
                self.lE_write_text2.setText("")
        except Exception as e:
            self.show_error(f"Не удалось создать файл: {e}")       

    def cB_open(self):
        # Проверяем состояние чекбокса
        if self.cB_create.isChecked():
            self.lE_write_text.setReadOnly(False)
            self.lE_write_text2.setReadOnly(False)
        else:
            self.lE_write_text.setText("")
            self.lE_write_text2.setText("")
            self.lE_write_text.setReadOnly(True)
            self.lE_write_text2.setReadOnly(True)

    
    # Отображает сообщение об ошибке в виде всплывающего окна.
    def show_error(self, message):
        error1 = QMessageBox()
        error1.setWindowTitle("Ошибка")
        error1.setText(message)
        error1.setIcon(QMessageBox.Icon.Warning)
        error1.setStandardButtons(QMessageBox.StandardButton.Ok)
        #error1.buttonClicked.connect(self.popup)
        error1.exec_() 
    
    # Добавляет сообщение об операции в текстовое поле `tE_infa`.
    def log_action(self, message):
        self.create_info += message + "\n"
        self.tE_infa.setPlainText(self.create_info)

    #Для выхода
    def exit(self):
        from firs_win import FirstWindow
        self.Login = FirstWindow()
        self.Login.show()
        self.hide()



