import os
from tkinter import filedialog as fd
from Beatmaps import Beatmap
from Decoders.BeatmapDecoder import BeatmapDecoder

OSU_PATH = os.path.join(os.getenv("LOCALAPPDATA"), "osu!")

def main():
    filename = fd.askopenfilename(initialdir=os.path.join(OSU_PATH, "Songs"),
                                  filetypes=[("*", ".osu")])
    bm_decoder = BeatmapDecoder()
    beatmap = bm_decoder.decode(filename)
    return

if __name__ == "__main__":
    main()