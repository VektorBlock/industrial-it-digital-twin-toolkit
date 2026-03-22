# Industrial IT Monitoring & Digital Twin Toolkit
## Project Manual

---

## 1. Introduction

This project aims to simulate an industrial monitoring system using a Digital Twin approach.

The goal is to model how IT conditions such as CPU load, network stability, and service availability can directly influence production performance.

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
- STOP → controlled stop
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
- produced_units
- good_units
- scrap_units

The dataset is not intended to be versioned permanently in the repository, but generated locally by running the simulator.

---

## 6. KPI Calculation

### Availability
Ratio of operating time versus total observed time.

### Performance
Ratio between actual output and expected output.

### Quality
Ratio of good units versus total produced units.

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

A negative correlation indicates that higher CPU load can reduce production efficiency.

---

## 8. Intelligent Logic

The system generates:

- system health status
- alerts based on thresholds
- insights describing system behavior

Example:
High CPU load combined with reduced production may indicate overload conditions.

---

## 9. Dashboard

The Streamlit dashboard provides:

- KPI overview
- production trends
- CPU vs production correlation
- state distribution
- downtime breakdown
- data table

---

## 10. Results Interpretation

Example output may include:

- OEE around 75%
- moderate downtime
- network instability as a stop reason

This indicates a functioning system with room for performance improvement.

---

## 11. How to Use the Project

Requirements:

- Python 3.x
- pandas
- streamlit

Install dependencies:

pip install -r requirements.txt

Run the simulator:

python3 src/simulator.py

At startup, the simulator asks the user to choose the simulation mode:

1 = Replicable mode  
   generates the same data at each execution

2 = Variable mode  
   generates different data at each execution

Replicable mode is useful for documentation and reproducible analysis.  
Variable mode is useful for testing dynamic scenarios.

The generated CSV file (`data/production_data.csv`) is overwritten at each execution and is intended to be created locally.

Run the dashboard:

python3 -m streamlit run dashboard/app.py

Access through browser:

http://localhost:8501

---

## 12. Compatibility

The project is compatible with:

- Linux
- Windows
- macOS

Python installation is required.

---

## 13. Project Value

This project demonstrates:

- integration between IT and industrial systems
- practical use of data analysis
- KPI-driven monitoring logic
- the impact of IT infrastructure on production efficiency

---

## 14. Limitations

- simulated data
- single machine model
- no persistent database
- no real-time integration

---

## 15. Future Improvements

- multi-machine simulation
- persistent database layer
- anomaly detection
- predictive maintenance models
- IoT integration

---

## 16. Conclusion

The project demonstrates a simplified but coherent Digital Twin capable of linking IT conditions to industrial performance.

It provides a foundation for more advanced industrial monitoring systems.
