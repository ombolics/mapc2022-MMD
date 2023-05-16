from agent.action.surveyAction import SurveyAction
from data.coreData import Coordinate

from data.intention import Observation
from agent.intention.agentIntention import AgentIntention

from agent.action import AgentAction

class SurveyIntention(AgentIntention):    
    """
    Intention to detach every connected entity. Its goal is to
    detach every attached entity.
    """

    async def planNextAction(self, observation : Observation) -> AgentAction:
        return SurveyAction()

    def checkFinished(self, observation: Observation) -> bool:
        return not any(observation.agentData.attachedEntities)
    
    def updateCoordinatesByOffset(self, _: Coordinate) -> None:
        pass

    def normalizeCoordinates(self) -> None:
        pass

    def explain(self) -> str:
        return "dropping blocks"