import os
import numpy as np
import yaml
from scipy.signal import savgol_filter, find_peaks
from scipy.optimize import curve_fit
from esr import linep2dp
import matplotlib.pyplot as plt

class PeakAnalyzer:
    def __init__(self, datafolder):
        self.idle_waves_fnames, self.active_waves_fnames = self.load_fnames(datafolder)
    def smooth_data(self, data, window_length=15, poly_order=3):
        if len(data) <= 0:
            raise ValueError("Provided data for data smoothing is empty")
        return savgol_filter(data, window_length, poly_order)
    def lorentzian(self, x, amp, cen, wid):
        return -amp * wid ** 2 / ((x - cen) ** 2 + wid ** 2)

    def fit_all_clusters(self, x, *params):
        if len(params) != 18*3:
            raise ValueError("No. of params for curve fitting is incorrect")
        result = np.zeros_like(x)
        for i in range(0, len(params), 3):
            amp, cen, wid = params[i:i + 3]
            result += self.lorentzian(x, amp, cen, wid)
        return result

    def visualize_data(self, x, y, title='', xaxis_title='X-axis', yaxis_title='Y-axis',
                            line_color='royalblue'):
        linep2dp(
                [f * 1e-9 for f in x],
                y,
                title=title,
                xaxis_title=xaxis_title,
                yaxis_title=yaxis_title,
                color=line_color
            )
    def visualise_peaks(self, x, y, peaks, title="", color="blue"):
        plt.figure(figsize=(10, 5))
        plt.plot([f * 1e-9 for f in x], y, label='Smoothed Clipped Data', color=color)
        plt.scatter([f * 1e-9 for f in x[peaks]], y[peaks], color='red', s=50, label='Detected Peaks', zorder=2.5)
        plt.title(title)
        plt.xlabel('Frequency GHz')
        plt.ylabel('Normalized Intensity')
        plt.legend()
        plt.grid(True)
        plt.show()
    def chunk_array_by_sizes(self, data, chunk_sizes):
        chunks = []
        start_index = 0
        for size in chunk_sizes:
            if start_index + size > len(data):
                raise ValueError("Chunk sizes exceed the length of the data.")
            end_index = start_index + size
            chunk = data[start_index:end_index]
            chunks.append(chunk)
            start_index = end_index

        return chunks

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

    def curve_fitting(self, x, y, peaks, depth=200000):
        if len(peaks) != 18:
            raise ValueError("No. of peaks for curve fitting is incorrect")
        initial_guesses = self.generate_parameters_for_fitting(x, y, peaks)
        popt, pcov = curve_fit(self.fit_all_clusters, x, y, p0=initial_guesses,
                               maxfev=depth)
        return popt, pcov

    def get_clip_range(self, step_interval_list, clip_percentage=.10):
        if len(step_interval_list) <= 0:
            raise ValueError("Step interval list is empty")
        return int(step_interval_list[0] * clip_percentage)

    def get_peaks_delta(self, peaks, frq):
        delta_list = []
        if len(peaks) != 18:
            raise ValueError("No. of peaks for peak delta is incorrect")
        delta_one_six_peak = np.abs((np.sum(frq[peaks[0:3]]) / 3) - (np.sum(frq[peaks[15:18]]) / 3))
        delta_two_five_peak = np.abs((np.sum(frq[peaks[3:6]]) / 3) - (np.sum(frq[peaks[12:15]]) / 3))
        delta_three_four_peak = np.abs((np.sum(frq[peaks[6:9]]) / 3) - (np.sum(frq[peaks[9:12]]) / 3))
        delta_list.extend([delta_one_six_peak, delta_two_five_peak, delta_three_four_peak])
        return delta_list

    def print_results(self, peaks_idle, frq_idle, peaks_active, frq_active):
        if len(peaks_idle) != 18 and len(peaks_active) !=18:
            raise ValueError("No. of peaks for calculation is incorrect")
        delta_f_idle_list = self.get_peaks_delta(peaks_idle, frq_idle)
        delta_f_active_list = self.get_peaks_delta(peaks_active, frq_active)
        if len(delta_f_idle_list) !=3 and len(delta_f_active_list) !=3:
            raise ValueError("No. of peaks for calculation is incorrect")
        print(f"Difference Between 1-6 Peak:{(delta_f_active_list[0]-delta_f_idle_list[0])*1e-9}")
        print(f"Difference Between 2-5 Peak:{(delta_f_active_list[1]-delta_f_idle_list[1])*1e-9}")
        print(f"Difference Between 3-4 Peak:{(delta_f_active_list[2]-delta_f_idle_list[2])*1e-9}")

    def load_fnames(self, datafolder):
        subdir = [ "without_current/", "with_current/"]
        if not os.path.isdir(datafolder+subdir[0]) or not os.path.isdir(datafolder+subdir[1]):
            raise ValueError("The specified directory does not exist.")
        idle_files, active_files = os.listdir(datafolder+subdir[0]), os.listdir(datafolder+subdir[1])
        idle_fname_list = [datafolder+subdir[0] + file.split(".npy")[0] for file in idle_files if os.path.isfile(os.path.join(datafolder+subdir[0], file)) and file.endswith(".npy")]
        active_fname_list = [datafolder+subdir[1] +file.split(".npy")[0] for file in active_files if os.path.isfile(os.path.join(datafolder + subdir[1], file)) and file.endswith(".npy")]
        return idle_fname_list, active_fname_list

    def get_idle_fname_list(self):
        return self.idle_waves_fnames

    def get_active_fname_list(self):
        return self.active_waves_fnames

    def load_data(self,filename):
       y = np.load(f"{filename}.npy")
       with open(f"{filename}.yaml","r") as f:
            cfg = yaml.safe_load(f)
            frq = cfg["frequency_values"]
            step_intervals = cfg["step_intervals"]
       return np.array(frq), y, np.array(step_intervals)

    def normalise_dataset(self, data):
        if len(data) <= 0 or data.shape[0] < 2:
            raise ValueError("Provided data for data normalisation doesn't have the right dimensions")
        return np.sum(data[0] / data[1], axis=1)

    def plot_image(self, data, title, cmap="viridis"):
        plt.figure(figsize=(8, 6))
        plt.imshow(data, cmap=cmap, interpolation='nearest')  # Use 'gray' for grayscale image
        plt.title(title)
        plt.xlabel('Column Index')
        plt.ylabel('Row Index')
        plt.show()

    def print_data_statistics(self, data):
        print("Array Shape:", data.shape)
        print("Overall Mean In Dimension 1:", np.mean(data[0]))
        print("Overall Mean In Dimension 2:", np.mean(data[1]))
        print("Overall Standard Deviation In Dimension 1:", np.std(data[0]))
        print("Overall Standard Deviation In Dimension 2:", np.std(data[1]))
        self.plot_image(data[0, 0, 0, :, :], title=f"Single 50x50 image")

    def get_peaks(self, data, distance=5, dips=True):
        if len(data) <= 0:
            raise ValueError("Provided data for peak finidng is empty")
        if dips:
            return find_peaks(-data, distance=distance)
        else:
            return find_peaks(data, distance=distance)