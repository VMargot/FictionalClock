import time
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import streamlit as st

from clock_logic import (get_day_night_durations, get_fictif_hour,
                         get_timezone_offset, plot_clock, second_duration)

# Script Streamlit
st.markdown("<h1 style='text-align: center; color: black;'>Adjusted fictitious clock</h1>",
            unsafe_allow_html=True)
# Input : Latitude, Longitude, Date
latitude = st.sidebar.number_input("Latitude", value=48.8566, min_value=-90.0, max_value=90.0)  # Paris
longitude = st.sidebar.number_input("Longitude", value=2.3522, min_value=-180.0, max_value=180.0)  # Paris
date = st.sidebar.date_input("Date", value=datetime.now().date())
timezone, utc_offset = get_timezone_offset(latitude, longitude)

# Calcul des durées jour/nuit
day_duration, night_duration = get_day_night_durations(date, latitude)

# Heure actuelle réelle
current_time = datetime.now(timezone)
# Heure fictive
fictif_time = get_fictif_hour(current_time, day_duration, night_duration,
                              latitude, longitude, timezone, utc_offset)
fictif_second_duration = second_duration(current_time, day_duration,
                                         night_duration, latitude, longitude,
                                         utc_offset)

st.sidebar.write(f"Day duration: {day_duration:.2f} hours")
st.sidebar.write(f"Night duration: {night_duration:.2f} hours")

placeholder = st.empty()
while True:
    current_time = datetime.now(timezone)
    with placeholder.container():
        fig = plot_clock(fictif_time.hour, fictif_time.minute,
                         fictif_time.second)
        st.pyplot(fig)

        st.write(f"Current time: {current_time.strftime('%H:%M:%S')}")
        st.write(f"Ajusted time : {fictif_time.strftime('%H:%M:%S')}")
        st.write(f"Duration of adjusted second: {round(fictif_second_duration, 3)}")

    fictif_second_duration = second_duration(current_time, day_duration,
                                             night_duration, latitude,
                                             longitude, utc_offset)
    fictif_time = fictif_time + timedelta(seconds=1)
    time.sleep(fictif_second_duration)
    plt.close(fig)
