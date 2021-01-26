#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5 import uic

import c_constants as const


class CEventTypesList(QtWidgets.QMainWindow):
    """Класс окна списка событий."""
    def __init__(self, pparent, pdatabase, papplication_folder):
        """Конструктор."""
        super(CEventTypesList, self).__init__(pparent)
        self.parent = pparent
        self.database = pdatabase
        self.application_folder = papplication_folder
        uic.loadUi(self.application_folder / const.FORMS_FOLDER / const.EVENT_TYPES_LIST_FORM, self)
        # self.QButtonAdd.clicked.connect(self.__insert_event)
        # self.QButtonEdit.clicked.connect(self.__update_event)
        # self.QButtonDelete.clicked.connect(self.__delete_event)
        self.update()
        # *** Показываем окно
        self.show()


    def closeEvent(self, event):
        """Перехватывает событие закрытия окна."""
        self.parent.update()
        event.accept()

    def __load_data(self):
        """Обновляет данные в списке."""
        self.listWidget.clear()
        self.event_id_list, self.event_name_list = self.database.get_event_types_list()
        for event_name in self.event_name_list:
        
            self.listWidget.addItem(QtWidgets.QListWidgetItem(event_name))



    def update(self):
        """Обновляет список событий."""
        self.__load_data()