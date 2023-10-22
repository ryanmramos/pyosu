from Enums.Replays.StandardKeys import StandardKeys as Key
from Beatmaps.Objects.Spinner import Spinner
from globals import *

# File globals
START_IDX = 0
LAST_IDX = 1
NEXT_START_IDX = 2

def get_next_tap(keys, idx=0):
    # Structure of tap_frames: [{start_idx}, {end_idx}, {next_start_idx}]
    tap_frames = []

    # Get to next tap if index is not already there
    while idx < len(keys) and keys[idx] & (Key.K1 + Key.K2) == 0:
        idx += 1
    
    # No more taps
    if idx >= len(keys):
        return None

    # Make list of possible transitions to the next tap while still remaining in current hold
    possible_transitions = []

    if keys[idx] & (Key.K1 + Key.K2) == Key.K1 + Key.K2:
        # No transitions (both keys are pressed)
        pass
    else:
        # Transition from one button pressed to both
        possible_transitions.append(Key.K1 + Key.K2)
        # Transtion from one button pressed immediately to the other
        possible_transitions.append(Key.K1 + Key.K2 - (keys[idx] & (Key.K1 + Key.K2)))
    tap_frames.append(idx)      # Start index
    idx += 1

    # Get hold frames
    next_start_idx = None
    while idx < len(keys) and keys[idx] & (Key.K1 + Key.K2) > 0:
        # TODO: I think this condition can be checked more elegantly
        if not next_start_idx and (keys[idx] in possible_transitions or (idx > 0 and keys[idx] > keys[idx - 1])):
            # No more transitions, one has been found
            possible_transitions = []
            next_start_idx = idx
        idx += 1
    
    if not next_start_idx:
        next_start_idx = idx
    tap_frames.append(idx - 1)          # Last index for this tap window
    tap_frames.append(next_start_idx)   # Start index for next call
    return tap_frames

def get_taps(replay_frames):
    # Form a list of Keys from the keys value in replay_frames
    key_list = [replay_frame.Keys for replay_frame in replay_frames]

    tap_windows = []

    start_idx = 0
    while start_idx < len(key_list):
        tap = get_next_tap(key_list, start_idx)
        if not tap:
            break
        tap_window = []
        for i in range(tap[START_IDX], tap[LAST_IDX] + 1):
            tap_window.append(replay_frames[i])
        tap_windows.append(tap_window)
        start_idx = tap[NEXT_START_IDX]
    
    return tap_windows

def get_hit_object_taps(hit_objects, tap_starts, diff_section):

    hit_object_taps = []

    hit_obj_idx = 0
    tap_start_idx = 0
    while tap_start_idx < len(tap_starts):
        # Get next HitCircle or Slider
        while hit_obj_idx < len(hit_objects) and isinstance(hit_objects[hit_obj_idx], Spinner):
            hit_obj_idx += 1
        
        # All HitCircles and Sliders have been iterated over
        if hit_obj_idx >= len(hit_objects):
            break

        # Next HitCircle of Slider
        curr_hit_obj = hit_objects[hit_obj_idx]

        # Starting frame of current tap
        tap_start = tap_starts[tap_start_idx]
        """
            tap_start is either:
                - too early for current HitObject's window
                    move on to next iteration of tap_start
                - within current HitObject's window
                    check if tap was made within HitObject
                - too late for current HitObject's window
                    move on to the next HitObject
        """
        if tap_start.Time < curr_hit_obj.StartTime - (200 - 10 * diff_section.OverallDifficulty):
            # Move on to next tap_start
            tap_start_idx += 1
            pass
        
        hit_obj_tapped = False
        # Store frame where player potentially missed
        potential_miss_tap = None
        while tap_start.Time <= curr_hit_obj.StartTime + (200 - 10 * diff_section.OverallDifficulty):
            if IsWithinHitObject(curr_hit_obj, [tap_start.X, tap_start.Y], diff_section.CircleSize):
                # HitObject has been tapped!
                hit_obj_tapped = True
                hit_object_taps.append([curr_hit_obj, tap_start])
                tap_start_idx += 1
                hit_obj_idx += 1
                break
            else:
                if not potential_miss_tap:
                    potential_miss_tap = tap_start
                    # Encode that this is a miss in the Keys field by negating it
                    potential_miss_tap.Keys *= -1
                tap_start_idx += 1
                if tap_start_idx < len(tap_starts):
                    tap_start = tap_starts[tap_start_idx]
                else:
                    break
        if not hit_obj_tapped:
            hit_object_taps.append([curr_hit_obj, potential_miss_tap])
            hit_obj_idx += 1
    
    return hit_object_taps

def IsWithinHitObject(hit_obj, cursor_pos, cs):
    # Formula for HitCircle radius given CS
    hit_circle_radius = 54.4 - 4.48 * cs

    # Calculate distance between HitCircle center and cursor
    dist = (cursor_pos[X] - hit_obj.Position[X]) ** 2
    dist += ((cursor_pos[Y] - hit_obj.Position[Y]) ** 2)
    dist = dist ** (1 / 2)

    # Return whether cursor is within HitCircle
    return dist <= hit_circle_radius