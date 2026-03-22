# Industrial IT Monitoring & Digital Twin Toolkit
## Project Manual

---

## 1. Introduction

This project aims to simulate an industrial monitoring system using a Digital Twin approach.

The goal is to model how IT conditions (CPU usage, network stability, system status) can directly impact industrial production performance.

---

## 2. Project Objectives

The system is designed to:

- simulate machine behavior
- generate IT metrics (CPU, RAM, network)
- calculate industrial KPIs (OEE)
- analyze downtime causes
- provide intelligent alerts
- visualize data through an interactive dashboard

---

## 3. System Architecture

The project is structured into three main layers:

### 3.1 Simulation Layer
- Generates machine states (RUN, STOP, FAULT)
- Simulates IT conditions (CPU load, network issues)

### 3.2 Data Layer
- Stores data in CSV format
- Structured as time-series data

### 3.3 Analytics & Visualization Layer
- Processes data using Pandas
- Displays insights via Streamlit dashboard

---

## 4. Machine Model

The simulated machine operates in different states:

- RUN → normal production
- STOP → planned stop
- FAULT → unexpected issue

Transitions between states are influenced by:
- CPU load
- network status
- random events

---

## 5. Dataset Structure

Each row in the dataset represents a time snapshot.

Main fields include:

- timestamp
- machine_id
- state
- stop_reason
- cpu_percent
- ram_percent
- production
- good_units
- scrap_units

---

## 6. KPI Calculation

### Availability
Ratio of operating time vs total time.

### Performance
Ratio between actual output and expected output.

### Quality
Ratio of good units vs total produced units.

### OEE
Overall Equipment Effectiveness:
OEE = Availability × Performance × Quality

---

## 7. Data Analysis

The system performs:

- time-series analysis
- state distribution analysis
- downtime analysis
- correlation analysis (CPU vs production)

Example:
A negative correlation indicates that higher CPU load reduces production efficiency.

---

## 8. Intelligent Logic

The system generates:

- system health status (OK, WARNING, CRITICAL)
- alerts based on thresholds
- insights describing system behavior

Example:
High downtime + high CPU = potential system overload

---

## 9. Dashboard

The Streamlit dashboard provides:

- KPI overview
- production trends
- CPU vs production correlation
- state distribution
- downtime breakdown
- real-time-like data table

---

## 10. Results Interpretation

Example output:

- OEE: 75.91% → acceptable but improvable
- Downtime: 36 minutes → moderate inefficiency
- Main issue: NETWORK_DOWN

Interpretation:
The system shows that IT instability can significantly affect production performance.

---

## 11. Project Value

This project demonstrates:

- integration between IT and industrial systems
- practical use of data analysis for operations
- impact of infrastructure on production efficiency

---

## 12. Limitations

- simulated data (not real sensors)
- single machine model
- no persistent database

---

## 13. Future Improvements

- multi-machine simulation
- real-time data ingestion
- anomaly detection
- predictive maintenance models
- database integration

---

## 14. Conclusion

The project successfully demonstrates a simplified Digital Twin capable of linking IT conditions to industrial performance.

It provides a foundation for more advanced industrial monitoring systems.
