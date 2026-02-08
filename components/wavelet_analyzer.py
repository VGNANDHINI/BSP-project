# components/wavelet_analyzer.py

import numpy as np
import plotly.graph_objects as go
import streamlit as st
import pywt


class WaveletAnalyzer:
    """
    Performs wavelet-based frequency analysis of EEG signals for schizophrenia research.
    Focuses on delta, theta, alpha, beta, and gamma bands.
    """

    def __init__(self, signal, sampling_rate=256, min_freq=0.5, max_freq=50):
        """
        Initialize with EEG signal.

        :param signal: 1D EEG signal array
        :param sampling_rate: Sampling frequency in Hz (default 256)
        :param min_freq: Minimum frequency of interest (default 0.5 Hz)
        :param max_freq: Maximum frequency of interest (default 50 Hz)
        """
        self.signal = signal
        self.sampling_rate = sampling_rate
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.scales = np.arange(1, 128)  # scales for CWT

    def perform_wavelet_transform(self, time_range=(0, 5)):
        """
        Perform Continuous Wavelet Transform (CWT) on selected time range.

        :param time_range: Tuple (start_sec, end_sec)
        :return: coefficients (2D array), corresponding frequencies (1D array)
        """
        start_idx = int(time_range[0] * self.sampling_rate)
        end_idx = int(time_range[1] * self.sampling_rate)

        if end_idx > len(self.signal):
            st.warning("Time range exceeds signal length. Adjusting end index.")
            end_idx = len(self.signal)

        signal_slice = self.signal[start_idx:end_idx]

        # CWT using Morlet wavelet
        coefficients, _ = pywt.cwt(signal_slice, self.scales, 'cmor1.5-1.0')

        # Convert scales to frequencies
        frequencies = pywt.scale2frequency('cmor1.5-1.0', self.scales) * self.sampling_rate
        mask = (frequencies >= self.min_freq) & (frequencies <= self.max_freq)
        frequencies = frequencies[mask]
        coefficients = coefficients[mask, :]

        return coefficients, frequencies

    @staticmethod
    def plot_wavelet_transform(coefficients, frequencies, time_range=(0, 5)):
        """
        Plot the wavelet transform as a time-frequency heatmap.

        :param coefficients: 2D CWT coefficients
        :param frequencies: 1D array of frequencies
        :param time_range: Tuple (start_sec, end_sec)
        """
        if coefficients.size == 0 or len(frequencies) == 0:
            st.warning("No coefficients to plot.")
            return

        time = np.linspace(time_range[0], time_range[1], num=coefficients.shape[1])

        heatmap = go.Heatmap(
            z=np.abs(coefficients),
            x=time,
            y=frequencies,
            colorscale='Viridis',
            zmin=0,
            zmax=np.max(np.abs(coefficients))
        )

        layout = go.Layout(
            title=f"EEG Time-Frequency (Wavelet) from {time_range[0]}s to {time_range[1]}s",
            xaxis_title="Time (s)",
            yaxis_title="Frequency (Hz)"
        )

        fig = go.Figure(data=[heatmap], layout=layout)
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def extract_band_power(coefficients, frequencies, bands=None):
        """
        Compute average power in standard EEG bands.

        :param coefficients: 2D CWT coefficients
        :param frequencies: 1D frequency array
        :param bands: dict of EEG bands {name: (low, high)}
        :return: dict of band powers
        """
        if bands is None:
            bands = {
                "Delta": (0.5, 4),
                "Theta": (4, 8),
                "Alpha": (8, 12),
                "Beta": (12, 30),
                "Gamma": (30, 50)
            }

        band_power = {}
        for band, (low, high) in bands.items():
            mask = (frequencies >= low) & (frequencies <= high)
            if np.any(mask):
                band_power[band] = np.mean(np.abs(coefficients[mask, :])**2)
            else:
                band_power[band] = 0
        return band_power
