from nonebot_plugin_orm import Model
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class Detail(Model):
    __tablename__ = "Detail"
    id = Column(String(255), primary_key=True, nullable=True)  #id
    group_id = Column(String(255), nullable=True)  # summary
    user_id = Column(String(255), nullable=True)
    updated = Column(DateTime, nullable=True)
    text = Column(String(255), nullable=True)
    clip = Column(String(255), nullable=True)
    sentiment = Column(String(255), nullable=True)

class hot_history(Model):
    __tablename__ = "hot_history"
    id = Column(String(255), primary_key=True, nullable=True)
    group_id = Column(String(255), nullable=True)
    word = Column(String(255), nullable=True)
    frequency = Column(String(255), nullable=True)
    sentiment = Column(String(255), nullable=True)
    updated = Column(DateTime, nullable=True)

class Clip(Model):
    __tablename__ = "Clip"
    id = Column(String(255), primary_key=True, nullable=True)  #id
    group_id = Column(String(255), nullable=True)  # summary
    word = Column(String(255), nullable=True)
    frequency = Column(Integer, nullable=True)

class History(Model):
    __tablename__ = "History"
    id = Column(String(255), primary_key=True, nullable=True)  #id
    group_id = Column(String(255), nullable=True)  # summary
    user_id = Column(String(255), nullable=True)
    updated = Column(DateTime, nullable=True)
    text = Column(String(255), nullable=True)
    clip = Column(String(255), nullable=True)
    sentiment = Column(String(255), nullable=True)