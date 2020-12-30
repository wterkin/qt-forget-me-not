"""Qt оболочка для forget-me-not."""
import sys
from pathlib import Path
from datetime import datetime
from PyQt5 import QtWidgets
from PyQt5 import uic


import c_config as cfg
import c_constants as const
import c_database as db

TABLE_COLUMNS_COUNT = 4

EMODJ_COLUMN = 0
TYPE_COLUMN = 1
DATE_COLUMN = 2
NAME_COLUMN = 3


class MainWindow(QtWidgets.QMainWindow):
    """Класс."""
    def fill_table_with_data(self, pdata):
        """ Заполняет таблицу данными """

        assert pdata is not None, "Assert: [tforms.fill_table_with_data]: \
            No <p_data> parameter specified!"

        self.QMainTable.setColumnCount(4)     # Устанавливаем три колонки
        self.QMainTable.setRowCount(len(pdata))        # и одну строку в таблице
        row_number = 0
        for data_row in pdata:

            emodji_item = QtWidgets.QTableWidgetItem(data_row[db.EVENT_LIST_CONVERTED_TYPE_EMODJI_FIELD])
            # emodji_item.setTextAlignment(Qt.AlignHCenter) # QtCore.
            # emodji_item.setForeground(QBrush(QColor(data_row[db.EVENT_LIST_CONVERTED_TYPE_COLOR_FIELD])))        
            self.QMainTable.setItem(row_number, EMODJ_COLUMN, emodji_item)

            date_item = QtWidgets.QTableWidgetItem(f"{data_row[db.EVENT_LIST_CONVERTED_DATE_FIELD]:%d.%m.%Y}")
            # date_item.setTextAlignment(QtCore.Qt.AlignHCenter)
            # date_item.setForeground(QBrush(QColor(data_row[db.EVENT_LIST_CONVERTED_TYPE_COLOR_FIELD])))
            self.QMainTable.setItem(row_number, DATE_COLUMN, date_item)
            
            type_item = QtWidgets.QTableWidgetItem(data_row[db.EVENT_LIST_CONVERTED_TYPE_NAME_FIELD])
            # type_item.setTextAlignment(QtCore.Qt.AlignHCenter)
            # type_item.setForeground(QBrush(QColor(data_row[db.EVENT_LIST_CONVERTED_TYPE_COLOR_FIELD])))
            self.QMainTable.setItem(row_number, TYPE_COLUMN, type_item)

            name_item = QtWidgets.QTableWidgetItem(data_row[db.EVENT_LIST_CONVERTED_NAME_FIELD])
            # name_item.setTextAlignment(QtCore.Qt.AlignHCenter)
            # name_item.setForeground(QBrush(QColor(data_row[db.EVENT_LIST_CONVERTED_TYPE_COLOR_FIELD])))
            self.QMainTable.setItem(row_number, NAME_COLUMN, name_item)
            #print("*** FTWD:data ", name_item, data_row[db.EVENT_LIST_CONVERTED_NAME_FIELD])
            
            
            row_number += 1
        self.QMainTable.resizeColumnsToContents()            
        self.QMainTable.setCurrentCell(0, 0)


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

    def __init__(self):
        """Конструктор класса."""
        super(MainWindow, self).__init__()
        self.application_folder = Path.cwd()
        uic.loadUi(self.application_folder / const.FORMS_FOLDER / const.MAIN_WINDOW_FORM, self)
        self.config = cfg.CConfiguration()
        self.database = db.CDatabase(self.config)
        if not self.is_database_exists():
        
            self.database.create_database()
        data = self.load_data()
        # self.QMainTable.setColumnCount(TABLE_COLUMNS_COUNT)
        # model = QStandartItemModel()
        # print("*** MN:INIT:FILL")
        self.fill_table_with_data(data)
        # print("*** MN:INIT:SHOW")
        self.show()




if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    application.exec_()
