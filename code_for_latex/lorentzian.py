def lorentzian(self, x, amp, cen, wid):
    return -amp * wid ** 2 / ((x - cen) ** 2 + wid ** 2)

def fit_all_clusters(self, x, *params):
    assert len(params) == 18 * 3
    result = np.zeros_like(x)
    for i in range(0, len(params), 3):
        amp, cen, wid = params[i:i + 3]
        result += self.lorentzian(x, amp, cen, wid)
    return result

def generate_parameters_for_fitting(self, x, y, peaks):
    parameter_list = []
    for index in range(0, len(peaks), 3):
        width = (x[peaks[index + 2]] - x[peaks[index]]) / 2
        peak_1 = [y[peaks[index]], x[peaks[index]], width]
        peak_2 = [y[peaks[index + 1]], x[peaks[index + 1]], width]
        peak_3 = [y[peaks[index + 2]], x[peaks[index + 2]], width]
        parameter_list.extend(peak_1)
        parameter_list.extend(peak_2)
        parameter_list.extend(peak_3)
    return parameter_list

def curve_fitting(self, x, y, peaks, depth):
    initial_guesses = self.generate_parameters_for_fitting(peaks)
    popt, pcov = curve_fit(self.fit_all_clusters, x, y, p0=initial_guesses,
                           maxfev=depth)