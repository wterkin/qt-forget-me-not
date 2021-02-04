#!/usr/bin/python
## -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса типа события."""

from sqlalchemy import Table, Column, String

import c_ancestor as anc

class CEventType(anc.CAncestor):
    """Класс типов событий."""

    __tablename__ = 'tbl_types'
    fname = Column(String,
                    nullable=False,
                    unique=True)
    fcolor = Column(String,
                    nullable=False)
    femodji = Column(String,
                     nullable=True)

    def __init__(self, pstatus, pname, pcolor, pemodji):
        """Конструктор"""
        super().__init__(pstatus)
        self.fname = pname
        self.fcolor = pcolor
        self.femodji = pemodji
        
    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Name:{self.fname},
                   Color:{self.fcolor},
                   Emodji:{self.femodji}"""

