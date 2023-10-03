class TimingPoint():
    def __init__(self, offset, beatLength, timeSignature, sampleSet, 
                 customSampleSet, volume, inherited, effects):
        self.Offset = offset
        
        # Uninherited timing points: duration of a beat in milliseconds
        # Inherited timing points: negative inverse slider velocity multiplier, as a percantage
        # ex: -50 would make all sliders in this timing section twice as fast as SliderMultiplier
        self.BeatLength = beatLength
        
        self.TimeSignature = timeSignature
        self.SampleSet = sampleSet
        self.CustomSampleSet = customSampleSet
        self.Volume = volume
        self.Inherited = inherited
        self.Effects = effects
        
    def __str__(self):
        s = f"Offset: {self.Offset}\nBeatLength: {self.BeatLength}\n"
        s += f"TimeSignature: {self.TimeSignature}\nSampleSetValue: {self.SampleSet}\n"
        s += f"CustomSampleSet: {self.CustomSampleSet}\nVolume: {self.Volume}\n"
        s += f"Inherited: {self.Inherited}\nEffects: {self.Effects}\n"
        return s
        