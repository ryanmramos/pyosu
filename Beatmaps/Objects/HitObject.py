from Beatmaps.Objects.Extras import Extras

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
        s = f"<x: {self.Position[0]}, y: {self.Position[1]}>\n"
        s += f"Start Time: {self.StartTime}\nEnd Time: {self.EndTime}\n"
        return s
        
    def DistanceFrom(self, otherObject):
        dist = (self.Position[0] - otherObject.Position[0]) ** 2
        dist += (self.Position[1] - otherObject.Position[1]) ** 2
        dist = pow(dist, 0.5)
        return dist