from enum import IntFlag

class HitSoundType(IntFlag):
    none = 0
    Normal = 1 << 0
    Whistle = 1 << 1
    Finish = 1 << 2
    Clap = 1 << 3