# Solar Mo Lang SCADA System Documentation

# Overview

Solar Mo Lang is a SCADA-inspired solar monitoring system developed using Python.

The project simulates a renewable energy monitoring platform capable of:

* Simulating solar sensor data
* Monitoring battery and solar performance
* Detecting system issues
* Displaying real-time telemetry
* Visualizing system topology
* Tracking XP and rewards
* Displaying operational recommendations
* Managing user authentication
* Supporting future IoT integration

The system is divided into three major modules:

| File        | Purpose                         |
| ----------- | ------------------------------- |
| `main.py`   | Starts the application          |
| `ui.py`     | Handles the graphical interface |
| `engine.py` | Handles system logic and data   |

---

# Project Architecture

```text
main.py
   ↓
ui.py (GUI Layer)
   ↓
engine.py (Logic Layer)
```

---

# System Workflow

```text
User Starts Application
        ↓
main.py Launches App
        ↓
Login System Loads
        ↓
User Authenticates
        ↓
Dashboard Loads
        ↓
Sensor Data Generated
        ↓
Engine Processes Data
        ↓
UI Displays Telemetry
        ↓
Warnings & XP Updated
        ↓
Graph Refreshes Every 2 Seconds
```

---

# main.py Documentation

# Purpose

`main.py` is the main entry point of the Solar Mo Lang system.

It is responsible for:

* Starting the application
* Initializing the GUI
* Running the event loop
* Handling safe shutdowns

Think of this file as:

> "The launcher of the entire SCADA system."

---

# Source Code

```python
"""
Main entry point for the Solar Mo Lang
Run this file to start the program.
"""

import sys
from ui import App


def main():
    # Initialize the Application
    app = App()

    # Optional: Setup global exception handling or logging here

    try:
        # Start the main event loop
        app.mainloop()

    except KeyboardInterrupt:
        print("\nShutting down SCADA system...")
        app.shutdown()
        sys.exit(0)


if __name__ == "__main__":
    main()
```

---

# Imports Used in main.py

## `sys`

Provides system-level functions.

Used for:

```python
sys.exit(0)
```

which safely closes the application.

---

## `App`

```python
from ui import App
```

Imports the graphical user interface from `ui.py`.

Without this import:

* The system cannot launch
* No GUI will appear

---

# `main()` Function

```python
def main():
```

The main startup function.

Responsibilities:

1. Create the application
2. Start the interface
3. Handle shutdowns

---

# Application Initialization

```python
app = App()
```

Creates the main GUI application.

This automatically initializes:

* Login system
* Dashboard
* Sidebar
* Update loops
* Graphs
* Rewards system
* Toast notifications

---

# Event Loop

```python
app.mainloop()
```

Starts the graphical event loop.

The event loop continuously listens for:

* Mouse clicks
* Keyboard input
* Window actions
* Timed updates

Without `mainloop()`:

* The window would instantly close

---

# Keyboard Interrupt Handling

```python
except KeyboardInterrupt:
```

Handles interruptions such as:

```text
CTRL + C
```

Used for safe shutdown procedures.

---

# Safe Shutdown

```python
app.shutdown()
```

Stops the update loop and safely closes the application.

---

# Program Exit

```python
sys.exit(0)
```

Ends the program successfully.

---

# Entry Point Check

```python
if __name__ == "__main__":
```

Ensures the program only runs when executed directly.

---

# ui.py Documentation

# Purpose

`ui.py` handles the graphical user interface (GUI).

This is the part users interact with.

Responsibilities include:

* Login authentication
* Dashboard display
* Real-time telemetry
* Graph visualization
* Alerts and warnings
* Navigation system
* Rewards and quests
* Fault line visualization

---

# Imports Used in ui.py

```python
import logging
import datetime
import tkinter as tk
from tkinter import font as tkfont
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import engine
```

---

# Import Explanations

| Module          | Purpose                   |
| --------------- | ------------------------- |
| `logging`       | Error tracking            |
| `datetime`      | Time operations           |
| `tkinter`       | Base GUI framework        |
| `customtkinter` | Modern styled UI          |
| `matplotlib`    | Graph plotting            |
| `engine`        | Backend logic integration |

---

# Fonts and Themes

# `get_universal_font()`

Automatically selects a font based on the operating system.

Priority:

1. Segoe UI
2. Ubuntu
3. Arial

