# components/data_loader.py

import os
import pandas as pd
import streamlit as st
from scipy.signal import butter, filtfilt


class EEGDataLoader:
    """
    Class to handle loading and preprocessing EEG data specifically for schizophrenia analysis.
    Focuses on schizophrenia-relevant channels and basic preprocessing.
    """

    # Channels most relevant in schizophrenia studies
    SCHIZO_CHANNELS = ["F3", "F4", "F7", "F8", "T3", "T4", "Cz", "Pz"]

    def __init__(self, file_name, sampling_rate=256):
        """
        Initialize the data loader.

        :param file_name: CSV file in the 'data' directory
        :param sampling_rate: EEG sampling frequency in Hz
        """
        self.file_path = os.path.join("data", file_name)
        self.data = None
        self.sampling_rate = sampling_rate

    def load_data(self):
        """
        Loads EEG data from CSV.

        :return: pandas DataFrame containing EEG data or None if an error occurs.
        """
        try:
            self.data = pd.read_csv(self.file_path, delimiter=",")
            st.success(f"Successfully loaded {self.file_path}")
            return self.data
        except FileNotFoundError:
            st.error(f"The file '{self.file_path}' was not found.")
            return None
        except pd.errors.EmptyDataError:
            st.error(f"The file '{self.file_path}' is empty.")
            return None
        except pd.errors.ParserError:
            st.error(f"There was an error parsing the file '{self.file_path}'.")
            return None

    def get_channels(self):
        """
        Returns available EEG channels that are relevant for schizophrenia analysis.

        :return: List of schizophrenia-related EEG channels present in the data.
        """
        if self.data is not None:
            available_channels = [ch for ch in self.SCHIZO_CHANNELS if ch in self.data.columns]
            if not available_channels:
                st.warning("None of the schizophrenia-relevant channels were found in the data.")
            return available_channels
        else:
            st.error("EEG data has not been loaded.")
            return []

    def bandpass_filter(self, low_freq=1, high_freq=50):
        """
        Apply a Butterworth bandpass filter to all schizophrenia-relevant channels.

        :param low_freq: Low cutoff frequency in Hz
        :param high_freq: High cutoff frequency in Hz
        :return: Filtered pandas DataFrame
        """
        if self.data is None:
            st.error("EEG data has not been loaded.")
            return None

        def butter_bandpass(lowcut, highcut, fs, order=5):
            nyq = 0.5 * fs
            low = lowcut / nyq
            high = highcut / nyq
            b, a = butter(order, [low, high], btype='band')
            return b, a

        b, a = butter_bandpass(low_freq, high_freq, self.sampling_rate)
        filtered_data = self.data.copy()

        for ch in self.get_channels():
            filtered_data[ch] = filtfilt(b, a, self.data[ch])

        return filtered_data
