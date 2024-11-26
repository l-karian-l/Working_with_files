import os
import xml.etree.ElementTree as ET
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5 import uic

class XmlWindow(QtWidgets.QDialog):
    def __init__(self):
        super(XmlWindow, self).__init__()
        uic.loadUi('XML_FILE.ui', self)

        self.create_info = ""
        self.home_path = os.path.expanduser("~")

        self.lE_create_filepath.setReadOnly(True) # задача "Создать файл"
        self.lE_create_filepath.setText(self.home_path)
        self.lE_write_filepath.setReadOnly(True) # задача "Записать в файл"
        self.lE_read_filepath.setReadOnly(True) # задача "Прочитать файл"
        
        self.btn_create.clicked.connect(self.create_xml_file) # Создание файла
        self.tB_create_filepath.clicked.connect(lambda: self.all_dir(self.lE_create_filepath))
        self.btn_write.clicked.connect(self.write_xml_file)  # Записать в файл строку
        self.tB_write_filepath.clicked.connect(lambda: self.all_file(self.lE_write_filepath))
        self.btn_read.clicked.connect(self.read_xml_file)  # Прочитать файл
        self.tB_read_filepath.clicked.connect(lambda: self.all_file(self.lE_read_filepath)) 

    # Выбор директории
    def all_dir(self, line_edit):
        try:
            path_dir = QFileDialog.getExistingDirectory(self, "Выберите директорию", self.home_path)
            if path_dir:
                line_edit.setText(path_dir)
        except Exception as e:
            self.show_error(f"Ошибка при выборе директории: {e}")

    # Выбор файла
    def all_file(self, line_edit):
        try:
            pathfile, _ = QFileDialog.getOpenFileName(self, "Выберите файл")
            if pathfile:  # Проверяем, что файл выбран
                line_edit.setText(pathfile)
        except Exception as e:
            self.show_error(f"Ошибка при выборе файла: {e}")        
    
    # Задача "Создать файл"
    def create_xml_file(self):
        path = self.lE_create_filepath.text().strip()
        name = self.lE_create_name.text().strip()

        if not name:
            self.show_error("Не задано имя файла.")
            return

        filepath = os.path.join(path, f"'{name}'.xml")
        
        self.root = ET.Element("Галерея1")
        element1_1=ET.SubElement(self.root, 'Секция')

        # Преобразуем XML-дерево в строку для логирования
        xml_content = ET.tostring(self.root, encoding="unicode", method="xml")
    
        self.log_action(f"Содержимое файла '{filepath}':\n\n{xml_content}")
        ET.ElementTree(self.root).write(filepath, encoding="utf-8", xml_declaration=True) 

    # Добавить данные
    def write_xml_file(self):
        try:
            filename = self.lE_write_filepath.text().strip()
            tree = ET.parse(filename)
            root = tree.getroot()

            tag = self.lE_write_teg.text().strip()
            text = self.lE_write_text.text().strip()

            if not filename:
                self.show_error("Не указан путь к файлу.")
                return
            if not tag or not text:
                self.show_error("Не заданы необходимые данные.")
                return

            new_element = ET.Element(tag)
            new_element.text = text
            root.append(new_element)

            tree.write(filename, encoding="utf-8", xml_declaration=True)
            self.log_action(f"Новые данные добавлены в файл: {filename}")
            self.lE_write_teg.setText("")
            self.lE_write_text.setText("")
            self.lE_write_filepath.setText("")
        except FileNotFoundError:
            self.show_error("Файл не найден. Сначала создайте XML файл.")
    
    # Добавить данные
    def read_xml_file(self):
        filepath = self.lE_read_filepath.text().strip()

        if not filepath:
            self.show_error("Не указан путь для файла.")
            return
        
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            
            # Форматируем содержимое XML для столбца
            xml_lines = []
            for element in root.iter():
                line = f"<{element.tag}> {element.text.strip() if element.text else ''}"
                xml_lines.append(line)
            
            formatted_content = "\n".join(xml_lines)

            self.log_action(f"Содержимое файла '{filepath}':\n\n{formatted_content}")
        except FileNotFoundError:
            self.show_error("Файл не найден. Сначала создайте XML файл.")
        except ET.ParseError:
            self.show_error("Файл не является корректным XML.")
    

        

    





    # Отображает сообщение об ошибке в виде всплывающего окна.
    def show_error(self, message):
        error1 = QMessageBox()
        error1.setWindowTitle("Ошибка")
        error1.setText(message)
        error1.setIcon(QMessageBox.Icon.Warning)
        error1.setStandardButtons(QMessageBox.StandardButton.Ok)
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
