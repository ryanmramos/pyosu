from pyosu.Enums.Beatmaps.SampleSet import SampleSet
from pyosu.Enums.Ruleset import Ruleset

class GeneralSection():
    def __init__(self):
        self.AudioFilename = ""
        self.AudioLeadIn = 0
        self.PreviewTime = -1
        self.Countdown = 1
        self.SampleSet = SampleSet.Normal
        self.StackLeniency = 0.7
        self.Mode = Ruleset.Standard
        self.LetterboxInBreaks = False
        self.UseSkinSprites = False
        self.EpilepsyWarning = False
        self.CountdownOffset = 0
        self.SpecialStyle = False
        self.WidescreenStoryBoard = False
        self.SamplesMatchPlaybackRate = False