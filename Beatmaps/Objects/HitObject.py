from Beatmaps.Objects.Extras import Extras
from globals import *

class HitObject():
    def __init__(self, position=[0,0], startTime=0, endTime=0, hitSoundValue=0,
                 extras=Extras(), isNewCombo=False, comboOffset=0):
        self.Position = position
        self.StartTime = startTime
        self.EndTime = endTime
        self.HitSoundValue = hitSoundValue
        self.Extras = extras
        self.IsNewCombo = isNewCombo
        self.ComboOffset = comboOffset
        
    def __str__(self):
        s = f"<x: {self.Position[X]}, y: {self.Position[Y]}>\n"
        s += f"Start Time: {self.StartTime}\nEnd Time: {self.EndTime}\n"
        return s
        
    def DistanceFrom(self, otherObject):
        dist = (self.Position[X] - otherObject.Position[X]) ** 2
        dist += (self.Position[Y] - otherObject.Position[Y]) ** 2
        dist = pow(dist, 0.5)
        return dist