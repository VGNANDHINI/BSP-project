# components/visualizer.py

import plotly.graph_objects as go
import streamlit as st


class EEGVisualizer:
    """
    Visualizes EEG signals, entropy, and complexity metrics for schizophrenia analysis.
    """

    def __init__(self, data, sampling_rate=256):
        """
        Initialize the visualizer with EEG data.

        :param data: pandas DataFrame containing EEG data
        :param sampling_rate: Sampling rate in Hz (default 256 Hz)
        """
        self.data = data
        self.sampling_rate = sampling_rate
        self.time = [i / sampling_rate for i in range(len(data))]

    def plot_channels(self, channels=None, time_range=(0, 5)):
        """
        Plots selected EEG channels over a given time range.

        :param channels: List of column names to plot (default: schizophrenia-relevant channels)
        :param time_range: Tuple (start_sec, end_sec) to display
        """
        if channels is None:
            channels = [ch for ch in ["F3", "F4", "F7", "F8", "T3", "T4", "Cz", "Pz"] if ch in self.data.columns]

        start_idx = int(time_range[0] * self.sampling_rate)
        end_idx = int(time_range[1] * self.sampling_rate)

        if start_idx >= len(self.data) or end_idx > len(self.data):
            st.warning("Time range exceeds data length. Adjusting to available range.")
            start_idx = max(0, min(start_idx, len(self.data)))
            end_idx = len(self.data)

        fig = go.Figure()

        for ch in channels:
            if ch in self.data.columns:
                fig.add_trace(go.Scatter(
                    x=self.time[start_idx:end_idx],
                    y=self.data[ch].iloc[start_idx:end_idx],
                    mode='lines',
                    name=ch
                ))

        if fig.data:
            fig.update_layout(
                title="EEG Channels - Schizophrenia Relevant",
                xaxis_title="Time (s)",
                yaxis_title="Amplitude (µV)",
                legend_title="Electrode"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("No schizophrenia-relevant channels available in the data.")

    @staticmethod
    def plot_entropy_over_time(entropy_windows_ch1, entropy_windows_ch2, window_size_sec):
        """
        Plots entropy over time for two channels for Sample, Approximate, and Permutation Entropy.

        :param entropy_windows_ch1: List of dicts from channel 1
        :param entropy_windows_ch2: List of dicts from channel 2
        :param window_size_sec: Window size in seconds
        """
        if not entropy_windows_ch1 or not entropy_windows_ch2:
            st.warning("Entropy data is empty. Cannot plot.")
            return

        times = [i * window_size_sec for i in range(len(entropy_windows_ch1))]

        fig = go.Figure()
        colors = {"Sample Entropy": "blue", "Approximate Entropy": "green", "Permutation Entropy": "red"}

        # Channel 1
        for metric, color in colors.items():
            values = [window.get(metric, None) for window in entropy_windows_ch1]
            fig.add_trace(go.Scatter(
                x=times, y=values, mode='lines+markers',
                marker=dict(symbol="circle", size=8, color=color),
                line=dict(width=1),
                name=f"Ch1 - {metric}"
            ))

        # Channel 2
        for metric, color in colors.items():
            values = [window.get(metric, None) for window in entropy_windows_ch2]
            fig.add_trace(go.Scatter(
                x=times, y=values, mode='lines+markers',
                marker=dict(symbol="triangle-up", size=8, color=color),
                line=dict(width=1),
                name=f"Ch2 - {metric}"
            ))

        fig.update_layout(
            title="Entropy Over Time - Schizophrenia EEG",
            xaxis_title="Time (s)",
            yaxis_title="Entropy Value",
            legend_title="Metrics"
        )
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def plot_average_entropy_bars(entropy_ch1, entropy_ch2, labels):
        """
        Plots bar chart comparing average entropy for two channels.

        :param entropy_ch1: List of average entropy values for channel 1
        :param entropy_ch2: List of average entropy values for channel 2
        :param labels: Labels for each entropy metric
        """
        if not entropy_ch1 or not entropy_ch2:
            st.warning("Entropy data is empty. Cannot plot bars.")
            return

        fig = go.Figure()

        fig.add_trace(go.Bar(x=labels, y=entropy_ch1, name="Channel 1", marker_color='orange'))
        fig.add_trace(go.Bar(x=labels, y=entropy_ch2, name="Channel 2", marker_color='purple'))

        fig.update_layout(
            title="Average Entropy Comparison",
            xaxis_title="Entropy Metric",
            yaxis_title="Value",
            barmode="group"
        )
        st.plotly_chart(fig)
