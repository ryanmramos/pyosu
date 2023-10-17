import os, re, sys
import config
from tkinter import filedialog as fd
from Beatmaps import Beatmap
from Decoders.BeatmapDecoder import BeatmapDecoder
from Replays.Objects.ReplayFrame import ReplayFrame
from ossapi import Ossapi
from osrparse import Replay

client_id = config.CLIENT_ID
client_secret = config.CLIENT_SECRET
api = Ossapi(client_id, client_secret)

OSU_PATH = os.path.join(os.getenv("LOCALAPPDATA"), "osu!")

def main():
    # Have the user choose a replay file
    replay_filename = fd.askopenfilename(initialdir=os.path.join(OSU_PATH, "Replays"),
                                         filetypes=[("*", ".osr")])
    replay = Replay.from_path(replay_filename)
    
    # Use ossapi to get the hash of the beatmap corresponding to the replay
    bm = api.beatmap(checksum=replay.beatmap_hash)
    
    # Find the beatmap locally
    bm_decoder = BeatmapDecoder()
    beatmap = None
    dir_regex = re.compile(f'^{bm.beatmapset_id}')          # find directory that starts with beatmap ID
    file_regex = re.compile(f'.*\[{bm.version}\].*osu$')    # check for file that his beatmap version
    for root, dir, files in os.walk(os.path.join(OSU_PATH, "Songs")):
        for d in dir:
            if dir_regex.match(d):
                for root, dir, files in os.walk(os.path.join(OSU_PATH, "Songs", d)):
                    for file in files:
                        if file_regex.match(file):
                            beatmap = bm_decoder.decode(os.path.join(OSU_PATH, "Songs", d, file))
                            break
    
    # Check if beatmap was found locally
    if not beatmap:
        print(f'(-) ERROR: Corresponding file for "{replay_filename[replay_filename.rfind("/") + 1:-1]}" not found locally.', file=sys.stderr)
        exit(-1)

    replay_frames = [0] * len(replay.replay_data)
    last_time = 0
    for i, replay_data in enumerate(replay.replay_data):
        replay_frames[i] = ReplayFrame(replay_data.x, replay_data.y, replay_data.time_delta, last_time + replay_data.time_delta, replay_data.keys)
        last_time = replay_frames[i].Time
    
    print(beatmap.HitObjects[0])
    for i, replay_frame in enumerate(replay_frames):
        if replay_frame.Time > 600 and replay_frame.Time < 900:
            print(replay_frame)
    
    return

if __name__ == "__main__":
    main()