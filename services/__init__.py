import logging

import repositories
from .devices import DeviceService
from .signals import SignalsService, SignalsLogService
from .codes import CodesService

# Repos
devices_repository = repositories.devices_repo
signals_repository = repositories.signals_repo
signals_log_repository = repositories.signals_log_repo
codes_repository = repositories.codes_repo

# Services
device_service = DeviceService(repository=devices_repository)
signals_service = SignalsService(repository=signals_repository)
signals_log_service = SignalsLogService(repository=signals_log_repository)
codes_service = CodesService(repository=codes_repository)

LOGGER = logging.getLogger()
