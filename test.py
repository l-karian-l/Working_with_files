import os
import xml.etree.ElementTree as ET

# Создаем XML-древо и записываем его в файл
def create_xml_file(file_name):
    root = ET.Element("Галерея1")
    element1_1=ET.SubElement(root, 'Секция')
 
    ET.dump(root)
    ET.ElementTree(root).write(file_name, encoding="utf-8", xml_declaration=True) 

# Имя файла XML, с которым будем работать
file_name = "E:\9_семестр\Мамаев\ПР 3\Working_with_files\galery.xml"

# 1. Создание XML-файла
create_xml_file(file_name)

