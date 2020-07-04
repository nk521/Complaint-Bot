from datetime import datetime
from contextlib import contextmanager
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
)
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///db.sqlite3")
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
    identifier = Column(String, nullable=False)


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
    by_user_id = Column(
        Integer, ForeignKey("user.tg_id", ondelete="cascade"), nullable=False
    )
    for_group_id = Column(
        Integer, ForeignKey("group.tg_id", ondelete="cascade"), nullable=False
    )
    assigned_to = Column(
        Integer, ForeignKey("admin.id", ondelete="cascade"), nullable=False
    )
    group = relationship("Group", backref="threads")


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


Base.metadata.create_all(engine)
Session = sessionmaker(engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
