# Home.py

import streamlit as st
from components.ui_elements import UIElements


def main():
    st.set_page_config(page_title="Schizophrenia EEG Analysis", page_icon="🧠", layout="wide")

    UIElements.display_usach_logo()

    st.title("Welcome to the Schizophrenia EEG Analysis Platform")

    st.markdown("""
    This platform allows you to upload and analyze EEG signals from schizophrenia patients. 
    Use the tabs below to explore the functionalities and analyze the EEG data for research or clinical purposes.
    """)

    tabs = st.tabs(["⚡ EEG Visualization", "📡 Frequency Analysis", "📊 Entropy Analysis"])

    with tabs[0]:
        st.header("⚡ EEG Visualization")
        st.markdown("""
        On this page, you can visualize EEG signals from **schizophrenia-relevant electrodes** (F3, F4, F7, F8, T3, T4, Cz, Pz).  
        This allows you to see the EEG data in the time domain and select specific time intervals for detailed inspection.

        ### Instructions:
        - 1️⃣ Upload a CSV file containing EEG data from schizophrenia patients.
        - 2️⃣ Select the electrode/channel and time range you wish to visualize.
        - 3️⃣ View the interactive EEG signal in the graph.
        """)

    with tabs[1]:
        st.header("📡 EEG Frequency Analysis")
        st.markdown("""
        This page allows you to perform **frequency analysis using Continuous Wavelet Transform (CWT)** on schizophrenia EEG signals.  
        You will be able to observe the **frequency spectrum over time**, focusing on bands relevant to schizophrenia research (Delta, Theta, Alpha, Beta, Gamma).

        ### Instructions:
        - 1️⃣ Upload a CSV file containing EEG data.
        - 2️⃣ Select the schizophrenia-relevant channel and time range for analysis.
        - 3️⃣ View the frequency spectrum and heatmaps to analyze EEG characteristics.
        """)

    with tabs[2]:
        st.header("📊 EEG Entropy Analysis")
        st.markdown("""
        On this page, you can perform **entropy analysis** on schizophrenia EEG signals to assess signal complexity.  
        Metrics such as Shannon Entropy, Approximate Entropy, and Sample Entropy will be calculated for selected channels.

        ### Instructions:
        - 1️⃣ Upload a CSV file containing EEG data.
        - 2️⃣ Select the channel, time range, and window size for entropy analysis.
        - 3️⃣ View the results in interactive line plots and bar charts.
        """)


if __name__ == "__main__":
    main()
