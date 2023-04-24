# Tunnel Runner

Implement to observe how agents move inside a tunnel full of opponents with minimum casualties. There are two strategies used. The first strategy  called <b>jump and go</b>. When an agent sees an opponent in front of him, then the agent jumps to the opposite side of the opponent agent and moves forward. The second strategy is called <b>wait and see</b>. When an agent sees an opponent in front of him, the agent waits until the opponent passes out. Then move forward. After a few iterations, agents learn and select which behavior needs to be used to cross the tunnel from these two strategies.

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