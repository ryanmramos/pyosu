from pyosu.Beatmaps.Sections import GeneralSection, EditorSection, MetadataSection, DifficultySection, EventsSection

# Beatmap class implementation heavily inspired from https://github.com/mrflashstudio/OsuParsers
class Beatmap:
    LATEST_OSZ_VERSION = 14
    
    def __init__(self):
        self.Version = self.LATEST_OSZ_VERSION
        self.GeneralSection = GeneralSection.GeneralSection()
        self.EditorSection = EditorSection.EditorSection()
        self.MetadataSection = MetadataSection.MetadataSection()
        self.DifficultySection = DifficultySection.DifficultySection()
        self.EventsSection = EventsSection.EventsSection()
        