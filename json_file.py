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
        self.home_path = os.path.expanduser("~")

        self.lE_create_filepath.setReadOnly(True) # задача "Создать файл"
        self.lE_create_filepath.setText(self.home_path)
        self.lE_write_text.setReadOnly(True) 
        self.lE_write_text2.setReadOnly(True)
        self.lE_write_key1.setReadOnly(True)
        self.lE_write_filepath.setReadOnly(True) # задача "Записать в файл"
        self.lE_read_filepath.setReadOnly(True) # задача "Прочитать файл"
        self.lE_delete_filepath.setReadOnly(True) # задача "Удалить файл" 

        self.btn_create.clicked.connect(self.create_json_file) # Создание файла
        self.cB_create.stateChanged.connect(self.cB_open) # Состояние чек бокса
        self.tB_create_filepath.clicked.connect(lambda: self.all_dir(self.lE_create_filepath))
        self.btn_write.clicked.connect(self.write_json_file)  # Записать в файл строку
        self.tB_write_filepath.clicked.connect(lambda: self.all_file(self.lE_write_filepath)) 
        self.btn_read.clicked.connect(self.read_json_file)  # Прочитать файл
        self.tB_read_filepath.clicked.connect(lambda: self.all_file(self.lE_read_filepath)) 
        self.btn_delete.clicked.connect(self.delete_json_file)  # Удалить файл
        self.tB_delete_filepath.clicked.connect(lambda: self.all_file(self.lE_delete_filepath))
        self.btn_exit.clicked.connect(self.exit)  # Выход 

    #Выбор директории
    def all_dir(self, line_edit):
        try:
            path_dir = QFileDialog.getExistingDirectory(self, "Выберите директорию", self.home_path)
            if path_dir:
                line_edit.setText(path_dir)
        except Exception as e:
            self.show_error(f"Ошибка при выборе директории: {e}")

    #Выбор файла
    def all_file(self, line_edit):
        try:
            pathfile, _ = QFileDialog.getOpenFileName(self, "Выберите файл")
            if pathfile:  # Проверяем, что файл выбран
                line_edit.setText(pathfile)
        except Exception as e:
            self.show_error(f"Ошибка при выборе файла: {e}")        
    
    # Создание файла JSON с использованием данных, введенных пользователем
    def create_json_file(self):
        try:
            path = self.lE_create_filepath.text().strip()
            name = self.lE_create_name.text().strip()
            author = self.lE_write_text.text().strip()
            picture = self.lE_write_text2.text().strip()
            key = self.lE_write_key1.text().strip()

            if not name:
                self.show_error("Не задано имя файла.")
                return
            
            filepath = os.path.join(path, f"'{name}'.json") 

            data = {}
            if (author or picture) and key:
                data = {
                    key:{
                        "authors": author ,
                        "paintings": picture,
                    }   
                }

            # Сериализация объекта в JSON и запись в файл
            try:
                with open(filepath, "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                    self.log_action(f"Файл '{filepath}' успешно создан.")
                    self.lE_write_text.setText("")
                    self.lE_write_text2.setText("")
                    self.lE_create_name.setText("")
                    self.lE_write_key1.setText("")
            except Exception as e:
                self.show_error(f"Не удалось создать файл: {e}") 
        
        except Exception as e:
            self.show_error(f"Ошибка при создании файла: {e}")

    # Проверяем состояние чекбокса
    def cB_open(self):
        if self.cB_create.isChecked():
            self.lE_write_text.setReadOnly(False)
            self.lE_write_text2.setReadOnly(False)
            self.lE_write_key1.setReadOnly(False)
        else:
            self.lE_write_text.setText("")
            self.lE_write_text2.setText("")
            self.lE_write_key1.setText("")
            self.lE_write_text.setReadOnly(True)
            self.lE_write_text2.setReadOnly(True)
            self.lE_write_key1.setReadOnly(True)

    # Запись данных в уже существующий JSON файл
    def write_json_file(self):
        filename = self.lE_write_filepath.text().strip()
        author = self.lE_write_text3.text().strip()
        picture = self.lE_write_text4.text().strip()
        new_key = self.lE_write_key.text().strip()
        
        if not filename:
            self.show_error("Не указан путь к файлу.")
            return
        if not new_key:
            self.show_error("Не задан ключ для новых данных.")
            return
        
        new_data = {
            "authors": author ,
            "paintings": picture,
        }
            
        # Открываем файл и загружаем его содержимое
        try:
            with open(filename, "r", encoding="utf-8") as file:
                existing_data = json.load(file)
        except json.JSONDecodeError:
            self.show_error("Ошибка: файл не является корректным JSON.")
        except Exception as e:
            self.show_error(f"Ошибка: {e}")
            return
        
        try:
            existing_data[new_key] = new_data
        
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(existing_data, file, indent=4, ensure_ascii=False)
            self.lE_write_text3.setText("")
            self.lE_write_text4.setText("")
            self.lE_write_key.setText("")
            self.lE_write_filepath.setText("")
            self.log_action(f"Новые данные добавлены в файл {filename}.")
        except Exception as e:
            self.show_error(f"Ошибка при записи файла: {e}")
    
    # Чтение файла и вывод
    def read_json_file(self):
        filepath = self.lE_read_filepath.text().strip()

        if not filepath:
            self.show_error("Не указан путь для файла.")
            return
        
        if not filepath.lower().endswith('.json'):
            self.show_error("Можно читать только JSON-файлы.")
            return

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
            self.log_action(f"Содержимое файла '{filepath}':\n{json.dumps(data, indent=4, ensure_ascii=False)}")
            self.lE_read_filepath.setText("")
        except json.JSONDecodeError:
            self.show_error("Ошибка: файл не является корректным JSON.")
        except Exception as e:
            self.show_error(f"Ошибка: {e}")
        
    # Удаление файла
    def delete_json_file(self):
        filepath = self.lE_delete_filepath.text().strip()
        filepath_w = self.lE_write_filepath.text().strip()
        filepath_r = self.lE_read_filepath.text().strip()

        if not filepath:
            self.show_error("Не указан путь для файла.")
            return
        
        if not filepath.lower().endswith('.json'):
            self.show_error("Можно удалять только JSON-файлы.")
            return
        
        if filepath == filepath_w:
                self.lE_write_filepath.setText("")
        if filepath == filepath_r:
                self.lE_read_filepath.setText("")
        
        try:
            os.remove(filepath)
            self.log_action(f"Файл '{filepath}' успешно удален.")
            self.lE_delete_filepath.setText("")
        except Exception as e:
            self.show_error(f"Ошибка удаления файла: {e}")

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
        self.create_info += "\n ----------------------- -----------------------"
        self.create_info +="\n" + message + "\n"
        self.tE_infa.setPlainText(self.create_info)

    #Для выхода
    def exit(self):
        from firs_win import FirstWindow
        self.Login = FirstWindow()
        self.Login.show()
        self.hide()
