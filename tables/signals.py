from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Unicode,
    Boolean,
    Enum as EnumCol,
)
from sqlalchemy.orm import relationship
from enum import Enum

from . import BaseModel


class Levels(Enum):
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"


class Signal(BaseModel):
    __tablename__ = "signals"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    device = relationship("Device", foreign_keys=[device_id], lazy='subquery')

    duration = Column(Integer, default=60)
    active = Column(Boolean, default=False)
    level = Column(EnumCol(Levels))
    description = Column(Unicode(4096))
    solution = Column(Unicode(4096))

    code_id = Column(Integer, ForeignKey("codes.id"))
    code = relationship("Code", foreign_keys=[code_id])

    row = Column(Unicode(255), index=True)

    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
