#!/usr/bin/python
## -*- coding: utf-8 -*-
"""Модуль всякой полезной всячины."""
import calendar
import c_constants as cnst
import datetime as dt
from PyQt5 import QtWidgets

LAST_MONTH = 12

def get_months_last_date(pdate):
    """Возвращает последний день месяца"""
    return calendar.monthrange(pdate.year, pdate.month)[1]


def get_years_last_date(pdate):
    """Возвращает последний день года."""
    return calendar.monthrange(pdate.year, LAST_MONTH)[1]
    

def notice(parent,title,text):
    message_box = QtWidgets.QMessageBox(parent)       
    message_box.setWindowTitle(title)
    message_box.setText(text)
    message_box.addButton("Понятно.", QtWidgets.QMessageBox.AcceptRole)
    message_box.exec()



def message_box(parent,title,text):
    message_box = QtWidgets.QMessageBox(parent)       
    message_box.setWindowTitle(title)
    message_box.setText(text)
    message_box.addButton("Да", QtWidgets.QMessageBox.YesRole)
    message_box.addButton("Нет", QtWidgets.QMessageBox.NoRole)
    message_box.exec()
    button = message_box.clickedButton()
    role = message_box.buttonRole(button)
    if role == QtWidgets.QMessageBox.YesRole:
        return True
    else:
        return False


def shift_date(pdate, pdays):
    """Смещает дату на заданный интервал.
    >>> shift_date(dt.date(2021, 1, 1), 31)
    datetime.date(2021, 2, 1)"""
    time_delta = dt.timedelta(days=pdays)
    return pdate+time_delta
    