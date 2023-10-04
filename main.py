import os
import config
from tkinter import filedialog as fd
from Beatmaps import Beatmap
from Decoders.BeatmapDecoder import BeatmapDecoder
from ossapi import Ossapi

client_id = config.CLIENT_ID
client_secret = config.CLIENT_SECRET
api = Ossapi(client_id, client_secret)

OSU_PATH = os.path.join(os.getenv("LOCALAPPDATA"), "osu!")

def main():
    # filename = fd.askopenfilename(initialdir=os.path.join(OSU_PATH, "Songs"),
    #                               filetypes=[("*", ".osu")])
    # bm_decoder = BeatmapDecoder()
    # beatmap = bm_decoder.decode(filename)
    
    top50 = api.ranking("osu", "performance")
    print(top50.ranking[0].user.username)
    return

if __name__ == "__main__":
    main()