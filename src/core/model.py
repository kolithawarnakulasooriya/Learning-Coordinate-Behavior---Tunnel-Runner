import mesa
from .commons import *
from .agents import TravellerAgent, OpponentAgent, TunnelAgent
from mesa.datacollection import DataCollector
import random as rnd

"""
This class represents the precondition table
"""
class Condition:
    def __init__(self):
        self.j =0
        self.k =0
        self.l =0
        self.m =0

"""
This class represent the precondition
"""
class PreCondition: 
    def __init__(self, type_index):
        # positive condition table
        self.positive = Condition()

        # negetive condition table
        self.negetive = Condition()
        
        #identification as behavior type (stay and go or jump and go)
        self.type = type_index
        
        self.cpa =0
        self.cna =0
        self.relevance =0
        self.reliability =0
        self.current_reliability = 0

    def active_and_positive(self, v):
        self.positive.j += v
    def not_active_and_positive(self, v):
        self.positive.k += v
    def active_and_negetive(self, v):
        self.negetive.j += v
    def not_active_and_negetive(self, v):
        self.negetive.k += v

    def active_and_no_postive(self, v):
        self.positive.l += v
    
    def not_active_and_no_negetive(self, v):
        self.negetive.m += v

    def active_and_no_negetive(self, v):
        self.negetive.l += v
    
    def not_active_and_no_positive(self, v):
        self.positive.m += v

