import mesa
import math
import random
from .commons import *

"""
    This is used for creating the tunnel walls
"""
class TunnelAgent(mesa.Agent):
    def __init__(self, unique_id, model, x, y):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y

    def step(self):
        pass

"""
    This agent is used for creating the opponents running in the tunnel
"""
class OpponentAgent(mesa.Agent):

    def __init__(self, unique_id, model, x=0, y=0, direction=0):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.direction = direction

    def step(self):
        if self.direction == OPPONENT_DIRECTION_DOWN:
            if self.y < WALL_TOP + 2:
                self.direction = OPPONENT_DIRECTION_UP
            else:
                self.y = self.y - 1
        else:
            if self.y > WALL_BOTTOM -3:
                self.direction = OPPONENT_DIRECTION_DOWN
            else:
                self.y = self.y + 1

        self.model.grid.move_agent(self, (self.x, self.y))

"""
This is the traveller agent going through the wall
"""
class TravellerAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.max_width = model.size[0]
        self.max_height = model.size[1]
        self.x = STARTING_X_POS - 2
        self.y = STARTING_Y_POS(self.max_height)
        self.precondition = PRE_COND_STAY_AND_GO
        self.energy = MAX_ENERGY

    """
        The statistics are initialized at some value N (for example N = 10) and 
        “decayed” by multiplying them with every time they are updated
    """
    def calculate_energy_decay(self):
        self.energy = self.energy / (self.energy + 1)
        return self.energy

    def step(self):
        if self.x <ENDING_X_POS + 2:
            next_x = self.x

            # within the tunnel
            if next_x >= STARTING_X_POS and next_x <= ENDING_X_POS:

                # get all the neighbours
                nb = self.model.grid.get_neighbors((next_x, self.y), moore= True)

                #find all the opponents who stays ahead not sides and behind
                nb = [x for x in nb if type(x) == OpponentAgent and x.x > next_x]

                # if there is an opponent, we should activate our saving strategies
                if len(nb)>0:
                    # here we assume that we only have one opponent ahead
                    opponent = nb[0]
                    # select the strategy 
                    strategy = STATEGY(self.model.select_strategy)

                    # if the strategy is jump and go
                    if strategy == PRE_COND_JUMP_AND_GO:
                        self.precondition = PRE_COND_JUMP_AND_GO
                        if(opponent.y > self.y):                   # if the opponent is on right side, safer is left side, chose left side
                            self.y -= 1
                            next_x += 1
                        elif(opponent.y < self.y):                 # if the opponent is on left side, safer is right side, chose right side
                            self.y += 1
                            next_x += 1
                        else:                               # if the opponent is on center, should not choose a side, so dont move
                            next_x = next_x 
                    # wait and see strategy until the opponent is passed
                    else:
                        self.precondition = 0
                        next_x = next_x 
                else:
                    next_x += 1
            else:
                next_x += 1

            # Here we update the correlation table
            # if we hit an opponent, 
            #       Consider as negetive feedback
            # if we move forwward,
            #       Consoder as a positive feedback
            # if not moved or not hit by an  opponent,
            #       Consider as no feedback comes
            d = [x for x in self.model.schedule.agents if type(x) == OpponentAgent and x.x == next_x and x.y == self.y]
            
            if(len(d) > 0):
                if self.x == next_x:
                # not feedback - not eaten but not negetive feedback
                    self.model.update_no_negetive_feedback(self.precondition, self.calculate_energy_decay())
                else:
                # negetive feedback 1 - eaten by opponent
                    self.model.update_negetive_feedback(self.precondition, self.calculate_energy_decay())
            else:
                if self.x == next_x:
                # not feedback - not eaten but not positive feedback
                    self.model.update_no_positive_feedback(self.precondition, self.calculate_energy_decay())
                else:
                # positive feedback - go without an issue
                    self.model.update_positive_feedback(self.precondition, self.calculate_energy_decay())

            self.x = next_x
            self.model.update_all()
            self.model.grid.move_agent(self, (self.x, self.y))
        else:
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)
            
            # if all the group of agents successfully moved to the end, the strategy coefficient chnages and new group comes in
            traveller_agents = [x for x in self.model.schedule.agents if type(x) == TravellerAgent]
            
            if len(traveller_agents) == 0:
                self.model.agents_count = self.model.max_agent_count
                self.model.update_strategy_coefficient()