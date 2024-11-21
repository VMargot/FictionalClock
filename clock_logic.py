import math
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
import pytz
from suntime import Sun
from timezonefinder import TimezoneFinder


def get_timezone_offset(latitude, longitude):
    """
    Obtenir le fuseau horaire GMT/UTC à partir de la latitude et de la longitude.
    """
    # Trouver le fuseau horaire
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=latitude, lng=longitude)

    if timezone_str is None:
        return None, None

    # Récupérer le décalage UTC
    timezone = pytz.timezone(timezone_str)
    now = datetime.now(timezone)
    utc_offset = now.utcoffset().total_seconds() / 3600  # Décalage en heures

    return timezone, utc_offset


def get_day_night_durations(date, latitude):
    phi = math.radians(latitude)
    day_of_year = date.timetuple().tm_yday
    declination = math.radians(-23.44 * math.cos(2 * math.pi * (day_of_year + 10) / 365))
    try:
        hour_angle = math.acos(-math.tan(phi) * math.tan(declination))
    except ValueError:
        hour_angle = 0 if latitude > 66.5 or latitude < -66.5 else math.pi
    day_duration = (24 / math.pi) * hour_angle
    night_duration = 24 - day_duration
    return day_duration, night_duration


def second_duration(current_time, day_duration, night_duration, latitude,
                    longitude, utc_offset):
    sun = Sun(latitude, longitude)
    today_sunrise = sun.get_local_sunrise_time(current_time)
    today_sunset = sun.get_local_sunset_time(current_time + timedelta(days=1))

    time_in_seconds = current_time.hour * 3600 + current_time.minute * 60 + current_time.second

    today_sunrise_in_seconde = (today_sunrise.hour + utc_offset) * 3600 \
        + today_sunrise.minute * 60 + today_sunrise.second
    today_sunset_in_seconde = (today_sunset.hour + utc_offset) * 3600 \
        + today_sunset.minute * 60 + today_sunset.second

    day_start = 6 * 3600
    day_end = today_sunrise_in_seconde + day_duration * 3600
    night_start = 18 * 3600
    night_end = today_sunset_in_seconde + night_duration * 3600

    total_duration = day_duration + night_duration
    amplitude = abs(day_duration - night_duration) / total_duration

    if day_start <= time_in_seconds < day_end:  # Période de jour
        t_real_day = (time_in_seconds - day_start) / (day_end - day_start)
        phase = t_real_day * math.pi
        modulation = math.sin(phase)  # Sinus croissant/décroissant
    elif night_start <= time_in_seconds < night_end:  # Période de nuit
        t_real_night = (time_in_seconds - night_start) / (night_end - night_start)
        phase = t_real_night * math.pi
        modulation = -math.sin(phase)  # Sinus inversé pour la nuit
    else:
        modulation = 0  # Hors périodes définies

    # Ajustement de la durée : + amplitude pour la nuit longue, - pour le jour long
    if night_duration > day_duration:
        return 1 + amplitude * modulation  # Secondes plus longues la nuit
    else:
        return 1 - amplitude * modulation  # Secondes plus longues le jour


def get_fictif_hour(current_time, day_duration, night_duration, latitude,
                    longitude, timezone, utc_offset):
    sun = Sun(latitude, longitude)
    today_sunrise = sun.get_local_sunrise_time(current_time)
    today_sunrise = today_sunrise.astimezone(timezone)
    today_sunset = sun.get_local_sunset_time(current_time + timedelta(days=1))
    today_sunset = today_sunset.astimezone(timezone)

    if current_time > today_sunset:
        delta_in_seconds = (current_time - today_sunset).seconds
        base_time = datetime.strptime("18:00:00", "%H:%M:%S")
    else:
        delta_in_seconds = (current_time - today_sunrise).seconds
        base_time = datetime.strptime("06:00:00", "%H:%M:%S")

    delta_in_hours = math.ceil(delta_in_seconds / 3600)
    seconds_list = []
    for i in range(0, delta_in_hours):
        time_ = today_sunset + timedelta(hours=i)
        duration = second_duration(time_, day_duration, night_duration,
                                   latitude, longitude, utc_offset)
        if i < delta_in_hours - 1:
            seconds_list += [duration] * 3600
        else:
            seconds_list += [duration] * (delta_in_hours - (delta_in_hours-1) * 3600)

    delta_seconds_fictif = sum(seconds_list)
    fictif_hour = base_time + timedelta(seconds=delta_seconds_fictif)

    return fictif_hour


# Clock visualization
def plot_clock(hours, minutes, seconds):
    """Trace une horloge circulaire avec des aiguilles pour heures, minutes, secondes."""
    # Calculate angles for hour, minute, and second hands
    second_angle = 2 * np.pi * seconds / 60
    minute_angle = 2 * np.pi * (minutes + seconds / 60) / 60
    hour_angle = 2 * np.pi * ((hours % 12) + minutes / 60) / 12

    # Plot clock face
    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw={"projection": "polar"})

    ax.scatter(0, 0, s=1000000, color="lightgray", zorder=1)
    ax.set_xticks(np.linspace(0, 2 * np.pi, 12, endpoint=False))
    ax.set_xticklabels(range(1, 13))
    ax.set_theta_direction(-1)
    ax.set_theta_offset(np.pi / 3.0)
    ax.grid(False)
    ax.set_yticks([])

    # Add clock hands
    ax.plot([0, second_angle], [0, 0.9], color="red", lw=1.5, label="Secondes", zorder=2)
    ax.plot([0, minute_angle], [0, 0.8], color="gray", lw=2, label="Minutes", zorder=2)
    ax.plot([0, hour_angle], [0, 0.65], color="gray", lw=2, label="Heures", zorder=2)

    # Add clock face markers
    for i in range(12):
        angle = 2 * np.pi * i / 12
        ax.plot([angle, angle], [0.9, 1.0], color="black", lw=1, zorder=2)

    ax.plot(0, 0, marker="o", color="black", markersize=10, zorder=3)
    # Title
    ax.set_title(
        f"{hours:02}:{minutes:02}:{seconds:02}",
        va="bottom",
    )
    return fig
