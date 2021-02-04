#!/usr/bin/python
## -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса-предка классов таблиц."""

from sqlalchemy import Table, Column, Integer, MetaData
from sqlalchemy.ext.declarative import declarative_base

convention = {
              "all_column_names": lambda constraint,
                                  table: "_".join([
                                    column.name for column in constraint.columns.values()
                                  ]),
              "ix": "ix__%(table_name)s__%(all_column_names)s",
              "uq": "uq__%(table_name)s__%(all_column_names)s",
              "cq": "cq__%(table_name)s__%(constraint_name)s",
              "fk": ("fk__%(table_name)s__%(all_column_names)s__"
                     "%(referred_table_name)s"),
              "pk": "pk__%(table_name)s"       
}

meta_data = MetaData(naming_convention = convention)
Base = declarative_base(metadata=meta_data)

class CAncestor(Base):
    """Класс-предок всех классов-таблиц Alchemy."""
    __abstract__ = True
    id = Column(Integer,
                autoincrement=True,
                nullable=False,
                primary_key=True,
                unique=True)
    fstatus = Column(Integer,
                     nullable=False,
                     )

    def __init__(self, pstatus):
        """Конструктор."""
        self.fstatus = pstatus
        
    def __repr__(self):
        
        return f"""ID:{self.id},
                   Status:{self.fstatus}"""
    
