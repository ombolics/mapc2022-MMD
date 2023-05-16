from data.coreData.coordinate import Coordinate
from data.coreData.incident import Incident

class HitIncident(Incident):

    origin: Coordinate | None

    def __init__(self, type, origin) -> None:
        super().__init__(type)

        self.origin = origin