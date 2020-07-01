from datetime import datetime
from sqlalchemy import (
    create_engine,
    declarative_base,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
)
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite3:///db.sqlite3")
Base = declarative_base()


class User(Base):
    """
    Represents a telegram user. No names are stored.
    """

    __tablename__ = "user"
    tg_id = Column(Integer, primary_key=True)
    is_superuser = Column(Boolean, default=False)
    is_balcklisted = Column(Boolean, default=False)


class Group(Base):
    """
    Represents a telegram group.
    """

    __tablename__ = "group"
    tg_id = Column(Integer, primary_key=True)
    identifier = Column(String, null=False)


class Admin(Base):
    """
    Register a certain user as an admin for a group.
    """

    __tablename__ = "admin"
    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("user.tg_id", ondelete="cascade"), nullable=False
    )
    groupid = Column(
        Integer, ForeignKey("group.tg_id", ondelete="cascade"), nullable=False
    )


class Thread(Base):
    """
    A complaint thread.
    """

    __tablename__ = "thread"
    id = Column(Integer, primary_key=True)
    for_group_id = Column(
        Integer, ForeignKey("group.tg_id", ondelete="cascade"), nullable=False
    )
    assigned_to = Column(
        Integer, ForeignKey("admin.id", ondelete="cascade"), nullable=False
    )


class HideFrom(Base):
    """
    Certain threads might need to be hidden from some people. For example if
    complaints are about a certain admin.
    """

    __tablename__ = "hidefrom"
    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("user.tg_id", ondelete="cascade"), nullable=False
    )
    thread_ = Column(
        Integer, ForeignKey("thread.id", ondelete="cascade"), nullable=False
    )


class Message(Base):
    """
    A log of messages sent to the bot in relation to a complaint.
    """

    __tablename__ = "message"
    contents = Column(BLOB)
    timestamp = Column(DateTime, default=datetime.utcnow)
    from_user_id = Column(
        Integer, ForeignKey("user.tg_id", ondelete="cascade"), nullable=False
    )
    thread_id = Column(
        Integer, ForeignKey("thread.id", ondelete="cascade"), nullable=False
    )


Base.metadata.create_all(engine)
Session = sessionmaker(engine)
