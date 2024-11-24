import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5 import uic

class FileWindow(QtWidgets.QDialog):
    def __init__(self):
        super(FileWindow, self).__init__()
        uic.loadUi('WORK_FILE.ui', self)

        self.create_info = ""
        home_path = os.path.expanduser("~")
    
    # Функционал  
        # Первоначальная настройка lineedit
        self.lE_create_filepath.setReadOnly(True) # задача "Создать файл"
        self.lE_create_filepath.setText(home_path)
        
        self.lE_write_filepath.setReadOnly(True) # задача "Записать в файл строку"
        self.lE_read_filepath.setReadOnly(True) # задача "Прочитать файл"
        self.lE_delete_filepath.setReadOnly(True) # задача "Удалить файл" 

        # Подключение кнопок к методам
        self.btn_create.clicked.connect(self.create_file) # Создание файла
        self.tB_create_filepath.clicked.connect(lambda: self.all_dir(self.lE_create_filepath))
        self.btn_write.clicked.connect(self.write_file)  # Записать в файл строку
        self.tB_write_filepath.clicked.connect(lambda: self.all_file(self.lE_write_filepath)) 
        self.btn_read.clicked.connect(self.read_file)  # Прочитать файл
        self.tB_read_filepath.clicked.connect(lambda: self.all_file(self.lE_read_filepath)) 
        self.btn_delete.clicked.connect(self.delete_file)  # Удалить файл
        self.tB_delete_filepath.clicked.connect(lambda: self.all_file(self.lE_delete_filepath))
        self.btn_exit.clicked.connect(self.exit)  # Выход 
        
    #Выбор файла
    def all_file(self, line_edit):
        pathfile, _ = QFileDialog.getOpenFileName(self, "Выберите файл")
        if pathfile:  # Проверяем, что файл выбран
            line_edit.setText(pathfile)

    #Выбор директории
    def all_dir(self, line_edit):
        try:
            path_dir = QFileDialog.getExistingDirectory(self, "Выберите директорию", self.home_path)
            if path_dir:
                line_edit.setText(path_dir)
        except Exception as e:
            self.show_error(f"Ошибка при выборе директории: {e}")

    # Создает пустой файл
    def create_file(self): 
        path = self.lE_create_filepath.text()
        name = self.lE_create_name.text()

        if not name:
            self.show_error("Не задано имя файла.")
            return
        
        filepath = os.path.join(path, f"'{name}'.txt") 

        try:
            with open(filepath, 'w') as file:
                pass
            self.log_action(f"Файл '{filepath}' успешно создан.")
        except Exception as e:
            self.show_error(f"Не удалось создать файл: {e}")


    # Записать в файл строку
    def write_file(self): 
        filepath = self.lE_write_filepath.text()
        text = self.lE_write_text.text()
        text += "\n"

        if not filepath:
            self.show_error("Не задан путь для файла.")
            return
        if not text:
            self.show_error("Введите текст для записи.")
            return

        try:
            with open(filepath, 'a') as file:
                file.write(text)
            self.log_action(f"Строка '{text}' записана в файл '{filepath}'.")
        except Exception as e:
            self.show_error(f"Ошибка записи в файл: {e}")
         
    #Прочитать файл
    def read_file(self): 
        filepath = self.lE_read_filepath.text()

        if not filepath:
            self.show_error("Не указан путь для файла.")
            return

        if not os.path.exists(filepath):
            self.show_error("Файл не существует.")
            return

        try:
            with open(filepath, 'r') as file:
                content = file.read()
            self.log_action(f"Содержимое файла '{filepath}':\n{content}")
        except Exception as e:
            self.show_error(f"Ошибка чтения файла: {e}")

    # Удаляет указанный файл
    def delete_file(self):
        filepath = self.lE_delete_filepath.text()

        if not filepath:
            self.show_error("Не указан путь для файла.")
            return

        if not os.path.exists(filepath):
            self.show_error("Файл не существует.")
            return

        try:
            os.remove(filepath)
            self.log_action(f"Файл '{filepath}' успешно удален.")
        except Exception as e:
            self.show_error(f"Ошибка удаления файла: {e}")
            
    # Добавляет сообщение об операции в текстовое поле `tE_infa`.
    def log_action(self, message):
        self.create_info += message + "\n"
        self.tE_infa.setPlainText(self.create_info)

    # Отображает сообщение об ошибке в виде всплывающего окна.
    def show_error(self, message):
        error1 = QMessageBox()
        error1.setWindowTitle("Ошибка")
        error1.setText(message)
        error1.setIcon(QMessageBox.Icon.Warning)
        error1.setStandardButtons(QMessageBox.StandardButton.Ok)
        #error1.buttonClicked.connect(self.popup)
        error1.exec_()

    #Для выхода
    def exit(self):
        from firs_win import FirstWindow
        self.Login = FirstWindow()
        self.Login.show()
        self.hide()
