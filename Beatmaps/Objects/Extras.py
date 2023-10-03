from Enums.Beatmaps.SampleSet import SampleSet

class Extras():
    def __init__(self, sampleSet=None, additionSet=None, customIdx=None, vol=None, sampleFileName=None):
        self.SampleSet = sampleSet
        self.AdditionSet = additionSet
        self.CustomIdx = customIdx
        self.Vol = vol
        self.SampleFileName = sampleFileName
        
    def __str__(self):
        s = f"SampleSet: {self.SampleSet}\n"
        s += f"AdditionSet: {self.AdditionSet}\n"
        s += f"CustomIndex: {self.CustomIdx}\n"
        s += f"Volume: {self.Vol}\n"
        s += f"SampleFileName: {self.SampleFileName}\n"
        return s