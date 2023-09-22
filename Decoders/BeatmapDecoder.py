import os, sys
from Beatmaps import Beatmap
from Enums.FileSections import FileSections

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
            print(line, end="")
        