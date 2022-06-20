#! /usr/bin/python3
## -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Qt оболочка для forget-me-not."""
import sys
from pathlib import Path
import shutil
from datetime import datetime
from PyQt5 import QtWidgets, QtGui
from PyQt5 import uic

import c_config as cfg
import c_constants as const
import c_database as db
import c_eventslist as evlst
import c_eventtypeslist as evtypelst
import c_tools as tls

PROGRAM_VERSION = "1.1"

class CMainWindow(QtWidgets.QMainWindow):
    """Класс."""
    def __init__(self):
        """Конструктор класса."""
        super(CMainWindow, self).__init__()
        self.application_folder = Path.cwd()
        uic.loadUi(self.application_folder / const.FORMS_FOLDER / const.MAIN_WINDOW_FORM, self)
        text_font = QtGui.QFont()
        text_font.setPointSize(text_font.pointSize()+3)
        self.textBrowser.setFont(text_font)        
        self.actionEventsList.triggered.connect(self.__event_list_show)
        self.actionOpenDatabase.triggered.connect(self.__open_database)
        self.actionEventTypesList.triggered.connect(self.__event_type_list_show)
        self.config = cfg.CConfiguration()
        
        self.database = db.CDatabase(self.config)
        if not self.__is_database_exists():
        
            self.database.create_database()
        self.database.cleanup()
        self.backup_need = False
        #PROGRAM_VERSION
        window_title = self.windowTitle() + f" ver. {PROGRAM_VERSION}"
        self.setWindowTitle(window_title)
        self.setWindowIcon(QtGui.QIcon('ui/forget-me-not.ico'))
        self.update()
        self.show()
  

    def __backup(self):
        """Функция осуществляет резервное копирование БД."""
        self.database.disconnect_from_database()

        backup_folder = Path(self.config.restore_value(cfg.DATABASE_FILE_KEY)).parent / const.BACKUPS_FOLDER
        if not backup_folder.exists():
        
            backup_folder.mkdir(parents=True, exist_ok=True)
            
        db_filename = Path(self.config.restore_value(cfg.DATABASE_FILE_KEY))
        new_filename = f"forget-me-not_{datetime.now():%Y%m%d_%H%M}.db"
        full_new_filename = backup_folder / new_filename
        shutil.copyfile(db_filename, full_new_filename)
        
    
    def __backup_rotation(self):
        """Убивает старые бэкапы."""
        backup_files = []
        max_backup_files = self.config.restore_value(cfg.MAX_BACKUP_FILES_KEY)
        backup_folder = Path(self.config.restore_value(cfg.DATABASE_FILE_KEY)).parent / const.BACKUPS_FOLDER
        for backup_file in backup_folder.iterdir():
            
            backup_files.append(backup_file)
        if len(backup_files) > max_backup_files:
            
            useless_files = backup_files[max_backup_files+1:]
            for useless_file in useless_files:
            
                useless_file.unlink()
            
        
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
        background_color = self.config.restore_value(cfg.BACKGROUND_COLOR_KEY)
        self.textBrowser.setStyleSheet(f"background-color: {background_color};")
        self.textBrowser.insertHtml(html_document)
        

    def __event_list_show(self):
        """Вызывает окно списка событий."""
        window = evlst.CEventList(pparent=self, 
                                  pdatabase=self.database, 
                                  papplication_folder=self.application_folder)
   

    def __event_type_list_show(self):
        """Показывает список типов событий."""
        
        window = evtypelst.CEventTypesList(pparent=self, 
                                           pdatabase=self.database, 
                                           papplication_folder=self.application_folder)


    def __is_database_exists(self):
        """Проверяет наличие базы данных по пути в конфигурации."""
        config_folder_path = Path(self.config.restore_value(cfg.DATABASE_FILE_KEY))
        return config_folder_path.exists()


    def __load_data(self):
        """Получает список событий за интервал, определенный в конфиге."""

        def sort_list(x):
            
            delta=datetime.now().date() - x[db.EVENT_LIST_CONVERTED_DATE_FIELD]
            return delta.days

        full_data = []
        db_month_data = self.database.get_actual_monthly_events()
        full_data.extend(db_month_data)
        # print("month ", db_month_data)
        db_year_data = self.database.get_actual_yearly_events()
        full_data.extend(db_year_data)
        # print("year ", db_year_data)
        db_one_shot_data = self.database.get_actual_one_shot_events()
        full_data.extend(db_one_shot_data)
        # print("one ", db_one_shot_data)
        sorted_data = sorted(full_data, key=sort_list)
        return(sorted_data)


    def __make_html_row(self, data_row):
        """Создает строку HTML с заданными параметрами."""
        future_sign = self.config.restore_value(cfg.FUTURE_SIGN_KEY)
        tomorrow_sign = self.config.restore_value(cfg.TOMORROW_SIGN_KEY)
        today_sign = self.config.restore_value(cfg.TODAY_SIGN_KEY)
        yesterday_sign = self.config.restore_value(cfg.YESTERDAY_SIGN_KEY)
        type_id = data_row[db.EVENT_LIST_CONVERTED_TYPE_ID_FIELD]
        emodji = data_row[db.EVENT_LIST_CONVERTED_TYPE_EMODJI_FIELD]
        type_name = data_row[db.EVENT_LIST_CONVERTED_TYPE_NAME_FIELD]
        event_date = data_row[db.EVENT_LIST_CONVERTED_DATE_FIELD]
        event_name = data_row[db.EVENT_LIST_CONVERTED_NAME_FIELD]
        if event_date == tls.shift_date(datetime.now(), 1).date():
            
            time_mark = tomorrow_sign
        elif event_date == datetime.now().date():

            time_mark = today_sign
        elif event_date == tls.shift_date(datetime.now(), -1).date():

            time_mark = yesterday_sign
        else:

            time_mark = future_sign
        html_row = f"<tr><td class='style_{type_id}'>{time_mark} {emodji} {type_name}{const.TYPE_SEPARATOR}{event_date:%d.%m.%Y} {event_name} "
        
        if (type_id == db.EVENT_TYPE_MEMORY_DAY) or (type_id == db.EVENT_TYPE_BIRTH_DAY) :
        
            html_row += data_row[db.EVENT_LIST_CONVERTED_MESSAGE_FIELD]
        html_row += "</td></tr>\n"
        return html_row
            

    def __open_database(self):
        """Открывает базу данных и запоминает ее, как базу по умолчанию."""
        db_path = Path(self.config.restore_value(cfg.DATABASE_FILE_KEY)).parent
        selected_file = QtWidgets.QFileDialog.getOpenFileName(parent=self,
                                                              caption="Выберите файл базы данных SQLITE",
                                                              directory=str(db_path),
                                                              filter="forget-me-not*.db"
                                                             )
        if selected_file[0]:
            result = QtWidgets.QMessageBox.question(self,
                                                    "Подтверждение",
                                                    "Вы действительно хотите использовать эту базу данных?",
                                                    buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                    defaultButton=QtWidgets.QMessageBox.No                            
                                                    )
            if result==QtWidgets.QMessageBox.Yes:
                
                self.config.store_value(cfg.DATABASE_FILE_KEY, selected_file[0])
                self.config.write_config()
                self.database.disconnect_from_database()
                self.database.connect_to_database()
                self.update()


    def closeEvent(self, event):
        """Перехватывает событие закрытия окна."""
        if self.backup_need:
        
            self.__backup()
            self.__backup_rotation()
        event.accept()

 
    def update(self, pbackup_need = False):
        """Обновляет содержимое браузера."""
        if pbackup_need:
        
            self.backup_need = True
        self.textBrowser.clear()
        self.__display_content(self.__load_data())
        

if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    main_window = CMainWindow()
    application.exec_()


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
          
