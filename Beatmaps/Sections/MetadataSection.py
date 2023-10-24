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
        
    def __str__(self):
        return f'Title: {self.Title}\nVersion: {self.Version}\nArtist: {self.Artist}\nCreator: {self.Creator}\nTags: {self.Tags}'