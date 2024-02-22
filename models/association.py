from sqlalchemy import Table, Column, String, ForeignKey
from core import Base

# Промежуточная таблица для связи многие ко многим между Operator и Event
user_event_association = Table('users_events', Base.metadata,
                               Column('user_id', String, ForeignKey('users.id'), primary_key=True),
                               Column('event_id', String, ForeignKey('events.id'), primary_key=True)
                               )
