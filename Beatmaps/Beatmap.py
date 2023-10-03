from Beatmaps.Sections import *
from Helpers.ParseHelper import ParseHelper

# Beatmap class implementation heavily inspired by https://github.com/mrflashstudio/OsuParsers

class Beatmap:
    LATEST_OSZ_VERSION = 14
    
    def __init__(self):
        self.Version = self.LATEST_OSZ_VERSION
        self.GeneralSection = GeneralSection.GeneralSection()
        self.EditorSection = EditorSection.EditorSection()
        self.MetadataSection = MetadataSection.MetadataSection()
        self.DifficultySection = DifficultySection.DifficultySection()
        self.EventsSection = EventsSection.EventsSection()
        self.ColorsSection = ColorsSection.ColorsSection()
        
        self.TimingPoints = []
        self.HitObjects = []
        
    def BeatLengthAt(self, offset):
        if len(self.TimingPoints) == 0:
            return 0

        timingPoint = 0
        samplePoint = 0
        
        for i in range(len(self.TimingPoints)):
            if self.TimingPoints[i].Offset <= offset:
                if self.TimingPoints[i].Inherited:
                    samplePoint = i
                else:
                    timingPoint = i
        
        multiplier = 1.0
        
        if samplePoint > timingPoint and self.TimingPoints[samplePoint].BeatLength < 0:
            multiplier = ParseHelper.CalculateBpmMultiplier(self.TimingPoints[samplePoint])
        
        return self.TimingPoints[timingPoint].BeatLength * multiplier
        