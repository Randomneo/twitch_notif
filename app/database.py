from typing import Sequence
from uuid import uuid4
import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, Session, relationship
from sqlalchemy import select

class Base(DeclarativeBase):
    ...


class User(Base):
    __tablename__ = 'user'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    send_code = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class Channel(Base):
    __tablename__ = 'channel'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey(User.id), nullable=False)
    active: sqlalchemy.Column[bool] = sqlalchemy.Column(
        sqlalchemy.Boolean,
        default=False,
    )
    user = relationship(User, backref='channels')


engine = sqlalchemy.create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)


def add_channel(id, user_id):
    with Session(engine) as session:
        session.add(Channel(id=id, user_id=user_id))
        session.commit()


def get_send_code(user_id):
    with Session(engine) as session:
        return session.execute(
            select(User).where(User.id==user_id)
        ).scalar_one().send_code


def get_or_create_user(id):
    with Session(engine, expire_on_commit=False) as session:
        user = session.execute(sqlalchemy.select(User).where(User.id == id))\
               .scalar_one_or_none()

        if not user:
            user = User(id=id, send_code=str(uuid4()))
            session.add(user)
            session.commit()

    return user


def channels(user_id):
    query = sqlalchemy.select(Channel).where(user_id==user_id)
    with Session(engine) as session:
        return session.scalars(query).all()

def channels_by_code(code):
    with Session(engine) as session:
        return session.scalars(
            sqlalchemy.Select(Channel)
            .join(User)
            .where(
                User.send_code == code,
                Channel.active == True,
            )
        ).all()


def set_state(id, active):
    with Session(engine) as session:
        session.execute(sqlalchemy.update(Channel).where(Channel.id==id).values(active=active))
        session.commit()
