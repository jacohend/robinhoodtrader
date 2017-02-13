# -*- coding: utf-8 -*-
from database import db
from sqlalchemy.dialects.postgresql import JSON, JSONB, ARRAY
from flask import abort

def redact(dictionary, ls):
    for blackout in ls:
        if blackout in dictionary.keys():
            dictionary[blackout] = None
    return dictionary

class Serialize():
    def to_dict(self, query_instance=None):
        if hasattr(self, '__table__'):
           return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
        else:
            cols = query_instance.column_descriptions
            return { cols[i]['name'] : self[i]  for i in range(len(cols))  }

    def from_dict(self, dict):
        for c in self.__table__.columns:
            setattr(self, c.name, dict[c.name])


class STRATEGY(db.Model, Serialize):
    __tablename__ = 'strategy'
    id = db.Column(db.Integer, primary_key=True)
    stock = db.COLUMN(db.TEXT)
    regression = db.COLUMN(db.TEXT)
    target_criteria = db.COLUMN(db.Float)
    action = db.COLUMN(db.Integer)
    created = db.Column(db.Integer)


class ACTION(db.Model, Serialize):
    __tablename__ = 'action'
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.TEXT)
    evidence = db.Column(db.TEXT)
    security = db.Column(db.TEXT)
    price = db.Column(db.Float)
    amount = db.Column(db.Integer)
    taken = db.Column(db.Integer)
 
