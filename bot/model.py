# from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column
# from sqlalchemy import Boolean
# from sqlalchemy import DateTime
# from sqlalchemy import ForeignKey
# from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import String
# from sqlalchemy import JSON
from sqlalchemy import UniqueConstraint
from sqlalchemy import func
# from sqlalchemy_fulltext import FullText
# from sqlalchemy.dialects.mysql import DATETIME as MySqlDateTime
from sqlalchemy.exc import InvalidRequestError

from bot.extensions import db


class BaseModel(db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    @classmethod
    def count(cls, *args):
        """Returns count"""
        return db.session.query(func.count(cls.id)).filter(*args).scalar()

    @classmethod
    def query(cls, **kwargs):
        """Return an SQLAlchemy query object."""
        return db.session.query(cls, **kwargs)

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def commit(self):
        try:
            db.session.commit()
        except:  # noqa
            try:
                db.session.rollback()
            except InvalidRequestError:
                pass  # nothing to rollback
            raise

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            self.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        if commit:
            self.commit()
        return

    @classmethod
    def fetch_by_id(cls, id):
        return cls.query().filter(cls.id == id).one_or_none()


class Restaurant(BaseModel):
    __tablename__ = 'restaurants'

    id = Column(String(length=36), default=uuid4, primary_key=True)
    name = Column(String(length=255))
    chat_id = Column(Integer(), index=True)
    lhde = Column(String(length=36))
    pde = Column(String(length=36))
    fdde = Column(String(length=36))

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Restaurant({name}-{chat_id})>'.format(
            name=self.name, chat_id=self.chat_id)

    @staticmethod
    def get_all(chat_id):
        restaurants = Restaurant.query().filter(
            Restaurant.chat_id == chat_id
        ).all()
        return restaurants

    @staticmethod
    def get_by_id(id):
        restaurant = Restaurant.query().filter(
            Restaurant.id == id,
        ).first()
        return restaurant


class Flow(BaseModel):
    __tablename__ = 'flows'

    id = Column(String(length=36), default=uuid4, primary_key=True)
    chat_id = Column(Integer(), index=True)
    flow_name = Column(String(length=155))
    state_id = Column(Integer())
    restaurant_id = Column(String(length=36))
    __table_args__ = (
        UniqueConstraint('chat_id', 'flow_name', name='uix_flow'), )

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Flow({name}-{chat_id})>'.format(
            name=self.flow_name, chat_id=self.chat_id)

    @staticmethod
    def get_by_name(chat_id, flow_name):
        flow = Flow.query().filter(
            Flow.chat_id == chat_id,
            Flow.flow_name == flow_name,
        ).first()
        return flow

    @staticmethod
    def get_state(chat_id, flow_name):
        flow = Flow.query().filter(
            Flow.chat_id == chat_id,
            Flow.flow_name == flow_name,
        ).first()
        return flow.state

    @staticmethod
    def check_flow_name(chat_id):
        flows = Flow.query().filter(
            Flow.chat_id == chat_id,
        ).all()
        active_flow = None
        for f in flows:
            if f.state_id != 0:
                active_flow = f.flow_name
                break
        return active_flow

    @staticmethod
    def check_flow_exists(chat_id, flow_name):
        flow = Flow.query().filter(
            Flow.chat_id == chat_id,
            Flow.flow_name == flow_name,
        ).first()
        return True if flow else False
