from data.coreData import MapValueEnum, Coordinate, MapValue, Task, TaskRequirement, MapcRole, Norm, NormRegulation, RegulationType
from data.coreData.enums import IncidentType
from data.coreData.hitIncident import HitIncident
from data.coreData.incident import Incident
from data.coreData.surveyIncident import SurveyIncident

class DynamicPerceptWrapper:
    """
    Wrapper for the simulation static percept.
    """

    score: int
    energy: int
    deactivated: bool
    role: str
    roleZones: list[Coordinate]
    goalZones: list[Coordinate]
    attached: list[Coordinate]
    lastAction: str
    lastActionResult: str
    things: dict[Coordinate, MapValue]
    markers: dict[Coordinate, MapValue]
    dispensers: dict[Coordinate, MapValue]
    tasks: list[Task]
    norms: list[Norm]
    events: list[Incident]


    def __init__(self, perception: dict, roles: dict[str, MapcRole], simulationStep: int) -> None:
        self.score = perception["score"]
        self.energy = perception["energy"]
        self.deactivated = perception["deactivated"]
        self.role = perception["role"]
        self.roleZones = [Coordinate(elem[0], elem[1], False) for elem in perception["roleZones"]]
        self.goalZones = [Coordinate(elem[0], elem[1], False) for elem in perception["goalZones"]]
        self.attached = [Coordinate(elem[0], elem[1], False) for elem in perception["attached"]]
        self.lastAction = perception["lastAction"]
        self.lastActionResult = perception["lastActionResult"]

        self.things = dict()
        self.markers = dict()
        self.dispensers = dict()
        
        ##TODO: events
        self.events = self.parseEvents(perception['events'])
        # print(f'perception[events]={perception["events"]}')

        self.tasks = [Task(task["name"], task["deadline"], task["reward"],
                [TaskRequirement(req["x"], req["y"], req["details"], req["type"]) for req in task["requirements"]])
            for task in perception["tasks"]]
        
        self.norms = [Norm(norm["name"], int(norm["start"]), int(norm["until"]), int(norm["punishment"]),
                [NormRegulation(RegulationType[r["type"].upper()], r["name"], int(r["quantity"])) for r in norm["requirements"]])
            for norm in perception["norms"]]
        
        for thing in perception["things"]:
            entity = DynamicPerceptWrapper.convertEntity(thing["type"])
            coordinate = Coordinate(thing["x"], thing["y"], False)

            if entity not in [MapValueEnum.MARKER, MapValueEnum.DISPENSER]:
                self.things[coordinate] = MapValue(entity, thing["details"], simulationStep)
            elif entity == MapValueEnum.DISPENSER:
                self.dispensers[coordinate] = MapValue(entity, thing["details"], simulationStep)
            elif thing["details"] != "cp":
                self.markers[coordinate] = MapValue(entity, thing["details"], simulationStep)
        
        self.fillWithEmptyThings(roles[self.role].vision, simulationStep)


    def parseEvents(self, data:list[dict]) -> list[Incident]:
        events = [Incident]
        for d in data:
            if d['type'] == IncidentType.HIT:
                events.append(HitIncident(IncidentType.HIT, d['origin']))
                
            else:
                incident = SurveyIncident(IncidentType.SURVEY, d['target'])
                
                if d['target'] == 'agent':
                    incident.name = d['name']
                    incident.role = d['role']
                    incident.energy = d['energy']
                else:
                    incident.distance = d['distance']
                events.append(incident)  
        return events

    def fillWithEmptyThings(self, vision: int, simulationStep: int) -> None:
        """
        Empty entities are not in the percept, these must be filled
        by the vision range and percept values.
        """

        for i in range((-1) * vision, vision + 1):
            for j in range((-1) * vision, vision + 1):
                coordinate = Coordinate(i, j, False)
                if coordinate not in self.things and Coordinate.manhattanDistance(Coordinate.origo(), coordinate) <= vision:
                    self.things[coordinate] = MapValue(MapValueEnum.EMPTY, "", simulationStep)

    @staticmethod
    def convertEntity(entity: str) -> MapValueEnum:
        """
        Converts percept entity strings to enums
        """

        match entity:
            case "entity":
                return MapValueEnum.AGENT
            case "obstacle":
                return MapValueEnum.OBSTACLE
            case "block":
                return MapValueEnum.BLOCK
            case "dispenser":
                return MapValueEnum.DISPENSER
            case "marker":
                return MapValueEnum.MARKER