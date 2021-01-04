#!/usr/bin/python
# -*- coding: utf-8 -*-

#import tkinter as tk
from PyQt5 import QtWidgets
from PyQt5 import uic

import c_constants as const
import c_eventeditor as eved
import c_tools as tls

class CEventList(QtWidgets.QDialog):
    """Класс окна списка событий."""
    def __init__(self, pdatabase, papplication_folder):
        """Конструктор."""
        super(CEventList, self).__init__()
        self.database = pdatabase
        self.application_folder = papplication_folder
        uic.loadUi(self.application_folder / const.FORMS_FOLDER / const.EVENT_LIST_FORM, self)
        self.QButtonAdd.clicked.connect(self.insert_event)
        self.QButtonEdit.triggered.connect(self.update_event)
        self.QButtonDelete.triggered.connect(self.delete_event)
        self.load_data()
        # *** Показываем окно
        print("Dialog")


    def delete_event(self):
        """Удаляет выбранное событие."""
        #selected_items = self.events_box.curselection()
        #if len(selected_items) > 0:

            #event_ident = self.event_id_list[selected_items[0]]
            #self.database.update_event(event_ident)
            #self.load_data()
        pass
    
    
    def insert_event(self):
        """Добавляет новое событие в базу."""
        print("*************")
        dialog = eved.CEventEditor(self.database, self.application_folder, None)
        dialog.exec()
        self.load_data()


    def load_data(self):
        """Обновляет данные в списке."""
        self.listWidget.clear()
        #self.listWidget.addItem(QListWidgetItem(name, self.list))
        self.event_id_list, self.event_name_list = self.database.get_events_list()
        for event_name in self.event_name_list:
            #self.events_box.insert(tk.END, event_name)
            self.listWidget.addItem(QtWidgets.QListWidgetItem(event_name))

    def update_event(self):
        """Изменяет уже существующее событие."""
        # FixMe: вот тут не передаются данные в редактор!
        #selected_items = self.events_box.curselection()
        #if len(selected_items) > 0:
            #event_ident = self.event_id_list[selected_items[0]]
            #event_editor = eved.EventEditor(self,
                                            #pdatabase=self.database,
                                            #pid=event_ident)
            #self.load_data()
        pass
   
