def get_peaks(self, data, distance=5, dips=True):
    if dips:
        return find_peaks(-data, distance=distance)
    else:
        return find_peaks(data, distance=distance)