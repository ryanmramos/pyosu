import re
from Enums.Beatmaps.CurveType import CurveType
from Enums.FileSections import FileSections

class ParseHelper():
    def GetCurrentSection(line):
        parsedSection = FileSections.none
        match = re.search("\[.*\]", line)
        if match:
            parsedSection = FileSections[match.group()[1:-1]]
            
        return parsedSection
    
    def IsLineValid(line, currentSection):
        if currentSection == FileSections.Format:
            return line.lower().find('osu file format v') > 0
        elif currentSection.value >= FileSections.General.value and currentSection.value <= FileSections.Difficulty.value:
            return line.find(':') > 0
        elif currentSection == FileSections.Fonts or currentSection == FileSections.Mania:
            return line.find(':') > 0
        elif currentSection == FileSections.Events or currentSection == FileSections.TimingPoints or currentSection == FileSections.HitObjects:
            return line.find(',') > 0
        elif currentSection == FileSections.Colours or currentSection == FileSections.CatchTheBeat:
            return line.find(',') > 0 and line.find(':') > 0
        else:
            return False
        
    def GetCurveType(c):
        # Switch on c
        if c == 'C':
            return CurveType.Catmull
        elif c == 'B':
            return CurveType.Bezier
        elif c == 'L':
            return CurveType.Linear
        elif c == 'P':
            return CurveType.PerfectCurve
        else:
            return CurveType.PerfectCurve
        
    def GetSliderPoints(segments):
        sliderPoints = []
        for seg in segments:
            positionTokens = seg.split(':')
            sliderPoints.append([int(positionTokens[0]), int(positionTokens[1])])
        return sliderPoints
    