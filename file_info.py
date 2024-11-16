import psutil
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic

class InfoWindow(QtWidgets.QDialog):
    def __init__(self):
        super(InfoWindow, self).__init__()
        uic.loadUi('INFO_FILE.ui', self)

        self.btn_exit.clicked.connect(self.exit)
        self.tE_info.setReadOnly(True)

        # Кнопка для обновления информации о дисках
        self.btn_refresh.clicked.connect(self.display_disk_info)  
        
        # Отображаем информацию о дисках при запуске
        self.display_disk_info()
        
    # Собирает информацию о логических дисках. Возвращает строку с информацией о каждом разделе.
    def get_disk_info(self):
        
        disk_info = ""

        try: 
            # Получаем информацию о дисках
            partitions = psutil.disk_partitions()

            # Проходим по каждому разделу и выводим информацию
            for partition in partitions:
                disk_info += f"Имя диска: {partition.device}\n"
                disk_info += f"Точка монтирования: {partition.mountpoint}\n"
                disk_info += f"Файловая система: {partition.fstype}\n"
                
                try:
                    # Получаем данные о дисковом пространстве
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_info += f"Метка тома: {partition.device}\n"
                    disk_info += f"Размер: {usage.total // (1024 ** 3)} ГБ\n"
                    disk_info += f"Свободно: {usage.free // (1024 ** 3)} ГБ\n"
                
                # Если нет доступа к разделу, добавляем соответствующее сообщение
                except PermissionError:    
                    disk_info += "Нет доступа к разделу\n"
                
                #Если ошибка приполучении данных
                except Exception as e:
                    disk_info += f"Ошибка при получении данных: {e}\n"
                
                disk_info += "-" * 30 + "\n"
        
        except Exception as e:
            disk_info += f"Ошибка при получении списка дисков: {e}\n"

        return disk_info

    # Отображает информацию о дисках в текстовом поле `tE_info`.
    def display_disk_info(self):
        try:
            # Получаем информацию о дисках и выводим в текстовое поле
            disk_info = self.get_disk_info()
            self.tE_info.setPlainText(disk_info)
        except Exception as e:
            error1 = QMessageBox()
            error1.setWindowTitle("Ошибка")
            error1.setText(f"Не удалось обновить информацию о дисках: {e}")
            error1.setIcon(QMessageBox.Icon.Warning)
            error1.setStandardButtons(QMessageBox.StandardButton.Ok)
            error1.buttonClicked.connect(self.popup)
            error1.exec_()

    def popup(self, btn):
        if btn.text() == "OK":
            self.hide()

    #Для выхода
    def exit(self):
        from firs_win import FirstWindow
        self.Login = FirstWindow()
        self.Login.show()
        self.hide()
        