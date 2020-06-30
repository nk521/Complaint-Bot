from datetime import datetime
from sqlalchemy import (
    create_engine,
    declarative_base,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.dialects.sqlite import BLOB

engine = create_engine("sqlite3:///db.sqlite3")
Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    tg_id = Column(Integer, primary_key=True)


class Group(Base):
    __tablename__ = "group"
    tg_id = Column(Integer, primary_key=True)


class Admin(Base):
    __tablename__ = "admin"
    user_id = Column(
        Integer, ForeignKey("user.tg_id", ondelete="cascade"), nullable=False
    )
    groupid = Column(
        Integer, ForeignKey("group.tg_id", ondelete="cascade"), nullable=False
    )


class Thread(Base):
    __tablename__ = "thread"
    id = Column(Integer, primary_key=True)


class Message(Base):
    __tablename__ = "message"
    contents = Column(BLOB)
    timestamp = Column(DateTime, default=datetime.utcnow)
    from_user_id = Column(
        Integer, ForeignKey("user.tg_id", ondelete="cascade"), nullable=False
    )
    for_group_id = Column(
        Integer, ForeignKey("group.tg_id", ondelete="cascade"), nullable=False
    )
    thread_id = Column(
        Integer, ForeignKey("thread.id", ondelete="cascade"), nullable=False
    )
