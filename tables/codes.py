from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Unicode,
    Enum as EnumCol,
)
from sqlalchemy.orm import relationship, backref

from . import BaseModel
from enum import Enum


class Levels(Enum):
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"


class Code(BaseModel):
    __tablename__ = "codes"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), index=True)
    level = Column(EnumCol(Levels))
    description = Column(Unicode(4096))
    solution = Column(Unicode(4096))

    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    device = relationship("Device", foreign_keys=[device_id])

    signal_id = Column(Integer, ForeignKey("signals.id"))
    signal = relationship("Signal", foreign_keys=[signal_id])

    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
