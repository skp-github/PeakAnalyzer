def get_peaks_delta(self, peaks, frq):
    delta_list = []
    delta_one_six_peak = np.abs((np.sum(frq[peaks[0:3]]) / 3) - (np.sum(frq[peaks[15:18]]) / 3))
    delta_two_five_peak = np.abs((np.sum(frq[peaks[3:6]]) / 3) - (np.sum(frq[peaks[12:15]]) / 3))
    delta_three_four_peak = np.abs((np.sum(frq[peaks[6:9]]) / 3) - (np.sum(frq[peaks[9:12]]) / 3))
    delta_list.extend([delta_one_six_peak, delta_two_five_peak, delta_three_four_peak])
    return delta_list


def print_results(self, peaks_idle, frq_idle, peaks_active, frq_active):
    delta_f_idle_list = self.get_peaks_delta(peaks_idle, frq_idle)
    delta_f_active_list = self.get_peaks_delta(peaks_active, frq_active)
    print(f"Difference Between 1-6 Peak:{(delta_f_active_list[0] - delta_f_idle_list[0]) * 1e-9}")
    print(f"Difference Between 2-5 Peak:{(delta_f_active_list[1] - delta_f_idle_list[1]) * 1e-9}")
    print(f"Difference Between 3-4 Peak:{(delta_f_active_list[2] - delta_f_idle_list[2]) * 1e-9}")