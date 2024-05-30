def get_clip_range(self, step_interval_list, clip_percentage=.10):
    return int(step_interval_list[0] * clip_percentage)
