"""Random player"""
import random
from typing import Sequence

from bots.BotInterface import BotInterface
from environment.Constants import Action, Stage
from environment.Observation import Observation
from utils.handValue import getHandPercent

# your bot class, rename to match the file name
class ANLI_Pre_Post(BotInterface):

    # change the name of your bot here
    def __init__(self, name="ANLI_Pre_Post"):
        '''init function'''
        super().__init__(name=name)

    def act(self, action_space: Sequence[Action], observation: Observation) -> Action:
        # use different strategy depending on pre or post flop (before or after community cards are delt)
        stage = observation.stage
        if stage == Stage.PREFLOP:
            return self.handlePreFlop(action_space, observation)

        return self.handlePostFlop(action_space, observation)

    def handlePreFlop(self, action_space: Sequence[Action], observation: Observation) -> Action:
        # get my hand's percent value (how good is this 2 card hand out of all possible 2 card hands)
        handPercent, _ = getHandPercent(observation.myHand)
        # if my hand is top 20 percent: raise
        if handPercent < .50:
            return Action.RAISE
        # if my hand is top 60 percent: call
        elif handPercent < .75:
            return Action.CALL
        # else check or fold
        return self.defaultAction(action_space)

    def handlePostFlop(self, action_space: Sequence[Action], observation: Observation) -> Action:
        # get my hand's percent value (how good is the best 5 card hand i can make out of all possible 5 card hands)
        handPercent, cards = getHandPercent(
            observation.myHand, observation.boardCards)
        # if my hand is top 30 percent: raise
        if handPercent <= .50:
            return Action.RAISE
        # if my hand is top 80 percent: call
        elif handPercent <= .75:
            return Action.CALL
        # else check or fold
        return self.defaultAction(action_space)
    
    def defaultAction(self, action_space: Sequence[Action]) -> Action:
        if Action.CHECK in action_space:
            return Action.CHECK
        elif Action.SMALL_BLIND in action_space:
            return Action.SMALL_BLIND
        elif Action.BIG_BLIND in action_space:
            return Action.BIG_BLIND
        return Action.FOLD
