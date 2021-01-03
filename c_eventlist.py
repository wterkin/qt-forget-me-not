#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk

import c_constants as cnst
import c_eventeditor as eved
import c_tools as tls

class EventList(tk.Toplevel):
    """Класс окна списка событий."""
    def __init__(self, pmaster, pdatabase, **kwargs):
        """Конструктор."""
        tk.Toplevel.__init__(self, pmaster, **kwargs)
        self.master = pmaster
        self.database = pdatabase
        self.construct_window()
        self.load_data()
        # *** Показываем окно
        self.transient(self.master)
        self.focus_set()
        self.grab_set()
        self.master.wait_window(self)

   
    def construct_window(self):
        """Создает интерфейс окна."""
        self.title(cnst.EVENT_LIST_WINDOW_TITLE)
        window_left, window_top = tls.center_window(self, cnst.EVENT_LIST_WINDOW_WIDTH, cnst.EVENT_LIST_WINDOW_HEIGHT)
        window_geometry = f"{cnst.EVENT_LIST_WINDOW_WIDTH}x{cnst.EVENT_LIST_WINDOW_HEIGHT}+{window_left}+{window_top}"
        self.geometry(window_geometry)
        self.update_idletasks()

        # *** Фрейм кнопок
        self.list_buttons_frame = tk.Frame(self)
        self.add_button = tk.Button(command=self.insert_event,
                                    master=self.list_buttons_frame,
                                    text="Добавить")
        self.add_button.pack(side=tk.LEFT)
        self.edit_button = tk.Button(command=self.update_event,
                                     master=self.list_buttons_frame,
                                     text="Редактировать")
        self.edit_button.pack(side=tk.LEFT)  # tk.RIGHT)
        self.delete_button = tk.Button(command=self.delete_event,
                                       master=self.list_buttons_frame,
                                       text="Удалить")
        self.delete_button.pack(side=tk.LEFT)  # tk.RIGHT)
        self.close_button = tk.Button(command=self.destroy,
                                      master=self.list_buttons_frame,
                                      text="Закрыть")
        self.close_button.pack(side=tk.RIGHT)
        self.list_buttons_frame.pack(side = tk.TOP)  # padx=10, pady=10
        
        # *** Фрейм списка событий
        self.events_frame = tk.Frame(self)
        self.events_box = tk.Listbox(self.events_frame)  #! , width=20, height=4)
        self.events_box.pack(expand=1, fill=tk.BOTH) # padx=10, pady=10
        self.events_frame.pack(expand=1, fill=tk.BOTH)
        self.update_idletasks()
        
        # print("EVLST:CONS:GEO", self.master.get_master().geometry())
   

    def delete_event(self):
        """Удаляет выбранное событие."""
        selected_items = self.events_box.curselection()
        if len(selected_items) > 0:

            event_ident = self.event_id_list[selected_items[0]]
            self.database.update_event(event_ident)
            self.load_data()

    
    def insert_event(self):
        """Добавляет новое событие в базу."""
        event_editor = eved.EventEditor(self,
                                        pdatabase=self.database,
                                        pid=None)
        self.load_data()


    def load_data(self):
        """Обновляет данные в списке."""
        self.events_box.delete(0, tk.END)
        self.event_id_list, self.event_name_list = self.database.get_events_list()
        for event_name in self.event_name_list:
            self.events_box.insert(tk.END, event_name)


    def update_event(self):
        """Изменяет уже существующее событие."""
        # FixMe: вот тут не передаются данные в редактор!
        selected_items = self.events_box.curselection()
        if len(selected_items) > 0:
            event_ident = self.event_id_list[selected_items[0]]
            event_editor = eved.EventEditor(self,
                                            pdatabase=self.database,
                                            pid=event_ident)
            self.load_data()

    
if __name__ == '__main__':
    master = tk.Tk()
    event_list = EventList(master)
    master.mainloop()
