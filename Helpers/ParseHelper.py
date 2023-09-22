import re
from Enums.FileSections import FileSections

class ParseHelper():
    def GetCurrentSection(self, line):
        parsedSection = FileSections.none
        match = re.search("\[.*\]", line)
        if match:
            parsedSection = FileSections[match.group()[1:-1]]
            
        return parsedSection
    def IsLineValid(self, line, currentSection):
        if currentSection == FileSections.Format:
            return line.lower().find('osu file format v') > 0
        elif currentSection.value >= FileSections.General.value and currentSection.value <= FileSections.Difficulty.value:
            return line.find(':') > 0
        elif currentSection == FileSections.Fonts or currentSection == FileSections.Mania:
            return line.find(':') > 0
        elif currentSection == FileSections.Events or currentSection == FileSections.TimingPoints or currentSection == FileSections.HitObjects:
            return line.find(',') > 0
        elif currentSection == FileSections.Colors or currentSection == FileSections.CatchTheBeat:
            return line.find(',') > 0 and line.find(':') > 0
        else:
            return False
    