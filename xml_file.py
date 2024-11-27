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
        self.spinbx_new = 0

        self.lE_create_filepath.setReadOnly(True) # задача "Создать файл"
        self.lE_create_filepath.setText(self.home_path)
        self.lE_write_filepath.setReadOnly(True) # задача "Записать в файл"
        self.lE_read_filepath.setReadOnly(True) # задача "Прочитать файл"
        self.sB_sec.setMinimum(0)
        
        self.btn_create.clicked.connect(self.create_xml_file) # Создание файла
        self.tB_create_filepath.clicked.connect(lambda: self.all_dir(self.lE_create_filepath))
        self.btn_write.clicked.connect(self.write_xml_file)  # Записать в файл информацию
        self.btn_write_sec.clicked.connect(lambda: self.new_sec(self.lE_write_filepath))  # Создать новую секцию для Галереи
        self.tB_write_filepath.clicked.connect(lambda: self.all_file(self.lE_write_filepath))
        self.btn_read.clicked.connect(self.read_xml_file)  # Прочитать файл
        self.tB_read_filepath.clicked.connect(lambda: self.all_file(self.lE_read_filepath)) 
        self.btn_delete.clicked.connect(self.delete_xml_file)  # Удалить файл
        self.tB_delete_filepath.clicked.connect(lambda: self.all_file(self.lE_delete_filepath))
        self.btn_exit.clicked.connect(self.exit)  # Выход 

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
                self.sB_sec.setMinimum(1)
                self.sB_sec.setMaximum(self.count_sections(pathfile)) #для Галереи
        except Exception as e:
            self.show_error(f"Ошибка при выборе файла: {e}")        
    
    # Сколько секций уже есть для Галереи
    def count_sections(self, line_edit):
        try:
            filepath = line_edit  # Получаем путь к файлу
            tree = ET.parse(filepath)
            root = tree.getroot()
            sections = root.findall("Секция")  # Найти все элементы 'Секция' и подсчитать их
            return len(sections)
        except Exception as e:
            self.show_error(f"Ошибка подсчета секций: {e}")
            return 0        

    # Создать новую секцию для Галереи
    def new_sec(self, pathfile):
        filepath = pathfile.text().strip()
        
        if not filepath:
            self.show_error("Не указан путь к файлу.")
            return
        
        section = self.sB_sec.maximum()
        section_id = section + 1

        try:
            # Читаем XML-файл
            tree = ET.parse(filepath)
            root = tree.getroot()

            # Создаем новую секцию с атрибутами
            new_section = ET.SubElement(root, "Секция", {"id": str(section_id)})

            tree.write(filepath, encoding="utf-8", xml_declaration=True)
            self.log_action(f"Добавлена новая секция с id='{section_id}' в файл: {filepath}")
            self.sB_sec.setMaximum(section_id)
        except FileNotFoundError:
            self.show_error("Файл не найден. Сначала создайте XML файл.")
        except ET.ParseError:
            self.show_error("Файл не является корректным XML.")
        except Exception as e:
            self.show_error(f"Ошибка: {e}")

    # Задача "Создать файл"
    def create_xml_file(self):
        path = self.lE_create_filepath.text().strip()
        name = self.lE_create_name.text().strip()
        # Увеличение счетчика для уникальных идентификаторов секций
        self.spinbx_new += 1 

        if not name:
            self.show_error("Не задано имя файла.")
            return

        filepath = os.path.join(path, f"'{name}'.xml")
        
        try:
            # Создание корневого элемента XML-документа
            root = ET.Element("Галерея1")
            # Генерация уникального идентификатора секции на основе счетчика
            section_id = str(self.spinbx_new)
            # Добавление подэлемента (секции) к корневому элементу с уникальным идентификатором
            element1_1=ET.SubElement(root, 'Секция', {"id": section_id}) # для Галереи
            # Преобразуем XML-дерево в строку для логирования
            xml_content = ET.tostring(root, encoding="unicode", method="xml") 
            # Сохранение XML-дерева в файл с указанием кодировки и декларации
            ET.ElementTree(root).write(filepath, encoding="utf-8", xml_declaration=True) 
            self.log_action(f"Содержимое файла '{filepath}':\n\n{xml_content}")
        except Exception as e:
            self.show_error(f"Ошибка создания XML файла: {e}")

    # Добавить данные
    def write_xml_file(self):
        filename = self.lE_write_filepath.text().strip()
        section_id = self.sB_sec.value()
        tag = self.lE_write_teg.text().strip()
        text = self.lE_write_text.text().strip()

        if not filename:
            self.show_error("Не указан путь к файлу.")
            return
        if not tag or not text:
            self.show_error("Не заданы необходимые данные.")
            return
        
        try:
            # Загрузка XML-дерева из файла
            tree = ET.parse(filename)
            # Получение корневого элемента XML-документа
            root = tree.getroot()
            
        # Функционал для Галереи
            # Найти элемент "Секция" (element1_1) для вложения
            target_section = root.find(f".//Секция[@id='{section_id}']")
            if target_section is None:
                self.show_error(f"Секция с ID '{section_id}' не найдена.")
                return
        
            # Добавление нового подэлемента в найденную секцию
            element1_1_1 = ET.SubElement(target_section, tag)
            # Установка текста внутри нового элемента
            element1_1_1.text = text
        
        # Функционал не для Галереи 
            #element1_1_1 = ET.Element(tag)
            #element1_1_1.text = text
            #root.append(element1_1_1)

            # Сохранение обновленного XML-дерева обратно в файл
            tree.write(filename, encoding="utf-8", xml_declaration=True)
            self.log_action(f"Новые данные добавлены в секцию с ID '{section_id}' в файле: {filename}")
            self.lE_write_teg.setText("")
            self.lE_write_text.setText("")
        except FileNotFoundError:
            self.show_error("Файл не найден. Сначала создайте XML файл.")
        except ET.ParseError:
            self.show_error("Ошибка парсинга XML. Проверьте структуру файла.")
        except Exception as e:
            self.show_error(f"Ошибка: {e}")
    
    # Прочитать данные
    def read_xml_file(self):
        filepath = self.lE_read_filepath.text().strip()

        if not filepath:
            self.show_error("Не указан путь для файла.")
            return
        
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            xml_content = ET.tostring(root, encoding="unicode", method="xml")
            self.log_action(f"Содержимое файла '{filepath}':\n\n{xml_content}")
        except FileNotFoundError:
            self.show_error("Файл не найден. Сначала создайте XML файл.")
        except ET.ParseError:
            self.show_error("Ошибка парсинга XML. Проверьте структуру файла.")
        except Exception as e:
            self.show_error(f"Ошибка: {e}")

    # Удаляем файл
    def delete_xml_file(self):
        filepath = self.lE_delete_filepath.text().strip()
        filepath_w = self.lE_write_filepath.text().strip()
        filepath_r = self.lE_read_filepath.text().strip()

        if not filepath:
            self.show_error("Не указан путь к файлу.")
            return
        # Проверяем, что файл имеет расширение .xml
        if not filepath.lower().endswith('.xml'):
            self.show_error("Можно удалять только XML-файлы.")
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
            self.show_error(f"Ошибка при удалении файла: {e}")
    
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
        self.create_info += "\n ----------------------- -----------------------"
        self.create_info += "\n" + message + "\n"
        self.tE_infa.setPlainText(self.create_info)

    #Для выхода
    def exit(self):
        from firs_win import FirstWindow
        self.Login = FirstWindow()
        self.Login.show()
        self.hide()