---

# `THEME`

Stores all application colors.

Benefits:

* Consistent design
* Easier maintenance
* Faster theme changes

---

# Main Application Class

```python
class App(ctk.CTk):
```

Main GUI window.

Everything displayed in the interface is controlled from this class.

---

# `__init__()`

Initializes the application.

Major responsibilities:

* Enable dark mode
* Configure window size
* Setup XP system
* Initialize data model
* Configure login credentials
* Load login screen

---

# Login System

# `_build_login()`

Creates the login page.

Components:

* Username input
* Password input
* Login button
* Error messages

---

# `_check_login()`

Validates credentials.

If successful:

```python
self._init_main_ui()
```

loads the full system interface.

Otherwise:

```text
Invalid credentials.
```

is displayed.

---

# Main Interface Setup

# `_init_main_ui()`

Creates the main application layout.

Components:

| Component      | Purpose            |
| -------------- | ------------------ |
| Sidebar        | Navigation         |
| View Container | Displays pages     |
| User Panel     | Displays user info |
| Update Loop    | Refreshes data     |

---

# Navigation System

# `switch_view()`

Changes the visible page.

Supported views:

| View        | Purpose         |
| ----------- | --------------- |
| Dashboard   | Main telemetry  |
| Fault Line  | Power topology  |
| Tips & Recs | Recommendations |
| Rewards     | XP system       |

---

# Dashboard View

# `_draw_dashboard()`

Creates the real-time monitoring dashboard.

Displays:

* Battery level
* Solar output
* Efficiency
* Temperature
* Telemetry graph
* Alert box

---

# Live Graph

Uses `matplotlib` to display:

```text
Battery Telemetry
```

Graph includes:

* Time axis
* Battery percentage axis
* Live updates every 2 seconds

---

# Toast Notification System

# `_trigger_toast()`

Displays floating warnings.

Features:

* Duplicate prevention
* Automatic removal
* Color-coded alerts

---

# Fault Line Visualization

# `_draw_fault_line()`

Displays the simulated solar network topology.

Components shown:

| Node         | Meaning             |
| ------------ | ------------------- |
| Solar Array  | PV generation       |
| Inverter     | DC to AC conversion |
| Battery Bank | Energy storage      |
| Main Grid    | Utility grid        |
| Home Load    | Consumption         |

---

# Tips & Recommendations

# `_draw_tips()`

Displays categorized recommendations.

Categories include:

* Energy Optimization
* Maintenance & Care
* Critical Safety

---

# Rewards System

# `_draw_rewards()`

Displays:

* User level
* XP points
* Progress bars
* Active quests

---

# Real-Time Update Loop

# `_update_loop()`

Main live refresh system.

Runs every:

```text
2 seconds
```

Responsibilities:

* Retrieve sensor data
* Update graphs
* Calculate XP
* Trigger warnings
* Update rewards
* Refresh dashboard

---

# Warning Detection

The system checks for:

| Warning           | Trigger                 |
| ----------------- | ----------------------- |
| Critical Battery  | Battery < 20%           |
| Thermal Alert     | Temperature > 45°C      |
| Low Efficiency    | Poor solar performance  |
| Conservation Mode | Low solar + low battery |

---

# Graph Updates

Battery history is plotted using:

```python
self.ax.plot(...)
```

---

# Shutdown System

# `shutdown()`

Safely closes the application.

Actions:

* Stops update loop
* Closes windows
* Releases resources

---

# engine.py Documentation

# Purpose

`engine.py` is the backend logic layer of the system.

Responsibilities:

* Simulate sensor readings
* Validate data
* Detect system conditions
* Calculate XP
* Store historical data
* Estimate backup runtime
* Generate recommendations
* Handle achievements
* Prepare cloud synchronization

---

# Imports Used in engine.py

```python
import random
from typing import Dict, Any, Optional
```

---

# `get_data()`

```python
def get_data(seed: Optional[int] = None) -> Dict[str, Any]:
```

Simulates sensor data.

Generated values:

| Sensor  | Purpose            |
| ------- | ------------------ |
| Battery | Battery percentage |
| Solar   | Solar output       |
| Voltage | Electrical voltage |
| Current | Electrical current |

---

# Example Output

```python
{
    "battery": 75,
    "solar": 320,
    "voltage": 12.5,
    "current": 4.2
}
```

---

