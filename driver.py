import numpy as np
from peakanalyzer.peakanalyzer import PeakAnalyzer
import time

DATAFOLDER = "data/"
WINDOW_LENGTH = 20
POLY_ORDER = 3
NUM_PEAKS_IN_CLUSTER = 3

if __name__ == "__main__":
    try:
        # Create PeakAnalyzer object
        pa_obj = PeakAnalyzer(DATAFOLDER)

        start_time = time.time()

        # Load all filenames
        idle_filenames = pa_obj.get_idle_fname_list()
        active_filenames = pa_obj.get_active_fname_list()

        for idle_fname in idle_filenames:
            for active_fname in active_filenames:
                try:
                    # Load data
                    idle_frq, idle_data, idle_step_intervals = pa_obj.load_data(idle_fname)
                    active_frq, active_data, active_step_intervals = pa_obj.load_data(active_fname)

                    # Print statistics
                    pa_obj.print_data_statistics(idle_data)
                    pa_obj.print_data_statistics(active_data)

                    # Normalize
                    idle_data = pa_obj.normalise_dataset(idle_data)
                    active_data = pa_obj.normalise_dataset(active_data)

                    # Smooth data
                    idle_smooth = pa_obj.smooth_data(idle_data[:, 0, 0], window_length=WINDOW_LENGTH, poly_order=POLY_ORDER)
                    active_smooth = pa_obj.smooth_data(active_data[:, 0, 0], window_length=WINDOW_LENGTH, poly_order=POLY_ORDER)

                    # Clipping outliers/tails
                    idle_clip_range = pa_obj.get_clip_range(idle_step_intervals)
                    idle_step_intervals[0] -= idle_clip_range
                    idle_step_intervals[-1] -= idle_clip_range
                    idle_smooth_clipped, idle_frq_clipped = idle_smooth[idle_clip_range:-idle_clip_range], idle_frq[idle_clip_range:-idle_clip_range]
                    active_clip_range = pa_obj.get_clip_range(active_step_intervals)
                    active_step_intervals[0] -= active_clip_range
                    active_step_intervals[-1] -= active_clip_range
                    active_smooth_clipped, active_frq_clipped = active_smooth[active_clip_range:-active_clip_range], active_frq[active_clip_range:-active_clip_range]

                    # Find peaks (dips in our case)
                    # Process array in chunks
                    idle_chunked_list = pa_obj.chunk_array_by_sizes(idle_smooth_clipped, idle_step_intervals)
                    active_chunked_list = pa_obj.chunk_array_by_sizes(active_smooth_clipped, active_step_intervals)

                    active_start_step = 0
                    active_peak_list = []
                    idle_start_step = 0
                    idle_peak_list = []

                    for idle_chunk_data, active_chunk_data in zip(idle_chunked_list, active_chunked_list):
                        idle_peaks, _ = pa_obj.get_peaks(idle_chunk_data)
                        idle_peak_heights = [(idle_chunk_data[peak], peak + idle_start_step) for peak in idle_peaks]
                        # Sort peaks based on height i.e. get the 3 main peaks in the segment
                        idle_sorted_peak_list = sorted(idle_peak_heights, key=lambda x: x[0])[:NUM_PEAKS_IN_CLUSTER]
                        idle_start_step += len(idle_chunk_data)
                        idle_peak_list.extend(idle_sorted_peak_list)
                        active_peaks, _ = pa_obj.get_peaks(active_chunk_data)
                        active_peak_heights = [(active_chunk_data[peak], peak + active_start_step) for peak in active_peaks]
                        active_sorted_peak_list = sorted(active_peak_heights, key=lambda x: x[0])[:NUM_PEAKS_IN_CLUSTER]
                        active_start_step += len(active_chunk_data)
                        active_peak_list.extend(active_sorted_peak_list)

                    # Sort peaks based on index i.e. get the right order of peaks
                    sorted_idle_peaks = sorted(idle_peak_list, key=lambda x: x[1])
                    sorted_idle_peaks = np.array([p[1] for p in sorted_idle_peaks])
                    sorted_active_peaks = sorted(active_peak_list, key=lambda x: x[1])
                    sorted_active_peaks = np.array([p[1] for p in sorted_active_peaks])

                    # Visualize peaks
                    pa_obj.visualise_peaks(idle_frq_clipped, idle_smooth_clipped, sorted_idle_peaks, 'Detected and Filtered Peaks in the Idle Wave', color="#E493B3")
                    pa_obj.visualise_peaks(active_frq_clipped, active_smooth_clipped, sorted_active_peaks, 'Detected and Filtered Peaks in the Active Wave', color="#51829B")

                    pa_obj.print_results(sorted_idle_peaks, idle_frq_clipped, sorted_active_peaks, active_frq_clipped)
                    end_time = time.time()
                    print(f"Total execution time without curve fitting: {end_time - start_time} seconds")

                    # Additionally fit a curve using triple lorentzian distribution
                    idle_wave_parameters = pa_obj.curve_fitting(idle_frq_clipped, idle_smooth_clipped,
                                                                sorted_idle_peaks)
                    active_wave_parameters = pa_obj.curve_fitting(active_frq_clipped, active_smooth_clipped,
                                                                  sorted_active_peaks)

                except Exception as e:
                    print(f"Error processing files {idle_fname} and {active_fname}: {str(e)}")
    except Exception as e:
        print(f"Failed to initialize PeakAnalyzer with data folder '{DATAFOLDER}': {str(e)}")
