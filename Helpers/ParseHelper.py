import re
from Enums.FileSections import FileSections

class ParseHelper():
    def GetCurrentSection(self, line):
        parsedSection = FileSections.none
        match = re.search("\[.*\]", line)
        if match:
            # print(match.group()[1:-1])
            print(FileSections[match.group()[1:-1]])
        