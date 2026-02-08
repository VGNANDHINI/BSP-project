# pages/1_⚡_EEG_Visualization.py

from components.data_loader import EEGDataLoader
from components.visualizer import EEGVisualizer
from components.ui_elements import UIElements
import streamlit as st
import os


def main():
    st.set_page_config(page_title="Schizophrenia EEG Visualization", page_icon="🧠")

    # Display logo
    UIElements.display_usach_logo()

    st.title("Schizophrenia EEG Visualization")
   
    # List available CSV files in the data directory
    available_files = [f for f in os.listdir("data") if f.endswith(".csv")]
    if not available_files:
        st.warning("No EEG CSV files found in the 'data' folder.")
        return

    selected_file = st.selectbox("Select an EEG file to load", available_files)

    # Load EEG data
    eeg_loader = EEGDataLoader(selected_file)
    data = eeg_loader.load_data()

    if data is not None:
        # Display metadata
        st.markdown(f"**Sampling rate:** 256 Hz (default for clinical EEG)")
        st.markdown("**Relevant electrodes:** F3, F4, F7, F8, T3, T4, Cz, Pz")
        st.markdown("**Reference electrode:** Mastoid or behind the ear")

        # Instantiate the visualizer
        visualizer = EEGVisualizer(data, sampling_rate=256)

        # Select time range
        total_duration = len(data) / visualizer.sampling_rate
        time_range = st.slider(
            "Select the time range to visualize (seconds)",
            min_value=0.0,
            max_value=total_duration,
            value=(0.0, min(5.0, total_duration)),
            step=0.1
        )

        # Default schizophrenia-relevant channels
        channels = [ch for ch in ["F3", "F4", "F7", "F8", "T3", "T4", "Cz", "Pz"] if ch in data.columns]

        if channels:
            visualizer.plot_channels(channels, time_range)
        else:
            st.error("No schizophrenia-relevant channels found in the loaded EEG file.")


if __name__ == "__main__":
    main()
