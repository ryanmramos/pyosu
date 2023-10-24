import os, re, sys
from pyosu import config
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

def get_replay_from_file(file):
    return Replay.from_file(file)

def get_replay_beatmap(replay):
    return find_local_beatmap(api.beatmap(checksum=replay.beatmap_hash))

"""
    TODO:
        I don't really like the idea of accessing/having to depend on local storage
        when retrieving beatmap data. Current api gives beatmap object with no HitObject list though,
        so this will be here for now.
"""
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

def get_taps_on_hit_objects(beatmap, replay):
    # Create replay frames to work with (frames that include explicit Time value, not just time_delta)
    replay_frames = create_replay_frames(replay.replay_data)
    
    # Get tap windows from replay frames
    tap_windows = get_taps(replay_frames)
    
    # Make a list of frames where each frame is the of a tap_window
    tap_starts = [tap_window[0] for tap_window in tap_windows]
    
    # Get list of lists where first element in each inner list is hit object and second element is frame where that
    # object was tapped/attempted (if on exists)
    hit_object_taps = get_hit_object_taps(beatmap.HitObjects, tap_starts, beatmap.DifficultySection)
    
    return hit_object_taps
    
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