from Enums.Replays.StandardKeys import StandardKeys as Key

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
        if keys[idx] in possible_transitions:
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