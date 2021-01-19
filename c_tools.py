#!/usr/bin/python
## -*- coding: utf-8 -*-
"""Модуль всякой полезной всячины."""
import calendar
import c_constants as cnst
import datetime as dt

LAST_MONTH = 12

def get_months_last_date(pdate):
    """Возвращает первый день месяца"""
    return calendar.monthrange(pdate.year, pdate.month)[1]

def get_years_last_date(pdate):
    """Возвращает последний день года."""
    return calendar.monthrange(pdate.year, LAST_MONTH)[1]
    

def shift_date(pdate, pdays):
    """Смещает дату на заданный интервал.
    >>> shift_date(dt.date(2021, 1, 1), 31)
    datetime.date(2021, 2, 1)"""
    time_delta = dt.timedelta(days=pdays)
    return pdate+time_delta
    