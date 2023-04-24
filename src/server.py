import mesa
import math
from core import model
from core.agents import TunnelAgent, TravellerAgent, OpponentAgent
from mesa.visualization.modules import TextElement, ChartModule

style = "margin-top: 0; margin-bottom: 0rem; font-size: 13px; font-weight: 500;"

class TextPreConditionDetail(TextElement):
    def __init__(self):
        pass


    def generate_table(self, p):

        r1 = [
            str(f"<p style=\"{style}\"> +ve, Active (j) = {round(p.positive.j,3)}</p>"),
            str(f"<p style=\"{style}\"> +ve, Not Active (k) = {round(p.positive.k,3)}</p>"),
            str(f"<p style=\"{style}\"> No +ve,     Active (l) = {round(p.positive.l,3)}</p>"),
            str(f"<p style=\"{style}\"> No -ve, Not Active (m) = {round(p.positive.m,3)}</p>"),
            str(f"<h5 style=\"{style};font-weight: 800\"> Corr(P,A) = {round(p.cpa,3)}</h5>"),
            str(f"<p style=\"{style}\">    -ve,     Active (j)= {round(p.negetive.j,3)}</p>"),
            str(f"<p style=\"{style}\">    -ve, Not Active (k)= {round(p.negetive.k,3)}</p>"),
            str(f"<p style=\"{style}\"> No -ve,     Active (l)= {round(p.negetive.l,3)}</p>"),
            str(f"<p style=\"{style}\"> No +ve, Not Active (m)= {round(p.negetive.m,3)}</p>"),
            str(f"<p style=\"{style};font-weight: 800\"> Corr(P,N) = {round(p.cna,3)}</p>"),
            str(f"<p style=\"{style};font-weight: 800; color: red\"> Relevance = {round(p.relevance,3)}</p>"),
            str(f"<p style=\"{style};font-weight: 800; color: green\"> Reliability = {round(p.reliability,3)}</p>"),
        ]
        s = ""
        for i in r1:
            s = s+i
        cs = "Jump and Go Behavior" if p.type ==1 else "Wait and See Behavior"
        return f"<h2>{cs}</h2> {s}"

    def render(self, model):
        s = ""

        for p in model.preconditions:
            s += self.generate_table(p)
        return s

class TextStrategy(TextElement):
    def __init__(self):
        pass

    def render(self, model):
        return f"<p style=\"{style};font-weight: 800; color: blue\"> Strategy selection = {round(model.select_strategy,3)}</p>"

chart_strategy = ChartModule([{"Label": "Strategy_Coefficient",
                                "Color": "Black"}],
                        data_collector_name='datacollector')

model_params = {
    "agents_count": mesa.visualization.Slider(
        "Agents Count",
        30,
        1,
        50,
        30
    ),
    "Kp": mesa.visualization.Slider(
        "Learning Coefficient",
        0.05,
        0,
        1,
        0.01
    ),
}

def agent_portrayal(agent):
    if type(agent) == TunnelAgent:
        return {"Shape": 'rect',
                 "Filled": "true",
                 "Layer": 0,
                 "Color": 'grey',
                 "w": 1,
                 "h": 1}
    elif type(agent) == OpponentAgent:
        return {"Shape": 'circle',
                 "Filled": "true",
                 "Layer": 0,
                 "Color": 'blue',
                 "r": 2}
    else:
        return  {"Shape": 'circle',
                 "Filled": "true",
                 "Layer": 0,
                 "Color": 'Red',
                 "r": 1}

grid = mesa.visualization.CanvasGrid(agent_portrayal, 100, 100, 500, 500)
server = mesa.visualization.ModularServer(
    model.Model,
    [grid, TextStrategy(), TextPreConditionDetail(), chart_strategy],
    "Tunner Runner",
    model_params,
)
server.port = 8521

if __name__ == '__main__':
    server.launch()