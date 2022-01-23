from sqlalchemy import Column, DateTime, Integer, String, Boolean

from database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String)
    task_date = Column(DateTime)
    task_done = Column(Boolean, default=False)
