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
    return api.beatmap(checksum=replay.beatmap_hash)

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