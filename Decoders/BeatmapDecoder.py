import os, sys
from Beatmaps.Beatmap import Beatmap
from Beatmaps.Objects.HitCircle import HitCircle
from Enums.FileSections import FileSections
from Enums.Beatmaps.HitObjectType import HitObjectType
from Enums.Beatmaps.HitSoundType import HitSoundType
from Enums.Beatmaps.SampleSet import SampleSet
from Enums.Ruleset import Ruleset
from Helpers.ParseHelper import ParseHelper
from Beatmaps.Objects import Extras

class BeatmapDecoder():
    def __init__(self):
        self.Beatmap = None
        self.CurrentSection = FileSections.none
        
    def decode(self, path):
        
        # check that path is valid
        if (not os.path.isfile(path)):
            print(f"(-) Error: path '{path}' is not valid", file=sys.stderr)
            return None
        
        f = None
        # attempt to open file to read from it
        try:
            f = open(path, "r", encoding='utf-8')
        except IOError:
            print(f"(-) Error: Could not open file '{path}' as the input file.", file=sys.stderr)
        
        self.Beatmap = Beatmap()
        self.CurrentSection = FileSections.Format
        
        for line in f:
            if (line and not line.isspace()) and (not line.startswith("//")):
                if ParseHelper.GetCurrentSection(line) != FileSections.none:
                    self.CurrentSection = ParseHelper.GetCurrentSection(line)
                elif ParseHelper.IsLineValid(line, self.CurrentSection):
                    self.ParseLine(line)
                    
    def ParseLine(self, line):
        # pass on a case means that it's not a priority for me as of right now
        # and will be implemented later :)
        if self.CurrentSection == FileSections.Format:
            pass
        elif self.CurrentSection == FileSections.General:
            pass
        elif self.CurrentSection == FileSections.Editor:
            pass
        elif self.CurrentSection == FileSections.Metadata:
            pass
        elif self.CurrentSection == FileSections.Difficulty:
            pass
        elif self.CurrentSection == FileSections.Events:
            pass
        elif self.CurrentSection == FileSections.TimingPoints:
            pass
        elif self.CurrentSection == FileSections.Colours:
            pass
        elif self.CurrentSection == FileSections.HitObjects:
            self.ParseHitObject(line)
            
    def ParseHitObject(self, line):
        # Hit object syntax: x,y,time,type,hitSound,objectParams,hitSample
        tokens = line.split(',')
        
        position = [int(tokens[0]), int(tokens[1])]
        
        startTime = int(tokens[2])  # in ms
        
        type = int(tokens[3])
        
        comboOffset = (type & HitObjectType.ComboOffset.value) >> 4
        type &= ~HitObjectType.ComboOffset.value
        
        isNewCombo = True if (type & HitObjectType.NewCombo.value) > 0 else False
        type &= ~HitObjectType.NewCombo.value
        
        hitSound = int(tokens[4])
        
        hitObject = None
        
        # Build Extras for making Hit Object
        # Extras syntax --> normalSet:additionSet:index:volume:filename
        extrasSplit = tokens[-1].split(':')
        extraOffset = type & HitObjectType.Hold.value
        extras = Extras.Extras(
            SampleSet(int(extrasSplit[extraOffset])),
            SampleSet(int(extrasSplit[1 + extraOffset])),
            int(extrasSplit[2 + extraOffset]) if len(extrasSplit) > 2 else 0,
            int(extrasSplit[3 + extraOffset]) if len(extrasSplit) > 3 else 0,
            extrasSplit[4 + extraOffset] if len(extrasSplit) > 4 else ""
        ) if ':' in tokens[-1] else Extras.Extras()
        
        # Switch on type
        if type & HitObjectType.Circle.value:
            if self.Beatmap.GeneralSection.Mode == Ruleset.Standard:
                hitObject = HitCircle(position, startTime, startTime, hitSound, extras, isNewCombo, comboOffset)
                pass
            elif self.Beatmap.GeneralSection.Mode == Ruleset.Taiko:
                print("Taiko not implemented.", file=sys.stderr)
            elif self.Beatmap.GeneralSection.Mode == Ruleset.Catch:
                print("Catch not implemented.", file=sys.stderr)
            elif self.Beatmap.GeneralSection.Mode == Ruleset.Mania:
                print("Mania not implemented.", file=sys.stderr)
        elif type & HitObjectType.Slider.value:
            # Slider syntax: x,y,time,type,hitSound,curveType|curvePoints,slides,length,edgeSounds,edgeSets,hitSample
            curveType = ParseHelper.GetCurveType(tokens[5].split('|')[0][0])
            
            sliderPoints = ParseHelper.GetSliderPoints(tokens[5].split('|')[1:])
            
            repeats = int(tokens[6])
            
            pixelLength = float(tokens[7])
            
            # continue here with endTime
        