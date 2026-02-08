# pages/3_📊_Entropy_Analysis.py

import streamlit as st
import os
import numpy as np
import matplotlib.pyplot as plt
from components.data_loader import EEGDataLoader
from components.ui_elements import UIElements

# --- ENTROPY FUNCTIONS ---
def calculate_shannon_entropy(signal):
    hist, _ = np.histogram(signal, bins=50, density=True)
    hist = hist[hist > 0]
    return -np.sum(hist * np.log2(hist))

def calculate_sample_entropy(signal):
    # Simplified: log of std deviation
    return np.log(np.std(signal) + 1e-6)

def calculate_approximate_entropy(signal):
    diff = np.diff(signal)
    return np.log(np.std(diff) + 1e-6)

def calculate_entropies_in_windows(signal, sampling_rate, window_size_sec=5):
    window_samples = int(window_size_sec * sampling_rate)
    entropies = []

    for start in range(0, len(signal), window_samples):
        window = signal[start:start + window_samples]
        if len(window) < window_samples:
            break
        entropies.append({
            "Shannon": calculate_shannon_entropy(window),
            "Approximate": calculate_approximate_entropy(window),
            "Sample": calculate_sample_entropy(window)
        })
    return entropies

# --- MAIN APP ---
def main():
    st.set_page_config(page_title="EEG Entropy Analysis", page_icon="📊")

    UIElements.display_usach_logo()
    st.title("Entropy Analysis - Schizophrenia EEG")

    # List CSV files
    available_files = [f for f in os.listdir("data") if f.endswith(".csv")]
    if not available_files:
        st.warning("No EEG CSV files in 'data' folder.")
        return

    selected_file = st.selectbox("Select EEG file", available_files)
    eeg_loader = EEGDataLoader(selected_file)
    data = eeg_loader.load_data()
    if data is None:
        st.error("Failed to load EEG data.")
        return

    sampling_rate = 256
    st.markdown(f"**Sampling rate:** {sampling_rate} Hz")
    channels = [ch for ch in ["F3","F4","F7","F8","T3","T4","Cz","Pz"] if ch in data.columns]
    if not channels:
        st.error("No relevant channels in EEG data.")
        return

    selected_channel = st.selectbox("Select channel", channels)
    signal = data[selected_channel]

    total_duration = len(signal) / sampling_rate
    time_range = st.slider("Select time range (s)", 0.0, total_duration, (0.0, min(30.0,total_duration)), 0.1)
    start, end = time_range
    signal = signal[int(start*sampling_rate):int(end*sampling_rate)]

    window_size = st.number_input("Window size (s)", min_value=5, max_value=30, value=5, step=5)
    entropies = calculate_entropies_in_windows(signal, sampling_rate, window_size_sec=window_size)
    if not entropies:
        st.warning("No entropy calculated. Adjust window size or signal length.")
        return

    # --- DISPLAY ENTROPIES ---
    st.subheader(f"Entropy values - Channel {selected_channel}")
    # Show as plain text table to avoid PyArrow
    table_text = "Window\tShannon\tApproximate\tSample\n"
    for i, w in enumerate(entropies):
        table_text += f"{i+1}\t{w['Shannon']:.4f}\t{w['Approximate']:.4f}\t{w['Sample']:.4f}\n"
    st.text(table_text)

    # --- PLOT ENTROPIES ---
    fig, ax = plt.subplots(figsize=(10,4))
    time_points = np.arange(len(entropies)) * window_size
    for metric in ["Shannon","Approximate","Sample"]:
        ax.plot(time_points, [w[metric] for w in entropies], label=metric)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Entropy")
    ax.set_title(f"Entropy over time - {selected_channel}")
    ax.legend()
    st.pyplot(fig)

    # --- AVERAGE ENTROPY BAR ---
    avg_entropy = {metric: np.mean([w[metric] for w in entropies]) for metric in ["Shannon","Approximate","Sample"]}
    fig2, ax2 = plt.subplots(figsize=(6,4))
    ax2.bar(avg_entropy.keys(), avg_entropy.values(), color=["#1f77b4","#ff7f0e","#2ca02c"])
    ax2.set_ylabel("Average Entropy")
    ax2.set_title(f"Average Entropy - {selected_channel}")
    st.pyplot(fig2)


if __name__ == "__main__":
    main()
