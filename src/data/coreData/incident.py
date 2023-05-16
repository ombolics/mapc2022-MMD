from abc import ABC

from data.coreData.enums import IncidentType


class Incident(ABC):

    type: IncidentType

    def __init__(self, type) -> None:
        self.type = type

    def __str__(self) -> str:
        return ', '.join("%s: %s" % item for item in vars(self).items()) + '\n'

    