from sqlalchemy import Column,Integer,String, Boolean
from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Table(Base):
    __tablename__ = 'LIBRARY_DATA'

    id = Column(Integer, primary_key=True, nullable=False)
    book_title=Column(String, nullable=False)
    author=Column(String, nullable=False)
    student_id=Column(Integer, nullable=True)
    book_status = Column(String, default="unassigned",nullable=False)
    