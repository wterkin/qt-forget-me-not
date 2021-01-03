#! /usr/bin/python3
## -*- coding: utf-8 -*-
"""Qt оболочка для forget-me-not."""
import sys
from pathlib import Path
from datetime import datetime
from PyQt5 import QtWidgets
from PyQt5 import uic


import c_config as cfg
import c_constants as const
import c_database as db




class MainWindow(QtWidgets.QMainWindow):
    """Класс."""
    def __init__(self):
        """Конструктор класса."""
        super(MainWindow, self).__init__()
        self.application_folder = Path.cwd()
        uic.loadUi(self.application_folder / const.FORMS_FOLDER / const.MAIN_WINDOW_FORM, self)
        self.config = cfg.CConfiguration()
        self.database = db.CDatabase(self.config)
        if not self.is_database_exists():
        
            self.database.create_database()
        actual_data = self.load_data()
        self.display_content(actual_data)
        # self.QMainTable.setColumnCount(TABLE_COLUMNS_COUNT)
        # model = QStandartItemModel()
        # print("*** MN:INIT:FILL")
        #self.fill_table_with_data(data)
        #self.QMainTable.resizeColumnsToContents()
        #self.adjust_columns()
        # print("*** MN:INIT:SHOW")
        self.show()


    def display_content(self, pactual_data):
        """Генерирует HTML-код на основании выборки и выводит его в виджет."""
        #  view.setHtml(html)
        #main.document().setDefaultStyleSheet(
                    #'body {color: #333; font-size: 14px;} '
                    #'h2 {background: #CCF; color: #443;} '
                    #'h1 {background: #001133; color: white;} '
                #)
        #main.setStyleSheet('background-color: #EEF;')
        #main.insertHtml(fh.read())
        style_sheet = "<style>"
        event_type_objects_list = self.database.get_event_types_objects_list()
        for event_type in event_type_objects_list:
            
            style_sheet += " .style_"+f"{event_type.id}"+" {"+f" color: {event_type.fcolor};"+" }\n"
            #style_sheet += f"style_{event_type.id} \{ color: {event_type.fcolor}; \}"
        style_sheet += "</style>"
        print(style_sheet)
        self.textBrowser.setStyleSheet(style_sheet)
        html_document = "<table>\n"
        
        for row in pactual_data:
            
            html_document += self.make_html_row(row)
        html_document += "</table>"
        print(html_document)
        self.textBrowser.insertHtml(html_document)


    def is_database_exists(self):
        """Проверяет наличие базы данных по пути в конфигурации."""
        config_folder_path = Path(self.config.restore_value(cfg.DATABASE_FILE_KEY))
        return config_folder_path.exists()


    def load_data(self):
        """Получает список событий за интервал, определенный в конфиге и отображает их."""
        def sort_list(x):
            
            
            delta=x[db.EVENT_LIST_CONVERTED_DATE_FIELD]-datetime.now().date()
            return delta.days

        full_data = []
        db_month_data = self.database.get_actual_monthly_events()
        full_data.extend(db_month_data)
        db_year_data = self.database.get_actual_yearly_events()
        full_data.extend(db_year_data)
        db_one_shot_data = self.database.get_actual_one_shot_events()
        full_data.extend(db_one_shot_data)
        sorted_data = sorted(full_data, key=sort_list)
        # data_row = 1.0
        # for event in sorted_data:
            
            # row_content = f"""{event[db.EVENT_LIST_CONVERTED_TYPE_EMODJI_FIELD]}
                              # {event[db.EVENT_LIST_CONVERTED_DATE_FIELD]:%d.%m.%Y}
                              # {event[db.EVENT_LIST_CONVERTED_NAME_FIELD]}"""
            # print(row_content)
            # data_row += 1
        return(sorted_data)


    def make_html_row(self, data_row):
        """Создает строку HTML с заданными параметрами."""
        type_id = data_row[db.EVENT_LIST_CONVERTED_TYPE_ID_FIELD]
        emodji = data_row[db.EVENT_LIST_CONVERTED_TYPE_EMODJI_FIELD]
        type_name = data_row[db.EVENT_LIST_CONVERTED_TYPE_NAME_FIELD]
        event_date = data_row[db.EVENT_LIST_CONVERTED_DATE_FIELD]
        event_name = data_row[db.EVENT_LIST_CONVERTED_NAME_FIELD]
        
        #html_line = (f"<tr class='style_{data_row[EVENT_LIST_CONVERTED_TYPE_ID_FIELD]}'>
                       #<td>{data_row[EVENT_LIST_CONVERTED_TYPE_EMODJI_FIELD]}
                           #{data_row[EVENT_LIST_CONVERTED_TYPE_NAME_FIELD]}
                           #{data_row[EVENT_LIST_CONVERTED_DATE_FIELD]}
                           #{data_row[EVENT_LIST_CONVERTED_NAME_FIELD]}<td></tr>")
                           
        return f"<tr><td class='style_{type_id}'>{emodji} {type_name} {event_date:%d.%m.%Y} {event_name} </td></tr>\n"

if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    application.exec_()