class Model(mesa.Model):

    def __init__(self, agents_count=1, alpha = 0.01, Kp = 0.1, Ki = 0.01, width = 100, height=100):

        self.size = (width, height)
        self.grid = mesa.space.MultiGrid(width, height, torus=True)
        
        self.schedule = mesa.time.RandomActivation(self)
        self.agent_id = 0
        self.select_strategy = INITIAL_STRATEGY_BOUNDARY
        self.max_agent_count = agents_count
        self.agents_count = agents_count
        self.Kp = Kp
        self.Ki = Ki
        self.alpha = alpha
        self.datacollector = DataCollector(model_reporters={"Strategy_Coefficient": lambda m: m.select_strategy})

        # initiating pre conditions list
        self.preconditions: list = []
        self.preconditions.append(PreCondition(PRE_COND_STAY_AND_GO))
        self.preconditions.append(PreCondition(PRE_COND_JUMP_AND_GO))

        # create the tunnel 
        self.create_tunnel()
        # create opponents inside the tunnel
        self.create_opponents()

    """
        Update the agent id
    """
    def __update_agnet_id(self):
        self.agent_id +=1


    """
        This function creates the tunnel using tunnel bricks
    """
    def create_tunnel(self):

        x = STARTING_X_POS
        y_up = WALL_TOP
        y_down = WALL_BOTTOM
        length_of_the_tunnel = ENDING_X_POS - STARTING_X_POS

        # create the tunnel 
        for i in range(length_of_the_tunnel):
            
            # top brick
            tunnel_agent_top = TunnelAgent(self.agent_id, self, x, y_up)
            self.schedule.add(tunnel_agent_top)
            self.grid.place_agent(tunnel_agent_top, (tunnel_agent_top.x, tunnel_agent_top.y))
            self.__update_agnet_id()

            # bottom brik
            tunnel_agent_bottom = TunnelAgent(self.agent_id, self, x, y_down)
            self.schedule.add(tunnel_agent_bottom)
            self.grid.place_agent(tunnel_agent_bottom, (tunnel_agent_bottom.x, tunnel_agent_bottom.y))
            self.__update_agnet_id()

            # next brick place
            x += 1

    """
        This function creates opponents inside the tunnel
    """
    def create_opponents(self):

        length_of_the_tunnel = ENDING_X_POS - STARTING_X_POS

        for i in range(length_of_the_tunnel):
            y = self.random.randrange(WALL_BOTTOM - WALL_TOP - 5) + WALL_TOP + 3
            x = int(i) + STARTING_X_POS
            direction = rnd.randint(0, 1)
            
            opponent_agent = OpponentAgent(self.agent_id, self, x, y,  direction)
            self.schedule.add(opponent_agent)
            self.grid.place_agent(opponent_agent, (x, y))
            self.__update_agnet_id()

    """
        This function creates new traveller agent
    """
    def create_new_traveller_agent(self):
        agent = TravellerAgent(self.agent_id, self)
        self.schedule.add(agent)
        self.grid.place_agent(agent, (agent.x, agent.y))
        self.__update_agnet_id()

    """
        Override the step function from mesa
    """
    def step(self):
        self.schedule.step()
        # this cound how many agents are currently in the group, if all the group loss agents, start new group
        if self.agents_count >0:
            self.create_new_traveller_agent()
            self.agents_count -= 1
            self.datacollector.collect(self)


    def update_strategy_coefficient(self):
        
        pre_stay_and_go = self.preconditions[0] # stage and go
        pre_jump_and_go = self.preconditions[1] # jump and go

        k_stay_and_go =  self.Kp * (2 - pre_stay_and_go.relevance) + self.Ki * pre_stay_and_go.reliability
        k_jump_and_go =  self.Kp * (2 - pre_jump_and_go.relevance) + self.Ki * pre_jump_and_go.reliability
    
        #is jump and go is more reliable, increase the selection rate of jump and go
        if(k_stay_and_go < k_jump_and_go):
            self.select_strategy -= self.select_strategy * self.alpha
        elif(k_stay_and_go > k_jump_and_go):
            self.select_strategy += self.select_strategy * self.alpha
        else:
            self.select_strategy = self.select_strategy

        pre_stay_and_go.reliability = 0
        pre_jump_and_go.reliability = 0

        # is jump and go is more reliable, increase the selection rate of jump and go
        # if(pre_stay_and_go.reliability < pre_jump_and_go.reliability):
        #     self.select_strategy -= self.select_strategy * self.kp
        # elif(pre_stay_and_go.reliability > pre_jump_and_go.reliability):
        #     self.select_strategy += self.select_strategy * self.kp
        # else:
        #     self.select_strategy = self.select_strategy

        # end with maximum value of the selected strategy
        if(self.select_strategy > 1):
            self.select_strategy = 1.0

    #region feedback update functions
    def update_negetive_feedback(self, i, v):
        for x in self.preconditions:
            if x.type == i:
                x.active_and_negetive(v)
            else:
                x.not_active_and_negetive(v)

    def update_positive_feedback(self, i, v):
        for x in self.preconditions:
            if x.type == i: 
                x.active_and_positive(v)
            else:
                x.not_active_and_positive(v)

    def update_no_positive_feedback(self, i, v):
        for x in self.preconditions:
            if x.type == i:
                x.active_and_no_postive(v)
            else:
                x.not_active_and_no_negetive(v)

    def update_no_positive_feedback(self, i, v):
        for x in self.preconditions:
            if x.type == i:
                x.active_and_no_postive(v)
            else:
                x.not_active_and_no_negetive(v)

    def update_no_negetive_feedback(self, i, v):
        for x in self.preconditions:
            if x.type == i:
                x.active_and_no_negetive(v)
            else:
                x.not_active_and_no_positive(v)
    #endregion

    def update_all(self):
        for p in self.preconditions:
            # calculate coor(P,A)
            p.cpa = calculate_PPA(p.positive.j, p.positive.k, p.positive.l, p.positive.m)
            # calculate coor(N,A)
            p.cna = calculate_PPA(p.negetive.j, p.negetive.k, p.negetive.l, p.negetive.m)
            # coor(P,A) - coor(N,A)
            p.relevance = p.cpa - p.cna
            # calculate reliability of the action and behavior
            p.reliability += calculate_reliability(p)
            p.current_reliability = calculate_reliability(p)


        