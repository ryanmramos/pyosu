import os, re, sys
import config
from tkinter import filedialog as fd
from Beatmaps import Beatmap
from Decoders.BeatmapDecoder import BeatmapDecoder
from Replays.Objects.ReplayFrame import ReplayFrame
from Helpers.GetNextTap import get_next_tap

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
    beatmap = find_local_beatmap(bm)
    
    # Check if beatmap was found locally
    if not beatmap:
        print(f'(-) ERROR: Corresponding file for "{replay_filename[replay_filename.rfind("/") + 1:-1]}" not found locally.', file=sys.stderr)
        exit(-1)

    # Create replay frames to work with (includes explicit frame Time, not just time_delta)
    replay_frames = create_replay_frames(replay.replay_data)
    
    # print(beatmap.HitObjects[0])
    # for i, replay_frame in enumerate(replay_frames):
    #     # if replay_frame.Time > 600 and replay_frame.Time < 9000:
    #     print(replay_frame.Keys)

    get_next_tap(None, None)
    
    return

def find_local_beatmap(bm_api_response):
    dir_regex = re.compile(f'^{bm_api_response.beatmapset_id}')          # find directory that starts with beatmap ID
    file_regex = re.compile(f'.*\[{bm_api_response.version}\].*osu$')    # check for file that his beatmap version
    for root, dir, files in os.walk(os.path.join(OSU_PATH, "Songs")):
        for d in dir:
            if dir_regex.match(d):
                for root, dir, files in os.walk(os.path.join(OSU_PATH, "Songs", d)):
                    for file in files:
                        if file_regex.match(file):
                            # Local beatmap found, return beatmap object created using beatmap decoder
                            return BeatmapDecoder().decode(os.path.join(OSU_PATH, "Songs", d, file))
    
    # If function reaches here, local beatmap was not found
    return None

def create_replay_frames(replay_data_list):
    rf = [0] * len(replay_data_list)
    last_time = 0
    for i, replay_data in enumerate(replay_data_list):
        rf[i] = ReplayFrame(replay_data.x, replay_data.y,
                            replay_data.time_delta,
                            last_time + replay_data.time_delta,
                            replay_data.keys)
        
        last_time = rf[i].Time
    
    return rf

if __name__ == "__main__":
    main()