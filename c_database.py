#!/usr/bin/python
## -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, or_

import datetime as dtime
from datetime import datetime as dt

import c_ancestor
import c_config
import c_constants as const
import c_eventtype
import c_event  
import c_period
import c_tools as tls    

EVENT_LIST_NAME_FIELD = 0
EVENT_LIST_DAY_FIELD = 1
EVENT_LIST_MONTH_FIELD = 2
EVENT_LIST_YEAR_FIELD = 3
EVENT_LIST_TYPE_ID_FIELD = 4
EVENT_LIST_PERIOD_ID_FIELD = 5
EVENT_LIST_TYPE_NAME_FIELD = 6
EVENT_LIST_TYPE_COLOR_FIELD = 7
EVENT_LIST_TYPE_EMODJI_FIELD = 8

EVENT_LIST_CONVERTED_NAME_FIELD = 0
EVENT_LIST_CONVERTED_TYPE_ID_FIELD = 1
EVENT_LIST_CONVERTED_PERIOD_ID_FIELD = 2
EVENT_LIST_CONVERTED_TYPE_NAME_FIELD = 3
EVENT_LIST_CONVERTED_TYPE_COLOR_FIELD = 4
EVENT_LIST_CONVERTED_TYPE_EMODJI_FIELD = 5
EVENT_LIST_CONVERTED_DATE_FIELD = 6

QUERY_MONTHLY_DATA = 0
QUERY_YEARLY_DATA = 1

STATUS_INACTIVE = 0
STATUS_ACTIVE = 1

