#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from PyQt5 import uic

from datetime import datetime

import c_constants as const
import c_tools as tls

class CEventEditor(QtWidgets.QMainWindow):
    def __init__(self, pparent, pdatabase, papplication_folder, pid=None):
        # *** Конструктор
        super(CEventEditor, self).__init__(pparent)
        # *** Сохраняем параметры
        self.parent = pparent
        self.database = pdatabase
        self.application_folder = papplication_folder
        self.id = pid
        uic.loadUi(self.application_folder / const.FORMS_FOLDER / const.EVENT_EDITOR_FORM, self)
        # *** Загрузим список типов событий
        self.dateEdit_EventDate.setDate(QtCore.QDate(datetime.now()))
        self.toolButton_Accept.clicked.connect(self.__accept)
        self.toolButton_Recalc.clicked.connect(self.__recalc)
        self.__load_event_types_list()
        # *** Загрузим список периодов
        self.__load_periods_list()
        if self.id is not None:

            self.__load_data()
 
 
    def __accept(self):
        """Обработчик нажатия на клавишу 'Принять'."""
        self.__save_data()
        self.close()

        
    def closeEvent(self, event):
        """Перехватывает событие закрытия окна."""
        self.parent.update()
        event.accept()
    
    
    def __load_data(self):
        """Процедура загрузки данных в контролы."""
        event_name, event_date, self.event_type, self.event_period = self.database.get_event_data(self.id)
        self.lineEdit_EventName.setText(event_name)
        self.dateEdit_EventDate.setDate(event_date)
        self.comboBox_EventType.setCurrentIndex(self.event_types_id_list.index(self.event_type))
        self.comboBox_EventPeriod.setCurrentIndex(self.event_period_id_list.index(self.event_period))

    
    def __load_event_types_list(self):
        """Загружает список типов событий в listbox."""
        self.event_types_id_list, event_types_name_list = self.database.get_event_types_list()
        self.comboBox_EventType.clear()
        self.comboBox_EventType.addItems(event_types_name_list)

    
    def __load_periods_list(self):
        """Загружает список периодов в listbox."""
        self.event_period_id_list, event_period_name_list = self.database.get_periods_list()
        self.comboBox_EventPeriod.clear()
        self.comboBox_EventPeriod.addItems(event_period_name_list)

    
    def __recalc(self):
        """Пересчитывает введённое количество дней в дату."""
        entered_days = self.lineEdit_Days.text()
        if len(entered_days) > 0:

            if entered_days.isdigit():
            
                date_after_days = QtCore.QDate.currentDate()
                date_after_days = date_after_days.addDays(int(entered_days))
                self.dateEdit_EventDate.setDate(date_after_days)

    
    def __save_data(self):
        """Сохраняет введённые данные."""
        event_name = self.lineEdit_EventName.text()
        event_date = self.dateEdit_EventDate.date().toPyDate()
        event_type = self.event_types_id_list[self.comboBox_EventType.currentIndex()]
        event_period = self.event_period_id_list[self.comboBox_EventPeriod.currentIndex()]
        if self.id is None:

            self.database.insert_event(event_name,
                                       event_date,
                                       event_type,
                                       event_period)
        else:

            self.database.update_event(self.id, 
                                       event_name,
                                       event_date,
                                       event_type,
                                       event_period)
