#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса редактора типа события."""
from PyQt5 import QtWidgets, QtCore
from PyQt5 import uic
from PyQt5.QtGui import QColor

from datetime import datetime

import c_constants as const
import c_tools as tls

class CEventTypeEditor(QtWidgets.QMainWindow):
    def __init__(self, pparent, pdatabase, papplication_folder, pid=None):
        # *** Конструктор
        super(CEventTypeEditor, self).__init__(pparent)
        # *** Сохраняем параметры
        self.parent = pparent
        self.database = pdatabase
        self.application_folder = papplication_folder
        self.id = pid
        uic.loadUi(self.application_folder / const.FORMS_FOLDER / const.EVENT_TYPE_EDITOR_FORM, self)
        self.pushButton_Accept.clicked.connect(self.__accept)
        self.pushButton_ColorDialog.clicked.connect(self.__choose_color)
        # *** Загрузим список периодов
        if self.id is not None:

            self.__load_data()

 
    def __accept(self):
        """Обработчик нажатия на клавишу 'Принять'."""
        self.__save_data()
        self.parent.update(True)
        self.close()

       
    def __choose_color(self):
        """Функция вызова диалога выбора цвета."""
        selected_color = QColor(self.lineEdit_EventTypeColor.text())
        color_dlg = QtWidgets.QColorDialog()
        color_dlg.setCurrentColor(selected_color)
        if color_dlg.exec_() == QtWidgets.QColorDialog.Accepted:
        
            selected_color = color_dlg.currentColor()
            self.lineEdit_EventTypeColor.setText(selected_color.name())

       
    def closeEvent(self, event):
        """Перехватывает событие закрытия окна."""
        event.accept()
    
    
    def __load_data(self):
        """Процедура загрузки данных в контролы."""
        event_type_name, event_type_color, event_type_emodji = self.database.get_event_type_data(self.id)
        self.lineEdit_EventTypeName.setText(event_type_name)
        self.lineEdit_EventTypeColor.setText(event_type_color)
        self.lineEdit_EventTypeEmodji.setText(event_type_emodji)

    
    def __save_data(self):
        """Сохраняет введённые данные."""
        event_type_name = self.lineEdit_EventTypeName.text()
        event_type_color = self.lineEdit_EventTypeColor.text()
        event_type_emodji = self.lineEdit_EventTypeEmodji.text()
        if self.id is None:

            self.database.insert_event_type(event_type_name,
                                            event_type_color,
                                            event_type_emodji)
        else:

            self.database.update_event_type(self.id, 
                                            event_type_name,
                                            event_type_color,
                                            event_type_emodji)
