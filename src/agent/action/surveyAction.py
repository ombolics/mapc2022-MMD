from data.coreData.coordinate import Coordinate
from mapc2022 import Agent as MapcAgent, AgentActionError as MapcAgentActionError

from agent.action.agentAction import AgentAction

class SurveyAction(AgentAction):

    target: str | Coordinate | None
    
    def __init__(self, target: str | Coordinate | None) -> None:
        self.target = target

    def perform(self, agent: MapcAgent) -> str:
        

        try:
            agent.survey(self.target)
            return "success"
        except MapcAgentActionError as e:
            return e.args[0]