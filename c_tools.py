#!/usr/bin/python
## -*- coding: utf-8 -*-
"""Модуль всякой полезной всячины."""
import calendar
import c_constants as cnst

LAST_MONTH = 12

def get_months_last_date(pdate):
    """Возвращает первый день месяца"""
    return calendar.monthrange(pdate.year, pdate.month)[1]

def get_years_last_date(pdate):
    """Возвращает последний день года."""
    return calendar.monthrange(pdate.year, LAST_MONTH)[1]