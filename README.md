# Industrial IT Monitoring & Digital Twin Toolkit

Lightweight industrial monitoring and digital twin project built in Python.

## Dashboard Preview

![Dashboard](screenshots/dashboard.png)

## What this project does

This project simulates a production machine and combines:

- machine state simulation
- IT metrics simulation
- industrial KPI calculation
- downtime analysis
- intelligent alerts
- interactive Streamlit dashboard

## Main technologies

- Python
- Pandas
- Streamlit

## Project structure

- src/simulator.py -> generates the simulated production data
- data/production_data.csv -> stores the generated dataset
- dashboard/app.py -> displays KPIs, charts, alerts, and insights

## How to run

Run the simulator:

python3 src/simulator.py

Run the dashboard:

python3 -m streamlit run dashboard/app.py

## Main KPIs

- Availability
- Performance
- Quality
- OEE

## Purpose

This project shows how IT conditions such as CPU load, network instability, and service availability can affect simulated industrial performance.

## Documentation

Full project manual available here:

docs/project_manual.md
