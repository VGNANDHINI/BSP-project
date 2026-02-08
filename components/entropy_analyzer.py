# components/entropy_analyzer.py

import neurokit2 as nk


class EntropyAnalyzer:
    """
    Calculates EEG entropy metrics relevant to schizophrenia analysis.
    Reduced entropy in EEG is often observed in schizophrenia patients.
    """

    def __init__(self, signal, sampling_rate=256):
        """
        Initialize with EEG signal and sampling rate.

        :param signal: EEG signal (1D array-like)
        :param sampling_rate: Sampling frequency in Hz (default 256 Hz)
        """
        self.signal = signal
        self.sampling_rate = sampling_rate

    def calculate_entropy_windows(self, window_size_sec=5):
        """
        Compute entropy metrics in sliding windows.

        :param window_size_sec: Window length in seconds
        :return: List of dictionaries containing entropy metrics per window
        """
        window_size = int(window_size_sec * self.sampling_rate)
        num_windows = len(self.signal) // window_size

        entropy_results = []

        for i in range(num_windows):
            start_idx = i * window_size
            end_idx = start_idx + window_size
            window_signal = self.signal[start_idx:end_idx]

            # Compute entropies for this window
            entropy_values = self._compute_entropies(window_signal)
            entropy_results.append(entropy_values)

        return entropy_results

    @staticmethod
    def _compute_entropies(window_signal):
        """
        Compute Sample, Approximate, and Permutation Entropy for a signal window.

        :param window_signal: 1D EEG signal array
        :return: Dictionary of entropy metrics
        """
        return {
            "Sample Entropy": nk.entropy_sample(window_signal)[0],
            "Approximate Entropy": nk.entropy_approximate(window_signal)[0],
            "Permutation Entropy": nk.entropy_permutation(window_signal)[0]
        }