# `_ensure_keys()`

Checks if all required sensor values exist.

Required keys:

* battery
* solar
* voltage
* current

Prevents crashes caused by missing data.

---

# Battery Check

# `check_battery()`

Returns:

| Battery Level | Result |
| ------------- | ------ |
| Above 40%     | Good   |
| 40% or below  | Low    |

---

# Solar Check

# `check_solar()`

Returns:

| Solar Output | Result |
| ------------ | ------ |
| Above 200    | Good   |
| 200 or below | Weak   |

---

# Efficiency Check

# `efficiency_check()`

Determines whether the system is operating efficiently.

Efficient if:

```text
Battery > 50%
AND
Solar > 200W
```

---

# Blackout Detection

# `blackout_check()`

Detects low voltage conditions.

Blackout warning if:

```text
Voltage < 10
```

---

# XP System

# `calculate_xp()`

Calculates rewards.

Rules:

| Condition     | XP  |
| ------------- | --- |
| Efficient     | +10 |
| Non-efficient | +2  |
| Blackout      | -5  |

---

# Data Storage

# `DataModel`

Stores historical telemetry.

Used for:

* Graphs
* Trend analysis
* Monitoring

---

# `add_reading()`

Adds sensor readings into storage history.

---

# `get_recent()`

Retrieves recent telemetry values.

Example:

```python
model.get_recent("battery", 10)
```

---

# `average()`

Calculates average telemetry values.

Example:

```python
model.average("solar", 20)
```

---

# Sensor Synchronization

# `sync_sensors()`

Acts as the sensor retrieval layer.

Currently:

* Uses simulated data

Future support:

* Arduino
* APIs
* IoT sensors

---

# Backup Runtime Estimation

# `estimate_backup_minutes()`

Estimates how long the battery can continue supplying power.

Formula:

```text
Remaining Energy / Load × 60
```

---

# Efficiency Recommendations

# `tips_for_efficiency()`

Provides system recommendations.

Examples:

* Reduce loads
* Clean panels
* Check inverter settings

---

# Achievement System

# `achievements_for_xp()`

Unlocks badges.

| XP   | Badge          |
| ---- | -------------- |
| 100+ | Rising Star    |
| 500+ | Solar Champion |

---

# Cloud Synchronization

# `sync_to_cloud()`

Placeholder for future cloud integration.

Potential future use:

* Upload analytics
* Store telemetry online
* Connect to web dashboards

---

# Overall System Features

| Feature                | Description                  |
| ---------------------- | ---------------------------- |
| Login System           | User authentication          |
| Dashboard              | Live telemetry monitoring    |
| Fault Line             | Power topology visualization |
| Graphs                 | Real-time telemetry plotting |
| Toast Alerts           | Floating notifications       |
| XP System              | Gamified rewards             |
| Quest System           | User objectives              |
| Tips & Recommendations | Operational guidance         |
| Data History           | Telemetry storage            |
| Backup Estimation      | Runtime prediction           |
| Achievements           | Badge unlocks                |

---

# Current Limitations

Currently:

* Uses simulated/random data
* No Arduino integration yet
* Static recommendation system
* No cloud database

---

# Planned Future Improvements

Potential upgrades:

* Real sensor integration
* Arduino connectivity
* Cloud synchronization
* Database support
* Machine learning recommendations
* Mobile dashboard
* User settings page
* PDF/Excel report exporting
* Long-term analytics
* Executable packaging using PyInstaller

---

# Beginner-Friendly Summary

| File        | Role                             |
| ----------- | -------------------------------- |
| `main.py`   | Launches the system              |
| `ui.py`     | Displays the graphical interface |
| `engine.py` | Handles backend logic            |

---

# Final Notes

Solar Mo Lang was designed to be:

* Beginner-friendly
* Modular
* Expandable
* Educational
* Easy to maintain

The project demonstrates important concepts in:

* SCADA systems
* Renewable energy monitoring
* Python GUI development
* Real-time telemetry
* IoT-ready architecture
* Data visualization
* Gamification systems

Although the current version uses simulated data, the architecture is intentionally designed to support future integration with:

* Real hardware sensors
* Arduino systems
* IoT devices
* Cloud platforms
* Smart-grid infrastructure

This makes Solar Mo Lang a strong foundation for educational, industrial, and research-oriented renewable energy monitoring systems.
