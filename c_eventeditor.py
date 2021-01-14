#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore
from PyQt5 import uic

# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtSql import *

from datetime import datetime


import c_constants as const
import c_tools as tls

# lineEdit_Days
# toolButton_Recalc

class CEventEditor(QtWidgets.QDialog):
    def __init__(self, pparent, pdatabase, papplication_folder, pid=None):
        # *** Конструктор
        super(CEventEditor, self).__init__(pparent)
        self.database = pdatabase
        self.application_folder = papplication_folder
        self.id = pid
        uic.loadUi(self.application_folder / const.FORMS_FOLDER / const.EVENT_EDITOR_FORM, self)
        self.setWindowFlags(self.windowFlags()
               | QtCore.Qt.WindowMinimizeButtonHint
               | QtCore.Qt.WindowMaximizeButtonHint
               )        
        # *** Загрузим список типов событий
        self.toolButton_Accept.clicked.connect(self.accept)
        self.toolButton_Recalc.clicked.connect(self.recalc)
        self.load_event_types_list()
        # *** Загрузим список периодов
        self.load_periods_list()
        if self.id is not None:

            self.load_data()
    
    def accept(self):
        """Обработчик нажатия на клавишу 'Принять'."""
        self.save_data()
        
    
    def load_data(self):
        """Процедура загрузки данных в контролы."""
        event_name, event_date, self.event_type, self.event_period = self.database.get_event_data(self.id)
        #print("*** EE:LD:n:d:t:p ", event_name, event_date, self.event_type, self.event_period)
        self.lineEdit_EventName.setText(event_name)
        self.dateEdit_EventDate.setDate(event_date)
        self.comboBox_EventType.setCurrentIndex(self.event_types_id_list.index(self.event_type))
        self.comboBox_EventPeriod.setCurrentIndex(self.event_period_id_list.index(self.event_period))
        #self.event_name_entry.insert(tk.END, )
        #self.event_date_entry.set_date(event_date)
        # print("EVED:LD:type ", self.event_type)
        # print("EVED:LD:period ", self.event_period)
        
        #self.event_type_combo.current(
        #self.event_period_combo.current()

    
    def load_event_types_list(self):
        """Загружает список типов событий в listbox."""
        self.event_types_id_list, event_types_name_list = self.database.get_event_types_list()
        self.comboBox_EventType.clear()
        self.comboBox_EventType.addItems(event_types_name_list)

    
    def load_periods_list(self):
        """Загружает список периодов в listbox."""
        self.event_period_id_list, event_period_name_list = self.database.get_periods_list()
        self.comboBox_EventPeriod.clear()
        self.comboBox_EventPeriod.addItems(event_period_name_list)

    
    def recalc(self):
        """Пересчитывает введённое количество дней в дату."""
        entered_days = self.lineEdit_Days.text()
        date_after_days = QtCore.QDate.currentDate()
        print("*** EvEd:REC:dad ", date_after_days)
        print("*** EvEd:REC:ed ", int(entered_days) )
        date_after_days = date_after_days.addDays(int(entered_days))
        print("*** EvEd:REC:dad ", date_after_days)
        self.dateEdit_EventDate.setDate(date_after_days)

    
    def save_data(self):
        """Сохраняет введённые данные."""
        event_name = self.lineEdit_EventName.text()
        event_date = self.dateEdit_EventDate.date().toPyDate()
        event_type = self.event_types_id_list[self.comboBox_EventType.currentIndex()]
        event_period = self.event_period_id_list[self.comboBox_EventPeriod.currentIndex()]
        #print("*** EE:SD:* ", event_name, event_date, event_type, event_period)
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
        self.destroy()
    
    #@QtCore.pyqtSlot()
    #def reject(self):
        #self.close()

    # @QtCore.pyqtSlot()
    # def accept(self):
    
