#!/usr/bin/python
## -*- coding: utf-8 -*-
"""Модуль класса периода события Alchemy"""

from sqlalchemy import Table, Column, String

import c_ancestor

class CPeriod(c_ancestor.CAncestor):
	
    __tablename__ = 'tbl_periods'
    fname = Column(String,
                   nullable=False)

    def __init__(self, pstatus, pname):
        """Конструктор."""
        super().__init__(pstatus)
        self.fname = pname
    
    def __repr__(self):
        return f"""{ancestor_repr}
				   Period:{self.fname}"""
