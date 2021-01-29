#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5 import uic

import c_constants as const
import c_eventtypeeditor as evted
import c_tools as tls

class CEventTypesList(QtWidgets.QMainWindow):
    """Класс окна списка событий."""
    def __init__(self, pparent, pdatabase, papplication_folder):
        """Конструктор."""
        super(CEventTypesList, self).__init__(pparent)
        self.parent = pparent
        self.database = pdatabase
        self.application_folder = papplication_folder
        self.backup_need = False
        uic.loadUi(self.application_folder / const.FORMS_FOLDER / const.EVENT_TYPES_LIST_FORM, self)
        self.QButtonAdd.clicked.connect(self.__insert_event_type)
        self.QButtonEdit.clicked.connect(self.__update_event_type)
        self.QButtonDelete.clicked.connect(self.__delete_event_type)
        self.update()
        # *** Показываем окно
        self.show()
        

    def closeEvent(self, event):
        """Перехватывает событие закрытия окна."""
        self.parent.update(self.backup_need)
        event.accept()


    def __delete_event_type(self):
        """Удаляет выбранное событие."""
        
        selected_item = self.listWidget.currentRow()
        event_type_ident = self.event_type_id_list[selected_item]
        if self.database.ask_if_event_type_using(event_type_ident):
            
            tls.notice(self, "Внимание!", "Этот тип используется и не может быть удалён.")
        else:    
            
            self.database.delete_event_type(event_type_ident)
            self.backup_need = True
        self.update()


    def __insert_event_type(self):
        """Добавляет новый тип событий в БД."""
        window = evted.CEventTypeEditor(pparent=self, 
                                        pdatabase=self.database, 
                                        papplication_folder=self.application_folder,
                                        pid=None)
        window.show()


    def __load_data(self):
        """Обновляет данные в списке."""
        self.listWidget.clear()
        self.event_type_id_list, self.event_type_name_list = self.database.get_event_types_list()
        for event_type_name in self.event_type_name_list:
        
            self.listWidget.addItem(QtWidgets.QListWidgetItem(event_type_name))


    def __update_event_type(self):
        """Изменяет уже существующий тип событий."""
        selected_item = self.listWidget.currentRow()
        event_type_ident = self.event_type_id_list[selected_item]
        window = evted.CEventTypeEditor(pparent=self, 
                                        pdatabase=self.database, 
                                        papplication_folder=self.application_folder,
                                        pid=event_type_ident)
        window.show()


    def update(self, pbackup_need = False):
        """Обновляет список событий."""
        if pbackup_need:
        
            self.backup_need = True
        self.__load_data()
        list_is_not_empty = len(self.event_type_name_list) > 0
        self.QButtonEdit.setEnabled(list_is_not_empty)
        self.QButtonDelete.setEnabled(list_is_not_empty)
        