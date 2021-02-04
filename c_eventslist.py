#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса списка событий."""
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
        self.parent = pparent
        self.database = pdatabase
        self.backup_need = False
        self.application_folder = papplication_folder
        uic.loadUi(self.application_folder / const.FORMS_FOLDER / const.EVENT_LIST_FORM, self)
        self.QButtonAdd.clicked.connect(self.__insert_event)
        self.QButtonEdit.clicked.connect(self.__update_event)
        self.QButtonDelete.clicked.connect(self.__delete_event)
        self.update()
        # *** Показываем окно
        self.show()


    def closeEvent(self, event):
        """Перехватывает событие закрытия окна."""
        self.parent.update(self.backup_need)
        event.accept()


    def __delete_event(self):
        """Удаляет выбранное событие."""
        selected_item = self.listWidget.currentRow()
        event_ident = self.event_id_list[selected_item]
        self.database.delete_event(event_ident)
        self.backup_need = True
        self.update()
        
        
    
    def __insert_event(self):
        """Добавляет новое событие в базу."""
        window = eved.CEventEditor(pparent=self, 
                                    pdatabase=self.database, 
                                    papplication_folder=self.application_folder,
                                    pid=None)
        window.show()


    def __load_data(self):
        """Обновляет данные в списке."""
        self.listWidget.clear()
        self.event_id_list, self.event_name_list = self.database.get_events_list()
        for event_name in self.event_name_list:
        
            self.listWidget.addItem(QtWidgets.QListWidgetItem(event_name))


    def __update_event(self):
        """Изменяет уже существующее событие."""
        selected_item = self.listWidget.currentRow()
        event_ident = self.event_id_list[selected_item]
        window = eved.CEventEditor(pparent=self, 
                                   pdatabase=self.database, 
                                   papplication_folder=self.application_folder,
                                   pid=event_ident)
        
        window.show()
   
   
    def update(self, pbackup_need = False):
        """Обновляет список событий."""
        
        if pbackup_need:
        
            self.backup_need = True
        self.__load_data()
        list_is_not_empty = len(self.event_name_list) > 0
        self.QButtonEdit.setEnabled(list_is_not_empty)
        self.QButtonDelete.setEnabled(list_is_not_empty)
        