from Beatmaps.Objects.Extras import Extras
from Beatmaps.Objects.HitObject import HitObject

class Slider(HitObject):
    def __init__(self, position=[0,0], startTime=0, endTime=0, hitSoundValue=0,
                 curveType=None, sliderPoints=None, repeats=None, pixelLength=None, isNewCombo=False, comboOffset=0,
                 edgeHitSounds=None, edgeAdditions=None, extras=Extras()):
        super().__init__(position, startTime, endTime, hitSoundValue, extras, 
                         isNewCombo, comboOffset)
        self.CurveType = curveType
        self.SliderPoints = sliderPoints
        self.Repeats = repeats
        self.PixelLength = pixelLength
        self.EdgeHitSounds = edgeHitSounds
        self.EdgeAdditions = edgeAdditions
        
    def __str__(self):
        s = super().__str__()
        s += "Slider points:\n"
        for point in self.SliderPoints:
            s += f"<x: {point[0]}, y: {point[1]}>\n"
        s += f"Repeat #: {self.Repeats}\n"
        return s