class CDatabase(object):
    """Класс осуществляет работу с БД."""
    def __init__(self, pconfig):
        """Конструктор."""
        self.config = pconfig
        self.engine = create_engine('sqlite:///'+self.config.restore_value(c_config.DATABASE_FILE_KEY))
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()
        c_ancestor.Base.metadata.bind = self.engine


    def convert_monthly_tuple(self, pevent_super_tuple, pnew_date):
        """Конвертирует кортеж в список, подставляя значения года и месяца из даты."""
        event_super_list = []
        for event_tuple in pevent_super_tuple:

            event_list = list(event_tuple)
            event_list[EVENT_LIST_YEAR_FIELD] = pnew_date.year
            event_list[EVENT_LIST_MONTH_FIELD] = pnew_date.month
            event_date = dtime.date(event_list[EVENT_LIST_YEAR_FIELD], 
                                    event_list[EVENT_LIST_MONTH_FIELD], 
                                    event_list[EVENT_LIST_DAY_FIELD])
            event_list.pop(EVENT_LIST_YEAR_FIELD)
            event_list.pop(EVENT_LIST_MONTH_FIELD)
            event_list.pop(EVENT_LIST_DAY_FIELD)
            event_list.append(event_date)
            # print("$$$$ ", event_list)
            event_super_list.append(event_list)
        return event_super_list    


    def convert_one_shot_tuple(self, pevent_super_tuple):
        """Конвертирует кортеж в список, подставляя значения года и месяца из даты."""
        event_super_list = []
        for event_tuple in pevent_super_tuple:

            event_list = list(event_tuple)
            event_date = dtime.date(event_list[EVENT_LIST_YEAR_FIELD], 
                                    event_list[EVENT_LIST_MONTH_FIELD], 
                                    event_list[EVENT_LIST_DAY_FIELD])
            event_list.pop(EVENT_LIST_YEAR_FIELD)
            event_list.pop(EVENT_LIST_MONTH_FIELD)
            event_list.pop(EVENT_LIST_DAY_FIELD)
            event_list.append(event_date)
            # print("@@@@@ ", event_list)
            event_super_list.append(event_list)
        return event_super_list    


    def convert_yearly_tuple(self, pevent_super_tuple, pnew_date):
        """Конвертирует кортеж в список, подставляя значения года и месяца из даты."""
        event_super_list = []
        for event_tuple in pevent_super_tuple:

            event_list = list(event_tuple)
            event_list[EVENT_LIST_YEAR_FIELD] = pnew_date.year
            event_date = dtime.date(event_list[EVENT_LIST_YEAR_FIELD], 
                                    event_list[EVENT_LIST_MONTH_FIELD], 
                                    event_list[EVENT_LIST_DAY_FIELD])
            event_list.pop(EVENT_LIST_YEAR_FIELD)
            event_list.pop(EVENT_LIST_MONTH_FIELD)
            event_list.pop(EVENT_LIST_DAY_FIELD)
            event_list.append(event_date)
            # print("##### ", event_list)
            event_super_list.append(event_list)
        return event_super_list    


    def create_database(self):
        """Создает или изменяет БД в соответствии с описанной в классах структурой."""
        c_ancestor.Base.metadata.create_all()
        count = self.session.query(c_eventtype.CEventType).count()
        if count == 0:

            self.fill_event_types_table()
        count = self.session.query(c_period.CPeriod).count()
        if count == 0:

            self.fill_periods_table()


    def delete_event(self, pid):
        """Удаляет уже существующее событие в БД."""
        event_data = self.session.query(c_event.CEvent).filter_by(id=pid)
        event_data.update({c_event.CEvent.fstatus:STATUS_INACTIVE}, synchronize_session = False)
        self.session.commit()


    def fill_event_types_table(self):
        """Заполняет пустую таблицу справочника типов событий значениями."""
        event_type = c_eventtype.CEventType(1, "День памяти ", "#8db0bd", "☦️")
        self.session.add(event_type)
        event_type = c_eventtype.CEventType(1, "День рождения ", "#ecc176", "🎂")
        self.session.add(event_type)
        event_type = c_eventtype.CEventType(1, "Памятная дата - ", "#02b6ec", "📆")
        self.session.add(event_type)
        event_type = c_eventtype.CEventType(1, "Напоминание: ", "#6dec04", "🔔")
        self.session.add(event_type)
        self.session.commit()


    def fill_periods_table(self):
        """Заполняет пустую таблицу справочника периодов значениями."""
        period_type = c_period.CPeriod(1, "Ежемесячное событие")
        self.session.add(period_type)
        period_type = c_period.CPeriod(1, "Ежегодное событие")
        self.session.add(period_type)
        period_type = c_period.CPeriod(1, "Единовременное событие")
        self.session.add(period_type)
        self.session.commit()


    def get_actual_monthly_events(self):
        """Возвращает список ежемесячных событий, актуальных в периоде от текущей даты до текущей + период видимости."""
        # *** Дата c = текущая дата 
        date_from = dt.now().date()
        # *** Дата по = Дата с + период видимости
        date_to =  date_from + dtime.timedelta(days=int(self.config.restore_value(c_config.MONITORING_PERIOD_KEY)))
        # *** Если дата по в следующем месяце
        if date_to.month != date_from.month:
        
            # ***  Разделяем период на два отрезка - от текущей даты до конца м-ца 
            last_day = tls.get_months_last_date(date_from)
            this_month_date_to = dtime.datetime(date_from.year, date_from.month, last_day)
            # *** И от нач. м-ца до даты по 
            next_month_date_from = this_month_date_to + dtime.timedelta(days=1)
            # *** Делаем выборку за текущий месяц
            queried_data1=self.universal_query(date_from.day, 0, this_month_date_to.day, 0, const.EVENT_MONTH_PERIOD, QUERY_MONTHLY_DATA)
            # *** Конвертируем кортеж в список и подставляем текущий месяц и год
            queried_data1 = self.convert_monthly_tuple(queried_data1, this_month_date_to)
            
            # *** Делаем выборку за следующий месяц
            queried_data2 = self.universal_query(next_month_date_from.day, 0, date_to.day, 0, const.EVENT_MONTH_PERIOD, QUERY_MONTHLY_DATA)
            # *** Конвертируем кортеж в список и подставляем следующий месяц и год
            queried_data2 = self.convert_monthly_tuple(queried_data2, next_month_date_from)
            # *** Сливаем выборки
            queried_data1.extend(queried_data2)
            return queried_data1
        else:

            # *** Иначе делаем одну выборку
            queried_data = self.universal_query(date_from.day, 0, date_to.day, 0, const.EVENT_MONTH_PERIOD, QUERY_MONTHLY_DATA)
            # *** Конвертируем кортеж в список и подставляем текущий месяц и год
            queried_data = self.convert_monthly_tuple(queried_data, date_from)
            return queried_data
        

    def get_actual_one_shot_events(self):
        """Возвращает список одноразовых событий, актуальных в периоде от текущей даты до текущей + период видимости."""
        # *** Дата с..
        date_from = dt.now().date()
        # *** Дата по..
        date_to =  date_from + dtime.timedelta(days=int(self.config.restore_value(c_config.MONITORING_PERIOD_KEY)))
        # *** Если дата по в следующем году разделяем период на два отрезка - от текущей даты до конца года
        if date_to.year != date_from.year:
            
            last_day = tls.get_years_last_date(date_from)
            this_year_date_to = dtime.datetime(date_from.year, date_from.month, last_day)
            
            # *** И от нач. года до даты по 
            next_year_date_from = this_year_date_to + dtime.timedelta(days=1)
            queried_data1 = self.universal_query(date_from.day, date_from.month, this_year_date_to.day, this_year_date_to.month, const.EVENT_YEAR_PERIOD, QUERY_YEARLY_DATA)
            queried_data1 = self.convert_one_shot_tuple(queried_data1)
            # Вторая выборка
            queried_data2 = self.universal_query(next_year_date_from.day, next_year_date_from.month, date_to.day, date_to.month, const.EVENT_YEAR_PERIOD, QUERY_YEARLY_DATA)
            queried_data2 = self.convert_one_shot_tuple(queried_data2)
            # *** Сливаем обе выборки
            queried_data1.extend(queried_data2)
            return queried_data1
        if date_to.month != date_from.month:
        
            # ***  Разделяем период на два отрезка - от текущей даты до конца м-ца 
            last_day = tls.get_months_last_date(date_from)
            this_month_date_to = dtime.datetime(date_from.year, date_from.month, last_day)
            next_month_date_from = this_month_date_to + dtime.timedelta(days=1)
            queried_data1 = self.universal_query(date_from.day, date_from.month, this_month_date_to.day, this_month_date_to.month, const.EVENT_ONE_SHOT, QUERY_YEARLY_DATA)
            queried_data1 = self.convert_yearly_tuple(queried_data1, date_from)
            # *** И от нач. м-ца до даты по 
            queried_data2 = self.universal_query(next_month_date_from.day, next_month_date_from.month, date_to.day, date_to.month, const.EVENT_ONE_SHOT, QUERY_YEARLY_DATA)
            queried_data2 = self.convert_yearly_tuple(queried_data2, next_month_date_from)
            queried_data1.extend(queried_data2)
            return queried_data1

        queried_data=self.universal_query(date_from.day, date_from.month, date_to.day, date_to.month, const.EVENT_ONE_SHOT, QUERY_YEARLY_DATA)
        queried_data = self.convert_yearly_tuple(queried_data, date_from)
        return queried_data


    def get_actual_yearly_events(self):
        """Возвращает список ежегодных событий, актуальных в периоде от текущей даты до текущей + период видимости."""
        # *** Дата с..
        date_from = dt.now().date()
        # *** Дата по..
        date_to = date_from + dtime.timedelta(days=int(self.config.restore_value(c_config.MONITORING_PERIOD_KEY)))
        # print("*** DB:GAY:1")
        # *** Если дата по в следующем году 
        if date_to.year != date_from.year:
            
            # *** То разделяем период на два отрезка - от текущей даты до конца года 
            last_day = tls.get_years_last_date(date_from)
            this_year_date_to = dtime.datetime(date_from.year, date_from.month, last_day)
            
            # и от нач. года до даты по 
            next_year_date_from = this_year_date_to + dtime.timedelta(days=1)
            # *** делаем две выборки
            queried_data1=self.universal_query(date_from.day, date_from.month, this_year_date_to.day, this_year_date_to.month, const.EVENT_YEAR_PERIOD, QUERY_YEARLY_DATA)
            # *** Конвертируем кортеж в список и подставляем текущий год
            queried_data1 = self.convert_yearly_tuple(queried_data1, this_year_date_to)
            # Вторая выборка
            queried_data2=self.universal_query(next_year_date_from.day, next_year_date_from.month, date_to.day, date_to.month, const.EVENT_YEAR_PERIOD, QUERY_YEARLY_DATA)
            # *** Конвертируем кортеж в список и подставляем следующий год
            queried_data2 = self.convert_yearly_tuple(queried_data2, next_year_date_from)
            # *** Сливаем обе выборки
            queried_data1.extend(queried_data2)
            return queried_data1
        # else:
            
        # *** Если дата по в следующем месяце
        if date_to.month != date_from.month:
        
            # ***  Разделяем период на два отрезка - от текущей даты до конца м-ца 
            last_day = tls.get_months_last_date(date_from)
            this_month_date_to = dtime.datetime(date_from.year, date_from.month, last_day)
            # *** И от нач. м-ца до даты по 
            next_month_date_from = this_month_date_to + dtime.timedelta(days=1)
            print("*** DB:GAY:dt ", date_from, this_month_date_to)
            queried_data1 = self.universal_query(date_from.day, date_from.month, this_month_date_to.day, this_month_date_to.month, const.EVENT_YEAR_PERIOD, QUERY_YEARLY_DATA)
            queried_data1 = self.convert_yearly_tuple(queried_data1, date_from)
            print("*** DB:GAY:dt ", next_month_date_from, date_to)
            queried_data2 = self.universal_query(next_month_date_from.day, next_month_date_from.month, date_to.day, date_to.month, const.EVENT_YEAR_PERIOD, QUERY_YEARLY_DATA)
            queried_data2 = self.convert_yearly_tuple(queried_data2, next_month_date_from)
            
            queried_data1.extend(queried_data2)
            return queried_data1

        queried_data=self.universal_query(date_from.day, date_from.month, date_to.day, date_to.month, const.EVENT_YEAR_PERIOD, QUERY_YEARLY_DATA)
        queried_data = self.convert_yearly_tuple(queried_data, date_from)
        return queried_data
            

    def get_event_data(self, pid): # +
        """Возвращает данные события."""
        event_data = self.session.query(c_event.CEvent.fname,
                                        c_event.CEvent.fyear,
                                        c_event.CEvent.fmonth,
                                        c_event.CEvent.fday,
                                        c_event.CEvent.ftype,
                                        c_event.CEvent.fperiod).\
                                  filter_by(id=pid).first()
        return (event_data.fname,
                dtime.datetime(event_data.fyear,
                               event_data.fmonth,
                               event_data.fday),
                event_data.ftype,
                event_data.fperiod)


    def get_event_types_list(self): # +
        """Возвращает список ID и наименований типов событий."""
        event_types_name_list = list()
        event_types_id_list = list()
        queried_data = self.session.query(c_eventtype.CEventType).order_by(c_eventtype.CEventType.fname)
        for event_type in queried_data:
            
            event_types_name_list.append(event_type.fname)
            event_types_id_list.append(event_type.id)
        return event_types_id_list, event_types_name_list


    def get_event_types_objects_list(self):
        """Возвращает список объектов класса CEventType."""
        return self.session.query(c_eventtype.CEventType).order_by(c_eventtype.CEventType.fname)


    def get_periods_list(self): # +
        """Возвращает список ID и наименований периодов."""
        periods_name_list = []
        periods_id_list = []
        queried_data = self.session.query(c_period.CPeriod).order_by(c_period.CPeriod.id)
        for period in queried_data:
            
            periods_name_list.append(period.fname)
            periods_id_list.append(period.id)
        return periods_id_list, periods_name_list
    
    
    def get_events_list(self): # +
        """Возвращает события из базы."""
        event_name_list = []
        event_id_list = []
        query = self.session.query(c_event.CEvent.id, c_event.CEvent.fname, c_eventtype.CEventType.fname)
        query = query.join(c_eventtype.CEventType)
        query = query.filter(c_event.CEvent.fstatus>STATUS_INACTIVE) 
        query = query.order_by(c_eventtype.CEventType.fname, c_event.CEvent.fname)
        query = query.all()
        for event_id, event_name, event_type_name in query:
            
            event_name_list.append(f"{event_type_name}{const.TYPE_SEPARATOR}{event_name}")
            event_id_list.append(event_id)
        return event_id_list, event_name_list


    def delete_event(self, pid): # +
        """Удаляет уже существующее событие в БД."""
        event_data = self.session.query(c_event.CEvent).filter_by(id=pid)
        event_data.update({c_event.CEvent.fstatus: STATUS_INACTIVE}, synchronize_session = False)
        self.session.commit()


    def insert_event(self, pname, pdate, ptype, pperiod): # +
        """Добавляет новое событие в БД."""
        event = c_event.CEvent(1, pname, pdate, ptype, pperiod)
        self.session.add(event)
        self.session.commit()


    def universal_query(self, pday_from, pmonth_from, pday_to, pmonth_to, pperiod, pquery_type):
        """Процедура выбирает данные из БД."""
        queried_data = self.session.query(c_event.CEvent.fname,
                                          c_event.CEvent.fday,
                                          c_event.CEvent.fmonth,
                                          c_event.CEvent.fyear,
                                          c_event.CEvent.ftype,
                                          c_event.CEvent.fperiod,
                                          c_eventtype.CEventType.fname,
                                          c_eventtype.CEventType.fcolor,
                                          c_eventtype.CEventType.femodji)
        queried_data = queried_data.join(c_eventtype.CEventType)

        if pquery_type == QUERY_MONTHLY_DATA:
        
            queried_data = queried_data.filter(c_event.CEvent.fperiod==pperiod, 
                                               and_(c_event.CEvent.fday>=pday_from,
                                               and_(c_event.CEvent.fday<=pday_to,
                                               and_(c_event.CEvent.fstatus>STATUS_INACTIVE))))
            queried_data = queried_data.order_by(c_event.CEvent.fday)
        else:
        
            queried_data = queried_data.filter(c_event.CEvent.fperiod==pperiod, 
                                               and_(c_event.CEvent.fday>=pday_from,
                                               and_(c_event.CEvent.fmonth>=pmonth_from,
                                               and_(c_event.CEvent.fday<=pday_to,
                                               and_(c_event.CEvent.fmonth<=pmonth_to,
                                               and_(c_event.CEvent.fstatus>STATUS_INACTIVE))))))

            queried_data = queried_data.order_by(c_event.CEvent.fmonth, c_event.CEvent.fday)
        return queried_data.all()

        
    def update_event(self, pid, pname, pdate, ptype, pperiod): # +
        """Изменяет уже существующее событие в БД."""
        event_data = self.session.query(c_event.CEvent).filter_by(id=pid)
        event_data.update({c_event.CEvent.fname:pname,
                           c_event.CEvent.fyear:pdate.year,
                           c_event.CEvent.fmonth:pdate.month,
                           c_event.CEvent.fday:pdate.day,
                           c_event.CEvent.ftype:ptype,
                           c_event.CEvent.fperiod:pperiod}, synchronize_session = False)
        self.session.commit()
