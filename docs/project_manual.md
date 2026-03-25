# Industrial IT Monitoring & Digital Twin Toolkit
## Project Manual

---

## 1. Introduction

This project aims to simulate an industrial monitoring system using a Digital Twin approach.

The goal is to model how IT conditions — such as CPU load, network stability, and service availability — can directly influence production performance.

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

| State | Description |
|-------|-------------|
| **RUN** | Normal production |
| **STOP** | Controlled stop |
| **FAULT** | Unexpected issue |

Transitions between states are influenced by:

- CPU load
- network status
- random events

---

## 5. Dataset Structure

Each row in the dataset represents a time snapshot.

Main fields include:

| Field | Description |
|-------|-------------|
| `timestamp` | Date and time of the snapshot |
| `machine_id` | Machine identifier |
| `state` | Machine state (RUN / STOP / FAULT) |
| `stop_reason` | Reason for stop (if applicable) |
| `cpu_percent` | CPU load percentage |
| `ram_percent` | RAM usage percentage |
| `produced_units` | Total units produced |
| `good_units` | Good units produced |
| `scrap_units` | Scrapped units |

> The dataset is not versioned in the repository. It is generated locally by running the simulator.

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

```
OEE = Availability × Performance × Quality
```

---

## 7. Data Analysis

The system performs:

- time-series analysis
- state distribution analysis
- downtime analysis
- correlation analysis (CPU vs production)

> A negative correlation indicates that higher CPU load can reduce production efficiency.

---

## 8. Intelligent Logic

The system generates:

- system health status
- alerts based on thresholds
- insights describing system behavior

**Example:** High CPU load combined with reduced production may indicate overload conditions.

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

### Prerequisites

#### Windows
1. Install **Python 3.10+** from [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - During installation, **check "Add Python to PATH"**
2. Install **Git** (optional, to clone the repo) from [https://git-scm.com/](https://git-scm.com/)

#### Linux / macOS
Python is usually pre-installed. Verify with:
```bash
python3 --version
```

---

### Step 1 — Download the project

Clone via Git:
```bash
git clone https://github.com/VektorBlock/industrial-it-digital-twin-toolkit.git
```

Or download the ZIP from GitHub → **Code → Download ZIP** and extract it.

---

### Step 2 — Open a terminal inside the project folder

All the following commands must be run from inside the project folder.

**Windows:**
- Open File Explorer and navigate to the extracted folder (e.g. `industrial-it-digital-twin-toolkit-main`)
- Click on the address bar at the top, type `cmd` and press Enter
- A Command Prompt window will open already positioned in that folder

Alternatively, right-click inside the folder while holding **Shift** → **"Open PowerShell window here"**

**Linux:**
- Open the file manager, navigate to the extracted folder
- Right-click inside the folder → **"Open Terminal here"** (the option name may vary by distro)

Alternatively, open a terminal and navigate manually:
```bash
cd ~/Downloads/industrial-it-digital-twin-toolkit
```

**macOS:**
- Open Finder and navigate to the extracted folder
- Right-click the folder → **"New Terminal at Folder"** (requires macOS Monterey or later)

Alternatively, open Terminal and navigate manually:
```bash
cd ~/Downloads/industrial-it-digital-twin-toolkit
```

---

### Step 3 — Install dependencies

**Windows:**
```cmd
pip install -r requirements.txt
```

**Linux / macOS:**
```bash
pip3 install -r requirements.txt
```

---

### Step 4 — Run the simulator

**Windows:**
```cmd
python src\simulator.py
```

**Linux / macOS:**
```bash
python3 src/simulator.py
```

At startup, the simulator asks the user to choose the simulation mode:

| Option | Mode | Description |
|--------|------|-------------|
| `1` | **Replicable** | Generates the same data at each execution — useful for documentation and reproducible analysis |
| `2` | **Variable** | Generates different data at each execution — useful for testing dynamic scenarios |

The generated file `data/production_data.csv` is overwritten at each execution and is intended to be created locally, not versioned in the repository.

---

### Step 5 — Run the dashboard

#### Local only (accessible only from this PC)

**Windows:**
```cmd
python -m streamlit run dashboard\app.py
```

**Linux / macOS:**
```bash
python3 -m streamlit run dashboard/app.py
```

Then open your browser at: [http://localhost:8501](http://localhost:8501)

---

#### Accessible from other PCs on the local network

**Windows:**
```cmd
python -m streamlit run dashboard\app.py --server.address 0.0.0.0 --server.port 8501
```

**Linux / macOS:**
```bash
python3 -m streamlit run dashboard/app.py --server.address 0.0.0.0 --server.port 8501
```

Then find your local IP address:

- **Windows:** open cmd and run `ipconfig` → look for **IPv4 Address** (e.g. `192.168.1.42`)
- **Linux / macOS:** run `hostname -I`

From another PC on the same network, open the browser at:
```
http://<your-ip>:8501
```

> **Windows Firewall:** if the connection is blocked, add an inbound rule for TCP port 8501 in Windows Defender Firewall.

---

### Optional: Streamlit configuration

To hide the Deploy button and clean up the UI, create the file `.streamlit/config.toml` in the project root:

```toml
[server]
address = "localhost"
port = 8501

[client]
toolbarMode = "minimal"
showErrorDetails = false
```

---

## 12. Compatibility

| OS | Supported |
|----|-----------|
| Windows | ✅ |
| Linux | ✅ |
| macOS | ✅ |

Python 3.10+ is required on all platforms.

---

## 13. Project Value

This project demonstrates:

- integration between IT and industrial systems
- practical use of data analysis
- KPI-driven monitoring logic
- the impact of IT infrastructure on production efficiency

---

## 14. Limitations

- simulated data only
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
