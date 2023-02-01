from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from tables import BaseModel


class SignalsLog(BaseModel):
    __tablename__ = "signals_log"

    id = Column(Integer, primary_key=True)
    signal_id = Column(Integer, ForeignKey("signals.id"))
    signal = relationship("Signal", foreign_keys=[signal_id], lazy='subquery')
    duration = Column(Integer)  # Длительность сигнала в секундах

    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
