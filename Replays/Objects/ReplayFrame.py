from dataclasses import dataclass
from osrparse import Key

@dataclass
class ReplayFrame:
    X: float
    Y: float
    TimeDiff: int
    Time: int
    Keys: Key

    def __str__(self):
        return f'<x:{self.X}\t, y:{self.Y}>\t at time {self.Time}ms\t {self.Keys}'

""""
Keys: 
    A key that can be pressed during osu!standard gameplay - mouse 1 and 2, key
    1 and 2, and smoke.
    M1    = 1 << 0
    M2    = 1 << 1
    K1    = 1 << 2
    K2    = 1 << 3
    SMOKE = 1 << 4
"""