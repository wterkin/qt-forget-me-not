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
        self.id = pid
        self.application_folder = papplication_folder
        uic.loadUi(self.application_folder / const.FORMS_FOLDER / const.EVENT_EDITOR_FORM, self)
        # *** Загрузим список типов событий
        self.load_event_types_list()
        # *** Загрузим список периодов
        self.load_periods_list()
        if self.id is not None:

            self.load_data()
            
            
        
    def construct_window(self):
        """Создает интерфейс окна."""
        # *** Наименование события
        window_left, window_top = tls.center_window(self, cnst.EVENT_EDITOR_WINDOW_WIDTH, cnst.EVENT_EDITOR_WINDOW_HEIGHT)
        window_geometry = f"{cnst.EVENT_EDITOR_WINDOW_WIDTH}x{cnst.EVENT_EDITOR_WINDOW_HEIGHT}+{window_left}+{window_top}"
        self.geometry(window_geometry)
        self.update_idletasks()

        # *** Наименование события
        self.event_name_frame = tk.Frame(self)
        self.event_name_entry = tk.Entry(self.event_name_frame,
                                         width=40)
        self.event_name_entry.pack(side=tk.RIGHT)
        self.event_name_entry.focus()
        self.event_name_label = tk.Label(self.event_name_frame,
                                         text="Название события",
                                         width=20) #  bg='black', fg='white', )
        self.event_name_label.pack(side=tk.LEFT)
        self.event_name_frame.pack(padx=10,
                                   pady=10)

        # *** Тип и период события
        self.options_labels_frame = tk.Frame(self)
        self.event_type_label = tk.Label(self.options_labels_frame,
                                         text="Тип события",
                                         width=20)
        self.event_type_label.pack(side=tk.LEFT)
        self.event_period_label = tk.Label(self.options_labels_frame,
                                         text="Периодичность события",
                                         width=20)
        self.event_period_label.pack(side=tk.RIGHT)
        self.options_labels_frame.pack()

        self.options_frame = tk.Frame(self)
        self.event_type_combo = ttk.Combobox(self.options_frame, width=30)
        self.event_type_combo.pack(side=tk.LEFT)
        self.event_period_combo = ttk.Combobox(self.options_frame, width=30)
        self.event_period_combo.pack(side=tk.LEFT)
        self.options_frame.pack(padx=10,
                                pady=10)
      
        # *** Дата события
        self.event_date_frame = tk.Frame(self)
        self.event_date_label = tk.Label(self.event_date_frame,
                                         text="Дата события",
                                         width=20)
        self.event_date_label.pack(side=tk.LEFT)

        self.event_date_entry = tkcal.DateEntry(self.event_date_frame,
                                    width=12,
                                    locale="ru_RU",
                                    borderwidth=2)        
        self.event_date_entry.pack(side=tk.RIGHT)
        self.event_date_frame.pack(padx=10,
                                   pady=10)

        # *** Кнопки 
        self.buttons_frame = tk.Frame(self)
        self.ok_button = tk.Button(command=self.save_data,
                                   master=self.buttons_frame,
                                   text="Принять")
        self.ok_button.pack(side=tk.LEFT)
        self.cancel_button = tk.Button(command=self.destroy,
                                       master=self.buttons_frame,
                                       text="Отмена")
        self.cancel_button.pack(side=tk.RIGHT)
        self.buttons_frame.pack(padx=10,
                                pady=10)
        self.update_idletasks()
                                
        
    
    def load_data(self):
        """Процедура загрузки данных в контролы."""
        event_name, event_date, self.event_type, self.event_period = self.database.get_event_data(self.id)
        self.event_name_entry.insert(tk.END, event_name)
        self.event_date_entry.set_date(event_date)
        # print("EVED:LD:type ", self.event_type)
        # print("EVED:LD:period ", self.event_period)
        
        self.event_type_combo.current(self.event_types_id_list.index(self.event_type))
        self.event_period_combo.current(self.event_period_id_list.index(self.event_period))

    
    def load_event_types_list(self):
        """Загружает список типов событий в listbox."""
        self.event_types_id_list, event_types_name_list = self.database.get_event_types_list()
        self.comboBox_EventType.clear()
        self.comboBox_EventType.addItems(event_types_name_list)
        #self.event_type_combo["values"] = event_types_name_list
    
    def load_periods_list(self):
        """Загружает список периодов в listbox."""
        self.event_period_id_list, event_period_name_list = self.database.get_periods_list()
        self.comboBox_EventPeriod.clear()
        self.comboBox_EventPeriod.addItems(event_period_name_list)
        #self.event_period_combo["values"] = event_period_name_list

    
    def save_data(self):
        """Сохраняет введённые данные."""
        event_date = datetime.strptime(self.event_date_entry.get(), "%d.%m.%Y")
        event_type = self.event_types_id_list[self.event_type_combo.current()]
        event_period = self.event_period_id_list[self.event_period_combo.current()]
        # print("EVED:SD:type ", event_type)
        # print("EVED:SD:period ", event_period)
      
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
    
    
