# components/ui_elements.py

import streamlit as st

class UIElements:
    """
    Handles UI elements for the schizophrenia EEG analysis dashboard.
    Includes logos, headers, and section titles.
    """

    @staticmethod
    def display_usach_logo():
        """
        Displays a dashboard header with a logo and title.
        """
        
        st.markdown(
            """
            <h1 style='text-align:center; color:#4B0082; font-family:Arial;'>
                Schizophrenia EEG Analysis Dashboard
            </h1>
            <hr style='border:2px solid #4B0082; margin-top:10px; margin-bottom:20px;'>
            """,
            unsafe_allow_html=True
        )

    @staticmethod
    def display_section_title(title: str):
        """
        Displays a section title for different pages or analyses.

        :param title: Title text to display
        """
        st.markdown(
            f"""
            <h2 style='color:#1E90FF; margin-top:30px; font-family:Arial;'>{title}</h2>
            <hr style='border:1px solid #ccc; margin-bottom:15px;'>
            """,
            unsafe_allow_html=True
        )
