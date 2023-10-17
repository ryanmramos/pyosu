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