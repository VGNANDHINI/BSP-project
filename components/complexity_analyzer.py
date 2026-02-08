# components/complexity_analyzer.py

import neurokit2 as nk
import pandas as pd


class ComplexityAnalyzer:
    """
    Class to calculate EEG signal complexity metrics relevant to schizophrenia.
    Focuses on metrics like Sample Entropy, Higuchi Fractal Dimension, and Permutation Entropy.
    Reduced complexity is often observed in schizophrenia patients.
    """

    def __init__(self, signal, sampling_rate=256):
        """
        Initialize with EEG signal data.

        :param signal: EEG signal data (1D array-like)
        :param sampling_rate: Sampling frequency of the EEG signal (default 256 Hz)
        """
        self.signal = signal
        self.sampling_rate = sampling_rate

    def calculate_complexity(self):
        """
        Calculate schizophrenia-relevant complexity metrics.

        Returns:
            - complexity_df: pandas DataFrame with computed metrics
            - complexity_info: dictionary with interpretation notes
        """
        complexity_info = {}

        # Compute Sample Entropy
        samp_entropy = nk.entropy_sample(self.signal)
        complexity_info['Sample Entropy'] = samp_entropy

        # Compute Higuchi Fractal Dimension
        higuchi_fd = nk.complexity_higuchi(self.signal)
        complexity_info['Higuchi FD'] = higuchi_fd

        # Compute Permutation Entropy
        perm_entropy = nk.entropy_permutation(self.signal)
        complexity_info['Permutation Entropy'] = perm_entropy

        # Create DataFrame for easy visualization
        complexity_df = pd.DataFrame([complexity_info])

        return complexity_df, complexity_info
