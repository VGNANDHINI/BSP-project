# pages/2_📡_Frequency_Analysis.py

from components.data_loader import EEGDataLoader
from components.wavelet_analyzer import WaveletAnalyzer
from components.visualizer import EEGVisualizer
from components.ui_elements import UIElements
import pandas as pd 
import streamlit as st
import os

def main():
    st.set_page_config(page_title="Schizophrenia EEG Frequency Analysis", page_icon="📡")

    UIElements.display_usach_logo()

    st.title("Schizophrenia EEG Frequency Analysis (Wavelet)")

    # List available CSV files
    available_files = [f for f in os.listdir("data") if f.endswith(".csv")]
    if not available_files:
        st.warning("No EEG CSV files found in the 'data' folder.")
        return

    selected_file = st.selectbox("Select an EEG file to load", available_files)

    # Load EEG data
    eeg_loader = EEGDataLoader(selected_file)
    data = eeg_loader.load_data()

    if data is not None:
        channels = eeg_loader.get_channels()
        # Only show schizophrenia-relevant channels
        relevant_channels = [ch for ch in ["F3", "F4", "F7", "F8", "T3", "T4", "Cz", "Pz"] if ch in channels]
        if not relevant_channels:
            st.error("No schizophrenia-relevant channels found in the EEG data.")
            return

        channel = st.selectbox("Select a channel for frequency analysis", relevant_channels)

        if channel:
            signal = data[channel]
            sampling_rate = 256  # Clinical EEG standard

            # Visualize raw signal
            visualizer = EEGVisualizer(data, sampling_rate)
            total_duration = len(signal) / sampling_rate
            time_range = st.slider(
                "Select time range to analyze (seconds)",
                0.0,
                total_duration,
                (0.0, min(5.0, total_duration)),
                0.1
            )
            visualizer.plot_channels([channel], time_range)

            # Perform wavelet analysis
            wavelet_analyzer = WaveletAnalyzer(signal, sampling_rate)
            coefficients, frequencies = wavelet_analyzer.perform_wavelet_transform(time_range)

            # Plot wavelet transform heatmap
            wavelet_analyzer.plot_wavelet_transform(coefficients, frequencies, time_range)

            # Extract and display band power for schizophrenia-relevant bands
            band_power = wavelet_analyzer.extract_band_power(coefficients, frequencies)
            st.subheader(f"EEG Band Power - {channel}")

            # Use st.write instead of st.dataframe to avoid PyArrow issues
            st.write("Band power values:", band_power)


if __name__ == "__main__":
    main()
