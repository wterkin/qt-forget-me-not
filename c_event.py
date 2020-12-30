#!/usr/bin/python
## -*- coding: utf-8 -*-
"""Модуль класса события."""

from sqlalchemy import Table, Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship

import c_ancestor
import c_eventtype
import c_period


class CEvent(c_ancestor.CAncestor):
    """Класс события."""
    
    __tablename__ = 'tbl_events'
    fname = Column(String, nullable=False)
    fday = Column(Integer, nullable=False)
    fmonth = Column(Integer, nullable=False)    
    fyear = Column(Integer, nullable=False)    
    ftype = Column(Integer, ForeignKey(c_eventtype.CEventType.id))
    atype = relationship(c_eventtype.CEventType)
    fperiod = Column(Integer, ForeignKey(c_period.CPeriod.id))
    aperiod = relationship(c_period.CPeriod)

    def __init__(self, pstatus, pname, pdate, ptype, pperiod):
        """Конструктор."""

        super().__init__(pstatus)
        self.fname = pname
        self.fday = pdate.day
        self.fmonth = pdate.month
        self.fyear = pdate.year
        self.ftype = ptype
        self.fperiod = pperiod

    def __repr__(self):
        
        return f"""Name:{self.fname}, 
                   Date:{self.fday}.{self.fmonth}.{self.fyear}, 
                   Type:{self.ftype}, Period:{self.ftype}, {super().__repr__()}"""


