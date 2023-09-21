class MetadataSection():
    def __init__(self):
        self.Title = ""
        self.TitleUnicode = ""
        self.Artist = ""
        self.ArtistUnicode = ""
        self.Creator = ""
        self.Version = ""
        self.Source = ""
        self.Tags = []              # list of strings
        self.BeatmapID = None
        self.BeatmapSetID = None