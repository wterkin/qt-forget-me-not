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
import c_eventlist as evlst

# ToDo: Ежедневный и еженедельный бэкап базы
# ToDo: При каждом запуске удалять просроченные единоразовые события
# ToDo: Выделять сегодняшние события
# ToDo: Сортировать список событий

class CMainWindow(QtWidgets.QMainWindow):
    """Класс."""
    def __init__(self):
        """Конструктор класса."""
        super(CMainWindow, self).__init__()
        self.application_folder = Path.cwd()
        uic.loadUi(self.application_folder / const.FORMS_FOLDER / const.MAIN_WINDOW_FORM, self)
        self.actionEventsList.triggered.connect(self.__event_list_show)

        self.config = cfg.CConfiguration()
        
        self.database = db.CDatabase(self.config)
        if not self.__is_database_exists():
        
            self.database.create_database()
        self.update()
        self.show()

    
    def __display_content(self, pactual_data):
        """Генерирует HTML-код на основании выборки и выводит его в виджет."""
        # *** Формируем таблицу стилей страницы
        css_style = "<style>\n"
        event_type_objects_list = self.database.get_event_types_objects_list()
        for event_type in event_type_objects_list:
            
            css_style += f".style_{event_type.id} {{ color: {event_type.fcolor}; }}\n"
        
        css_style += "</style>"
        # *** Формируем HTML-документ
        html_document = f"""<html>\n
                              <head>\n
                                {css_style}
                              </head>\n
                                <body>\n
                                  <table>\n"""
                                 
        content = ""
        for row in pactual_data:
            
            content += self.__make_html_row(row)
        
        html_document += f"""     {content}    
                                </table>\n
                              </body>\n
                            </html>"""
        self.textBrowser.setStyleSheet("background-color: #3F3F3F;")
        self.textBrowser.insertHtml(html_document)
        
               #p {font-size: 16px;
                  #font-family: "%s";
                  #margin-right:50px;
                  #margin-left:50px;
                  #}
               #p1 {font-size: 16px;
                   #font-family: "%s";
                   #margin-right:50px;
                   #margin-left:50px;
                   #}
               #</style>
               #</head>
               #<body>
               #""" % (fontfamily, fontfamily)          
          

    def __event_list_show(self):
        """Вызывает окно списка событий."""
        window = evlst.CEventList(pparent=self, 
                                  pdatabase=self.database, 
                                  papplication_folder=self.application_folder)
   

    def __is_database_exists(self):
        """Проверяет наличие базы данных по пути в конфигурации."""
        config_folder_path = Path(self.config.restore_value(cfg.DATABASE_FILE_KEY))
        return config_folder_path.exists()


    def __load_data(self):
        """Получает список событий за интервал, определенный в конфиге."""
        def sort_list(x):
            
            delta=x[db.EVENT_LIST_CONVERTED_DATE_FIELD]-datetime.now().date()
            return delta.days

        full_data = []
        db_month_data = self.database.get_actual_monthly_events()
        print("*** MN:LD:mnt ", db_month_data)
        full_data.extend(db_month_data)
        db_year_data = self.database.get_actual_yearly_events()
        print("*** MN:LD:yr ", db_year_data)
        full_data.extend(db_year_data)
        db_one_shot_data = self.database.get_actual_one_shot_events()
        print("*** MN:LD:os ", db_one_shot_data)
        full_data.extend(db_one_shot_data)
        sorted_data = sorted(full_data, key=sort_list)
        print(sorted_data)
        return(sorted_data)


    def __make_html_row(self, data_row):
        """Создает строку HTML с заданными параметрами."""
        type_id = data_row[db.EVENT_LIST_CONVERTED_TYPE_ID_FIELD]
        emodji = data_row[db.EVENT_LIST_CONVERTED_TYPE_EMODJI_FIELD]
        type_name = data_row[db.EVENT_LIST_CONVERTED_TYPE_NAME_FIELD]
        event_date = data_row[db.EVENT_LIST_CONVERTED_DATE_FIELD]
        event_name = data_row[db.EVENT_LIST_CONVERTED_NAME_FIELD]
        return f"<tr><td class='style_{type_id}'>{emodji} {type_name}{const.TYPE_SEPARATOR}{event_date:%d.%m.%Y} {event_name} </td></tr>\n"


    def update(self):
        """Обновляет содержимое браузера."""
        self.textBrowser.clear()
        self.__display_content(self.__load_data())
        

if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    main_window = CMainWindow()
    application.exec_()
