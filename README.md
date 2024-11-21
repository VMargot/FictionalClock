# Fictional Clock with Variable Seconds

This Python project simulates a **fictional clock** where the sun invariably rises at **6:00 AM** and sets at **6:00 PM**, regardless of the season. The duration of a second varies throughout the day and night to reflect seasonal changes while maintaining smooth, continuous variations with peaks at **12:00 PM** and **12:00 AM**.

---

## **Features**

- Simulates a fictional clock with:
  - Fixed sunrise at **6:00 AM**.
  - Fixed sunset at **6:00 PM**.
  - Adjustable second durations to reflect seasonal changes.
  - Smooth transitions between the dilation and contraction of seconds.
- Dynamic clock display using **Streamlit** with moving hands that update in real time.

---

## **Requirements**

- Python 3.8+
- Required libraries:
  - `streamlit`
  - `pandas`
  - `numpy`
  - `suntime`
  - `math`

Install the dependencies using:

```bash
pip install -r requirements.txt
```
---

## **Usage**
### **1. Running the Clock**
Run the Streamlit app to view the real-time fictional clock:
```bash
streamlit run main.py
```

### **2. Functions Overview**
**Core Functions**
- Calculates the day and night durations based on the given date and latitude.
```bash
get_day_night_durations(date, latitude)
```

- Computes the adjusted duration of a second at a given time, based on the current phase of the day or night.
```bash
second_duration(current_time, day_duration, night_duration, latitude, longitude)
```

- Converts real-world time into the corresponding fictional time, accounting for the adjusted second durations.
```bash
get_fictif_hour(current_time, day_duration, night_duration, latitude, longitude)
```

**Streamlit Clock**
The application visualizes:
- A fictional clock with moving hands representing hours, minutes, and seconds.
- Dynamic second movements reflecting the adjusted durations.

---

## **Example**
### **1. Calculate Day/Night Durations**
```bash
from datetime import datetime
day_duration, night_duration = get_day_night_durations(datetime.now(), latitude=45)
print(f"Day Duration: {day_duration} hours, Night Duration: {night_duration} hours")
```

### **2. Get Adjusted Fictional Time**
```bash
current_time = datetime.now()
fictif_time = get_fictif_hour(current_time, day_duration, night_duration, latitude=45, longitude=3)
print(f"Fictional Time: {fictif_time}")
```

---

## **Folder Structure**

📂 FictionalClock <br>
├── 📄 main.py &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; # Main Streamlit application<br>
├── 📄 clock_logic.py &nbsp; &nbsp; &nbsp; # Core logic for time adjustments<br>
├── 📄 requirements.txt &nbsp; # Python dependencies<br>
└── 📄 README.md &nbsp; &nbsp; &nbsp; &nbsp; # Project documentation<br>

---

## **Contributing**
Contributions are welcome! Feel free to open issues or submit pull requests for enhancements or bug fixes.

---

## **License**
This project is licensed under the MIT License. See the LICENSE file for details.
