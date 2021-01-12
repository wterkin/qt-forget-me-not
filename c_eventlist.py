#!/usr/bin/python
# -*- coding: utf-8 -*-

#import tkinter as tk
import sys


from PyQt5 import QtWidgets
from PyQt5 import uic

import c_constants as const
import c_eventeditor as eved
import c_tools as tls

class CEventList(QtWidgets.QMainWindow):
    """Класс окна списка событий."""
    def __init__(self, pparent, pdatabase, papplication_folder):
        """Конструктор."""
        super(CEventList, self).__init__(pparent)
        self.database = pdatabase
        self.application_folder = papplication_folder
        uic.loadUi(self.application_folder / const.FORMS_FOLDER / const.EVENT_LIST_FORM, self)
        self.QButtonAdd.clicked.connect(self.insert_event)
        self.QButtonEdit.clicked.connect(self.update_event)
        self.QButtonDelete.clicked.connect(self.delete_event)
        self.load_data()
        print("*** EL:IN")
        # *** Показываем окно
        self.show()
        #self.exec()

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
        dialog = eved.CEventEditor(pparent=self, 
                                   pdatabase=self.database, 
                                   papplication_folder=self.application_folder)
        print("*** EL:IE:ex")
        dialog.exec()
        print("*** EL:IE:ld")
        self.load_data()
        print("*** EL:IE:sh")
        self.show()


    def load_data(self):
        """Обновляет данные в списке."""
        self.listWidget.clear()
        self.event_id_list, self.event_name_list = self.database.get_events_list()
        for event_name in self.event_name_list:
            self.listWidget.addItem(QtWidgets.QListWidgetItem(event_name))


    def update_event(self):
        """Изменяет уже существующее событие."""
        selected_item = self.listWidget.currentRow()
        event_ident = self.event_id_list[selected_item]
        dialog = eved.CEventEditor(pparent=self, 
                                   pdatabase=self.database, 
                                   papplication_folder=self.application_folder, 
                                   pid=event_ident)
        
        print("*** EL:UE:ex")
        dialog.show()
        # sys.exit(dialog.exec_())
        result = dialog.exec_()
        print("*** EL:UE:ld")
        self.load_data()
        print("*** EL:UE:sh")
        # self.open()
   
