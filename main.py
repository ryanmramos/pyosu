import os, re
import config
from tkinter import filedialog as fd
from Beatmaps import Beatmap
from Decoders.BeatmapDecoder import BeatmapDecoder
from ossapi import Ossapi
from osrparse import Replay

client_id = config.CLIENT_ID
client_secret = config.CLIENT_SECRET
api = Ossapi(client_id, client_secret)

OSU_PATH = os.path.join(os.getenv("LOCALAPPDATA"), "osu!")

def main():
    # filename = fd.askopenfilename(initialdir=os.path.join(OSU_PATH, "Songs"),
    #                               filetypes=[("*", ".osu")])
    # bm_decoder = BeatmapDecoder()
    # beatmap = bm_decoder.decode(filename)
    
    replay_filename = fd.askopenfilename(initialdir=os.path.join(OSU_PATH, "Replays"),
                                         filetypes=[("*", ".osr")])
    replay = Replay.from_path(replay_filename)
    
    bm = api.beatmap(checksum=replay.beatmap_hash)
    
    bm_file = None
    dir_regex = re.compile(f'^{bm.beatmapset_id}')
    file_regex = re.compile(f'.*\[{bm.version}\].*osu$')
    for root, dir, files in os.walk(os.path.join(OSU_PATH, "Songs")):
        for d in dir:
            if dir_regex.match(d):
                for root, dir, files in os.walk(os.path.join(OSU_PATH, "Songs", d)):
                    for file in files:
                        if file_regex.match(file):
                            print(file)
    
    return

if __name__ == "__main__":
    main()