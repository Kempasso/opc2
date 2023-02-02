from sqlalchemy.orm import declarative_base

BaseModel = declarative_base()

# Main app models
from .codes import Code, Levels as CodeLevels
from .devices import Device
from .signals import Signal, Levels as SignalLevels
from .signals_log import SignalsLog
