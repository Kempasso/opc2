from dataclasses import dataclass

from repositories.base import BaseRepo
from repositories.mixins import (
    CreateMixin,
    UpdateMixin,
    RetrieveMixin,
    FilterMixin,
)
from tables import Device


@dataclass
class DevicesRepo(BaseRepo, CreateMixin, UpdateMixin, RetrieveMixin, FilterMixin):
    table = Device
