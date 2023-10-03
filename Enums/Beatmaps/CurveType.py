from enum import Enum

class CurveType(Enum):
    Catmull = 0
    Bezier = 1
    Linear = 2
    PerfectCurve = 3