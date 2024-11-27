import os
import zipfile
from functools import partial # Позволяет зафиксировать значения аргументов для вызова функции
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QTableWidgetItem


class ZipWindow(QtWidgets.QDialog):
    def __init__(self):
        super(ZipWindow, self).__init__()
        uic.loadUi('ZIP_FILE.ui', self)

        self.create_info = ""
        self.home_path = os.path.expanduser("~")

        # Заполение таблицы
        self.select_f(self.home_path, self.tableWidget_file)

        # Отслеживание изменений в таблицах
        self.tableWidget_file.itemChanged.connect(lambda: self.update_f_tab(self.cB_all_f, self.btn_create, self.tableWidget_file))
        self.tableWidget_file_2.itemChanged.connect(lambda: self.update_f_tab(self.cB_all_f_2, self.btn_write, self.tableWidget_file_2))

        self.lE_create_filepath.setReadOnly(True) # задача "Создать файл"
        self.lE_create_filepath.setText(self.home_path)
        self.lE_write_filepath_zip.setReadOnly(True) # задача "Записать в файл"
        self.lE_write_filepath_files.setReadOnly(True)
        self.lE_unzip_filepath.setReadOnly(True) # задача "Разархивировать файл"
        self.lE_unzip_filepath_2.setReadOnly(True)

        self.btn_create.setEnabled(False)
        self.btn_create.clicked.connect(self.create_zip_arc) # Создание файла
        self.cB_all_f.stateChanged.connect(partial(self.select_all_file, self.tableWidget_file)) # Check box 1"Выбрать все"
        self.tB_create_filepath.clicked.connect(lambda: self.all_dir(self.lE_create_filepath, self.tableWidget_file ))
       
        self.btn_write.setEnabled(False)
        self.btn_write.clicked.connect(self.write_zip_file)  # Записать в файл строку
        self.tB_write_filepath_zip.clicked.connect(lambda: self.all_file(self.lE_write_filepath_zip))
        self.tB_write_filepath_file.clicked.connect(lambda: self.all_dir(self.lE_write_filepath_files, self.tableWidget_file_2))
        self.cB_all_f_2.stateChanged.connect(partial(self.select_all_file, self.tableWidget_file_2)) # Check box "Выбрать все"

        self.btn_unzip.clicked.connect(self.unzip_file)  # Разархивировать файл
        self.tB_unzip_filepath.clicked.connect(lambda: self.all_file(self.lE_unzip_filepath))
        self.tB_unzip_filepath_2.clicked.connect(lambda: self.all_dir(self.lE_unzip_filepath_2)) 

        self.btn_delete.clicked.connect(self.delete_zip_file)  # Удалить файл
        self.tB_delete_filepath.clicked.connect(lambda: self.all_file(self.lE_delete_filepath))
        
        self.btn_exit.clicked.connect(self.exit)  # Выход 

    #Выбор директории c выводом информации в таблицу
    def all_dir(self, line_edit, table_Widget=None):
        try:
            path_dir = QFileDialog.getExistingDirectory(self, "Выберите директорию", self.home_path)
            if path_dir:
                line_edit.setText(path_dir)
                if table_Widget:
                    self.select_f(path_dir, table_Widget)
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
    
    # Отобразить все файлы для выбора в выбранной директории
    def select_f(self, path_dir, table_Widget):
        try:
            file_path = []
            for item in os.listdir(path_dir):
                full_path = os.path.join(path_dir, item)
                if os.path.isfile(full_path):
                    file_path.append(item)
        
            table_Widget.setColumnCount(1)
            table_Widget.setRowCount(len(file_path))
            table_Widget.verticalHeader().setVisible(False)
            table_Widget.setHorizontalHeaderLabels(['Файлы'])

            #Настройка Check box, для выбора таблиц
            for row, string in enumerate(file_path, 0):
                chkBoxItem = QTableWidgetItem(string)
                chkBoxItem.setText(string)
                chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                chkBoxItem.setCheckState(Qt.Unchecked)
                table_Widget.setItem(row, 0, chkBoxItem)
        except Exception as e:
            self.show_error(f"Ошибка при загрузке файлов в таблицу: {e}")

    # Выставление значений при нажатии на check box "Выбрать все"
    def select_all_file(self, table_Widget, state):
        for row in range(table_Widget.rowCount()):
            item = table_Widget.item(row, 0)
            if item:  # Проверка, что элемент существует
                item.setCheckState(Qt.Checked if state == Qt.Checked else Qt.Unchecked)

    # Проверка состояния чекбоксов и активность кнопок
    def update_f_tab(self, cB, btn, table_Widget ):
        any_checked = False  
        all_checked = True

        for row in range(table_Widget.rowCount()):
            item = table_Widget.item(row, 0)
            if item and item.checkState() == Qt.Checked:
                any_checked = True
            else:
                all_checked = False 

        btn.setEnabled(any_checked)
        cB.blockSignals(True)
        cB.setCheckState(Qt.Checked if all_checked else Qt.Unchecked)
        cB.blockSignals(False)        

    # Создать архив в форматер zip и добавляет в него указанные файлы
    def create_zip_arc(self):
        try:
            path = self.lE_create_filepath.text().strip()
            name_z = self.lE_create_name.text().strip()

            if not path or not os.path.isdir(path):
                self.show_error("Указанный путь к директории неверен или не существует.")
                return
            if not name_z:
                self.show_error("Не задано имя файла.")
                return
                
            filepath = os.path.join(path, f"'{name_z}'.zip") 

            checked_items = []
            for row in range(self.tableWidget_file.rowCount()):
                item = self.tableWidget_file.item(row, 0)
                if item.checkState() == Qt.Checked:
                    checked_items.append(item.text())

            # Создание архива в режиме записи
            with zipfile.ZipFile(filepath, 'w') as zipf:    
                for file_path in checked_items:
                    # Формирование полного пути к файлу
                    full_path = os.path.join(path, file_path)
                    # Проверка: существует ли файл
                    if os.path.exists(full_path):                             
                        # Добавление файла в архив с сохранением только имени файла (без пути)
                        zipf.write(full_path, arcname=os.path.basename(file_path))
                    else:
                        self.show_error(f"Файл '{file_path}' не найден и не будет добавлен в архив.")
            self.log_action(f"Файл '{filepath}' успешно создан.Добавлено файлов: {len(checked_items)}")
            self.lE_create_name.setText("")
            self.select_f(path, self.tableWidget_file)
        except Exception as e:
            self.show_error(f"Ошибка при создании архива: {e}")

    # Добавить файл, выбранный пользователем, в архив
    def write_zip_file(self):
        try:
            archive_path = self.lE_write_filepath_zip.text().strip()
            path1 = self.lE_write_filepath_files.text().strip()

            if not archive_path.lower().endswith('.zip'):
                self.show_error("Выбранный файл не является ZIP-архивом.")
                return
            if not path1:
                self.show_error("Директория для выбора файлов не выбрана.")
                return
            if not os.path.exists(archive_path):
                self.show_error(f"Архив '{archive_path}' не найден.")
                return

            checked_items = []
            for row in range(self.tableWidget_file_2.rowCount()):
                item = self.tableWidget_file_2.item(row, 0)
                if item.checkState() == Qt.Checked:
                    checked_items.append(item.text())

            # Открываем архив для добавления файла
            with zipfile.ZipFile(archive_path, 'a') as zipf:
                for file_path in checked_items:
                    full_path = os.path.join(path1, file_path)
                    if os.path.exists(full_path):                             
                        # Добавление файла в архив с сохранением только имени файла (без пути)
                        zipf.write(full_path, arcname=os.path.basename(file_path))
                    else:
                        self.show_error(f"Файл '{file_path}' не найден и не будет добавлен в архив.")
            self.log_action(f"В архив '{archive_path}' добавлено файлов: {len(checked_items)}.")
            self.select_f(path1, self.tableWidget_file_2)
        except Exception as e:
            self.show_error(f"Ошибка при добавлении файлов в архив: {e}")

    # Разархивировать файл и вывести данные о нем
    def unzip_file(self):
        try:
            archive = self.lE_unzip_filepath.text().strip()
            where = self.lE_unzip_filepath_2.text().strip()

            if not archive.lower().endswith('.zip'):
                self.show_error("Выбранный файл не является ZIP-архивом.")
                return
            if not archive:
                self.show_error("Путь к zip файлу не выбран.")
                return

            # Открываем архив и извлекаем содержимое
            with zipfile.ZipFile(archive, 'r') as zipf:
                # Извлечение всех файлов из архива в указанную директорию
                zipf.extractall(where)
                # Получаем список файлов из архива
                extracted_files = zipf.namelist() 

                 # Формируем информацию о файлах
                file_info = []
                for file_name in extracted_files:
                    file_path = os.path.join(where, file_name)
                    if os.path.exists(file_path):
                        # Получение размера файла
                        size = os.path.getsize(file_path)
                        # Добавление информации о файле в список
                        file_info.append(f"Имя: {file_name}, Размер: {size} байт, Путь: {file_path}")
                self.log_action("Файлы успешно извлечены:\n\n" + "\n".join(file_info))
                self.lE_unzip_filepath.setText("")
        except zipfile.BadZipFile:
            self.show_error("Файл не является ZIP архивом или поврежден.")
        except Exception as e:
            self.show_error(f"Ошибка при извлечении архива: {e}")

    # Удаление архива и файлов внутри
    def delete_zip_file(self):
        filepath = self.lE_delete_filepath.text().strip()
        filepath_u = self.lE_unzip_filepath.text().strip()
        filepath_w = self.lE_write_filepath_zip.text().strip()

        if not filepath:
            self.show_error("Не указан путь для файла.")
            return
        
        if not filepath.lower().endswith('.zip'):
            self.show_error("Можно удалять только ZIP-файлы.")
            return
        
        if filepath == filepath_w:
                self.lE_write_filepath_zip.setText("")
        if filepath == filepath_u:
                self.lE_unzip_filepath.setText("")
        
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
        