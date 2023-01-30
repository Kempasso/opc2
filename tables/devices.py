from sqlalchemy import Column, DateTime, ForeignKey, Integer, Unicode, Float
from sqlalchemy.orm import relationship, relation

from . import BaseModel


class Device(BaseModel):
    __tablename__ = "devices"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), index=True)
    serial = Column(Unicode(255), index=True)
    description = Column(Unicode(4096))

    temperature = Column(Float)

    codes = relation("Code", remote_side=[id], uselist=True)

    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    # FOR HARDCODE PARAMS
    model = Column(Unicode(255))
    vendor = Column(Unicode(255))
    responsible = Column(Unicode(255))
