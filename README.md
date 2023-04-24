# Tunnel Runner

Implement to observe how agents move inside a tunnel with full of opponents with minimum casualities. There are two major 
strategies were used. First one is jump and go. when a agent see an opponent infront of him, then agent jumps to the opposit side of the agent and carry forward. second is wait and see,  when a agent see an opponent infront of him, agent waits until the opponent passed out. Then move forward. After few iterations, agents learn and select which behavior should use to cross the tunnel from these two strategies.

![image](https://github.com/kolithawarnakulasooriya/Learning-Coordinate-Behavior-Tunnel-Runner/blob/main/p1.png)

## Required Libraries

[Mesa](https://mesa.readthedocs.io/en/latest/index.html) - Multi agent simulator

## How to Run

```
pip install -r requirements.txt
python run.py
```

## Class Diagram
![cls](https://github.com/kolithawarnakulasooriya/Learning-Coordinate-Behavior-Tunnel-Runner/blob/main/classes_src.png)