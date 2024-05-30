import unittest
import numpy as np
from scipy.signal import find_peaks
from peakanalyzer.peakanalyzer import PeakAnalyzer

class TestPeakAnalyzer(unittest.TestCase):
    def setUp(self):
        self.data_folder = 'data/'
        self.analyzer = PeakAnalyzer(self.data_folder)
        self.sample_data = np.array([2, 4, 6, 8, 10, 9, 7, 5, 3, 1])
        self.noisy_data = np.random.normal(0, 1, 100) + np.linspace(0, 1, 100)

    def test_get_peaks(self):
        peaks, _ = self.analyzer.get_peaks(self.noisy_data)

        # Manually find peaks for comparison
        expected_peaks, _ = find_peaks(-self.noisy_data,distance=5)

        # Assert that detected peaks match the expected peaks
        np.testing.assert_array_equal(peaks, expected_peaks)

    def test_chunk_array_by_sizes(self):

        data = np.arange(10)
        chunk_sizes = [3, 3, 4]

        chunks = self.analyzer.chunk_array_by_sizes(data, chunk_sizes)

        self.assertEqual(len(chunks), 3)
        np.testing.assert_array_equal(chunks[0], [0, 1, 2])
        np.testing.assert_array_equal(chunks[1], [3, 4, 5])
        np.testing.assert_array_equal(chunks[2], [6, 7, 8, 9])

        # Check error handling for invalid chunk sizes
        with self.assertRaises(ValueError):
            self.analyzer.chunk_array_by_sizes(data, [3, 3, 5])

    def test_smooth_data_with_empty_array(self):
        # Check error handling for empty array
        with self.assertRaises(ValueError):
            self.analyzer.smooth_data(np.array([]))
