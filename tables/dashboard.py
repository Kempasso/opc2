from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Float,
    Boolean,
    Unicode,
)
from sqlalchemy.orm import relationship

from . import BaseModel


class Dashboard(BaseModel):
    __tablename__ = "dashboards"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    device = relationship("Device", foreign_keys=[device_id])
    online = Column(Boolean, default=False)
    temperature = Column(Float, nullable=True)

    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
