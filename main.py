import os, re, sys
import config
from tkinter import filedialog as fd
from Decoders.BeatmapDecoder import BeatmapDecoder
from Replays.Objects.ReplayFrame import ReplayFrame
from Helpers.TapHelper import get_taps, get_hit_object_taps
from globals import *

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

    # Get tap windows from replay frames
    tap_windows = get_taps(replay_frames)

    # Make a list of frames where each frame is the start of a tap_window
    tap_starts = [tap_window[0] for tap_window in tap_windows]

    # Get list of lists where first element is hit object and second element is frame where that object was tapped/attempted (if one exists)
    hit_object_taps = get_hit_object_taps(beatmap.HitObjects, tap_starts, beatmap.DifficultySection)
    
    for i, pair in enumerate(hit_object_taps):
        if i > 300:
            break
        print('HitObject:')
        print(pair[0])
        print('Tap Frame:')
        if not pair[1]:
            print('MISSED (NO TAP)\n')
            continue
        if pair[1].Keys < 0:
            print('MISSED (TAP)')
        print(pair[1])
        print(f'\nTiming: {pair[1].Time - pair[0].StartTime}\n')
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