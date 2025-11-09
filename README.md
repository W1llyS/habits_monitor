# Habits Monitor

**Habits Monitor** is a Linux desktop application that runs in your system tray and
  helps you track your computer usage statistics. View your daily computer
  activity through interactive charts and detailed analytics.

---

## Features

- **System Tray Integration**  
  • Lightweight indicator that runs in the background.  
  • Start/stop monitoring with a single click.
  
- **Interactive Statistics**    
  • Date range filtering (Last 7/14/30 days, custom range, or all-time).  
  • Visual graphs powered by Highcharts showing daily trends.  
  • Exportable charts to CSV, JSON, or PDF formats.  
  
- **Privacy-Focused Design**  
  • All data stored locally in SQLite database.  
  • No external connections or data sharing.  
  • Complete control over your tracking data.  

---

## Interface Preview

<p align="center">
  <img src="screenshots/habits_04.png" alt="Chart" width="700" />
</p>

<p align="center">
  <img src="screenshots/habits_05.png" alt="Chart" width="700" />
</p>

---

## Technologies Used

  - **Platform**: Linux with X11 (does not support Wayland)
  - **Language**: Python 3
  - **UI Framework**: GTK 3.0 
  - **Database**: SQLite 
  - **Charting**: Highcharts.js 
  - **License**: MIT

---

## Usage

  1. Launch the application from your application menu or terminal.
  2. The Habits indicator appears in your system tray.
  3. Click Start monitor to begin tracking.
  4. Use your computer normally - all activity is tracked automatically.
  5. Click Statistics to view your usage patterns.
  6. Explore Button Stats and Keyboard Stats for detailed breakdowns.

---

## Requirements

  - Linux with **X11** (does not support Wayland)
  - Python 3
  - Python Xlib
  - GTK 3.0
  - SQLite3 

---
  
  This is my version of the Habits application with some modifications. 
  
  Original author: Lorenzo Carbonell (atareao)
