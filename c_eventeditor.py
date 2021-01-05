#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5 import uic

from datetime import datetime

import c_constants as const
import c_tools as tls

    #"""Класс окна списка событий."""
    #def __init__(self, pdatabase, papplication_folder):
        #"""Конструктор."""
        #super(CEventList, self).__init__()
        #self.database = pdatabase
        #self.application_folder = papplication_folder
        #uic.loadUi(self.application_folder / const.FORMS_FOLDER / const.EVENT_LIST_FORM, self)


class CEventEditor(QtWidgets.QDialog):
    def __init__(self, pdatabase, papplication_folder, pid=None):
        # *** Конструктор
        super(CEventEditor, self).__init__()
        self.database = pdatabase
        self.application_folder = papplication_folder
        self.id = pid
        print("*** EE:init:pid", pid)
        uic.loadUi(self.application_folder / const.FORMS_FOLDER / const.EVENT_EDITOR_FORM, self)
        # *** Загрузим список типов событий
        self.load_event_types_list()
        # *** Загрузим список периодов
        self.load_periods_list()
        if self.id is not None:

            self.load_data()
        
    
    def load_data(self):
        """Процедура загрузки данных в контролы."""
        event_name, event_date, self.event_type, self.event_period = self.database.get_event_data(self.id)
        print("*** EE:LD:n:d:t:p ", event_name, event_date, self.event_type, self.event_period)
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

    
    def save_data(self):
        """Сохраняет введённые данные."""
        event_date = datetime.strptime(self.event_date_entry.get(), "%d.%m.%Y")
        event_type = self.event_types_id_list[self.event_type_combo.current()]
        event_period = self.event_period_id_list[self.event_period_combo.current()]
      
        if self.id is None:

            self.database.insert_event(self.event_name_entry.get().strip(),
                                       event_date,
                                       event_type,
                                       event_period)
        else:

            self.database.update_event(self.id, 
                                       self.event_name_entry.get().strip(),
                                       event_date,
                                       event_type,
                                       event_period)
        self.destroy()
    
    
