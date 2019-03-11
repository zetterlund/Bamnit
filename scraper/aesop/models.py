from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Integer, SmallInteger, String, Date, DateTime, Float, Boolean, Text, LargeBinary)
from scrapy.utils.project import get_project_settings

DeclarativeBase = declarative_base()


def db_connect():
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class ListingDB(DeclarativeBase):
    __tablename__ = "listing"

    id = Column(Integer, primary_key=True)
    aesop_id = Column('aesop_id', Integer)
    teacher = Column('teacher', String(256))
    position = Column('position', String(128))
    subject = Column('subject', String(128))
    campus = Column('campus', String(256))    
    begin_date = Column('begin_date', DateTime)
    end_date = Column('end_date', DateTime)    
    multiday = Column('multiday', Boolean)    
    fullday = Column('fullday', String(128))
    notes = Column('notes', Text)
    date_posted = Column('date_posted', DateTime)
    date_removed = Column('date_removed', DateTime)
    language = Column('language', String(64))
    grade = Column('grade', String(64))
    notification_sent = Column('notification_sent', Boolean)