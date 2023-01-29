from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Unicode,
    Boolean,
)
from sqlalchemy.orm import relationship

from . import BaseModel


class Signal(BaseModel):
    __tablename__ = "signals"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    device = relationship("Device", foreign_keys=[device_id], lazy='subquery')

    duration = Column(Integer)
    active = Column(Boolean, default=False)

    code_id = Column(Integer, ForeignKey("codes.id"))
    code = relationship("Code", foreign_keys=[code_id])

    row = Column(Unicode(255), index=True)
    description = Column(Unicode(4096))

    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
