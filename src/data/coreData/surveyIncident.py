
from data.coreData.enums import SurveyTarget
from data.coreData.incident import Incident


class SurveyIncident(Incident):

    target: SurveyTarget
    distance: int | None
    name: str | None
    role: str | None
    energy: str | None

    def __init__(self, type = None, target = None, distance = None, name = None, role = None, energy = None) -> None:
        super().__init__(type)
        
        self.target = target
        self.distance = distance
        self.name = name
        self. role = role
        self.energy = energy

    def __str__(self) -> str:
        return ', '.join("%s: %s" % item for item in vars(self).items()) + '\n'
       
