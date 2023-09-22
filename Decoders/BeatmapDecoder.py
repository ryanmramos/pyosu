import os, sys
from Beatmaps import Beatmap
from Enums.FileSections import FileSections
from Helpers.ParseHelper import ParseHelper

class BeatmapDecoder():
    def __init__(self):
        self.beatmap = None
        self.currentSection = FileSections.none
        
    def decode(self, path):
        
        # check that path is valid
        if (not os.path.isfile(path)):
            print(f"(-) Error: path '{path}' is not valid", file=sys.stderr)
            return None
        
        f = None
        # attempt to open file to read from it
        try:
            f = open(path, "r")
        except IOError:
            print(f"(-) Error: Could not open file '{path}' as the input file.", file=sys.stderr)
        
        self.beatmap = Beatmap.Beatmap()
        self.currentSection = FileSections.Format
        
        for line in f:
            if (line and not line.isspace()) and (not line.startswith("//")):
                if ParseHelper.GetCurrentSection(None, line) != FileSections.none:
                    self.currentSection = ParseHelper.GetCurrentSection(None, line)
                elif ParseHelper.IsLineValid(None, line, self.currentSection):
                    self.ParseLine(line)
                    
    def ParseLine(self, line):
        # pass on a case means that it's not a priority for me as of right now
        # and will be implemented later :)
        if self.currentSection == FileSections.Format:
            pass
        elif self.currentSection == FileSections.General:
            pass
        elif self.currentSection == FileSections.Editor:
            pass
        elif self.curretnSection == FileSections.Metadata:
            pass
        elif self.currentSection == FileSections.Difficulty:
            pass
        elif self.currentSection == FileSections.Events:
            pass
        elif self.currentSection == FileSections.TimingPoints:
            pass
        elif self.currentSection == FileSections.Colors:
            pass
        elif self.currentSection == FileSections.HitObjects:
            self.ParseHitObject(line)
            
    def ParseHitObject(self, line):
        pass
        