def smooth_data(self, data, window_length=15, poly_order=3):
    return savgol_filter(data, window_length, poly_order)